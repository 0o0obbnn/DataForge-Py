"""
API路由端点

定义所有FastAPI路由处理函数
"""

import json
import uuid
from datetime import datetime
from typing import Any

from fastapi import (
    BackgroundTasks,
    Body,
    Depends,
    HTTPException,
    Path,
    Query,
)

from ..config.settings import get_settings
from ..core.exceptions import (
    DataForgeException,
    DataGenerationError,
    GeneratorNotFoundError,
)
from ..core.factory import GeneratorFactory, GeneratorRegistry
from ..core.generator import GenerationContext, GeneratorConfig
from ..output.formatter import OutputFormatter
from .constants import (
    ALL_TASKS_SORTED_SET,
    TASK_EXPIRATION_SECONDS,
    TASK_KEY_PREFIX,
)
from .dependencies import get_generator_factory, get_registry
from .models import (
    BatchGeneratorRequest,
    GeneratorInfo,
    GeneratorRequest,
    HealthResponse,
    TaskResponse,
)
from .services import (
    execute_async_generation,
    get_example_parameters,
    get_task_from_redis,
    list_tasks_from_redis,
    safe_json_loads,
)

settings = get_settings()


def register_routes(app):
    """
    注册所有路由到FastAPI应用

    Args:
        app: FastAPI应用实例
    """

    @app.get("/")
    async def root():
        """API根路径"""
        return {
            "name": "DataForge API",
            "description": settings.api_description,
            "version": settings.api_version,
            "docs": settings.docs_url,
            "health": "/health",
        }

    @app.get("/health", response_model=HealthResponse)
    async def health_check(registry: GeneratorRegistry = Depends(get_registry)):
        """健康检查端点"""
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now(),
            version=settings.api_version,
            generators_count=len(registry.list_generators()),
        )

    @app.get("/generators")
    async def list_generators(
        factory: GeneratorFactory = Depends(get_generator_factory),
    ):
        """
        列出所有可用生成器
        """
        generators = factory.registry.list_generators()
        generator_info = []
        for name in generators:
            try:
                temp_config = GeneratorConfig(generator_type=name, parameters={})
                generator = factory.create_generator(temp_config)
                generator_info.append(
                    GeneratorInfo(
                        name=name,
                        type=str(generator.generator_type.value),
                        parameters=generator.supported_parameters,
                        description=f"{name}生成器",
                    )
                )
            except Exception:
                generator_info.append(
                    GeneratorInfo(
                        name=name,
                        type="unknown",
                        parameters=[],
                        description=f"{name}生成器 (配置可能存在错误)",
                    )
                )
        return sorted(generator_info, key=lambda x: x.name)

    @app.get("/generators/{generator_name}")
    async def get_generator_info(
        generator_name: str = Path(..., description="生成器名称"),
        factory: GeneratorFactory = Depends(get_generator_factory),
    ):
        """获取指定生成器的详细信息"""
        if not factory.registry.is_registered(generator_name):
            raise GeneratorNotFoundError(generator_name)
        temp_config = GeneratorConfig(generator_type=generator_name, parameters={})
        generator = factory.create_generator(temp_config)
        return {
            "name": generator_name,
            "type": str(generator.generator_type.value),
            "parameters": generator.supported_parameters,
            "description": f"{generator_name}生成器",
            "example_parameters": get_example_parameters(generator_name),
        }

    @app.post("/generate/{generator_name}")
    async def generate_data(
        generator_name: str = Path(..., description="生成器名称"),
        request: GeneratorRequest = Body(...),
        factory: GeneratorFactory = Depends(get_generator_factory),
    ):
        """
        生成数据

        根据指定的生成器类型和参数生成数据
        """
        if not factory.registry.is_registered(generator_name):
            raise GeneratorNotFoundError(generator_name)
        request.generator_type = generator_name
        try:
            config = GeneratorConfig(
                generator_type=request.generator_type,
                parameters=request.parameters,
                count=request.count,
                validate=request.should_validate,
            )
            generator = factory.create_generator(config)
            data = generator.generate_batch(request.count)
            formatter = OutputFormatter()
            records = [{request.generator_type: item} for item in data]
            if request.output_format.lower() == "json":
                return {
                    "success": True,
                    "generator_type": request.generator_type,
                    "count": len(data),
                    "data": records,
                    "timestamp": datetime.now().isoformat(),
                }
            else:
                formatted_data = formatter.format(records, request.output_format)
                return {
                    "success": True,
                    "generator_type": request.generator_type,
                    "count": len(data),
                    "format": request.output_format,
                    "data": formatted_data,
                    "timestamp": datetime.now().isoformat(),
                }
        except DataForgeException:
            raise
        except Exception as e:
            raise DataGenerationError(
                f"An unexpected error occurred during data generation: {e}"
            ) from e

    @app.post("/generate")
    async def generate_data_legacy(
        request: dict = Body(...),
        factory: GeneratorFactory = Depends(get_generator_factory),
    ):
        """
        生成数据（兼容旧版本）

        支持更灵活的请求格式，兼容旧API
        """
        generator_type = request.get("generator_type") or request.get("type")
        if not generator_type:
            raise HTTPException(
                status_code=422, detail="请求体缺少 generator_type 字段"
            )
        model = GeneratorRequest(
            generator_type=generator_type,
            count=int(request.get("count", 1)),
            parameters=request.get("parameters", {}),
            should_validate=bool(request.get("should_validate", True)),
            output_format=str(request.get("output_format", "json")),
        )
        return await generate_data(generator_type, model, factory)

    @app.post("/batch/generate")
    async def generate_batch_data(
        request: BatchGeneratorRequest,
        factory: GeneratorFactory = Depends(get_generator_factory),
    ):
        """
        批量生成数据

        支持同时生成多个不同类型的数据
        """
        try:
            configs = []
            for gen_config in request.generators:
                if "generator_type" not in gen_config:
                    raise HTTPException(
                        status_code=400,
                        detail="每个生成器配置必须包含 'generator_type'",
                    )
                generator_type = gen_config["generator_type"]
                if not factory.registry.is_registered(generator_type):
                    raise GeneratorNotFoundError(generator_type)
                config = GeneratorConfig(
                    generator_type=generator_type,
                    parameters=gen_config.get("parameters", {}),
                    validate=gen_config.get("should_validate", True),
                )
                configs.append(config)
            results = []
            for _ in range(request.count):
                context = GenerationContext()
                batch_result = factory.generate_batch_with_relations(configs, context)
                results.append(batch_result)
            return {
                "success": True,
                "generators": [config.generator_type for config in configs],
                "count": len(results),
                "data": results,
                "timestamp": datetime.now().isoformat(),
            }
        except DataForgeException:
            raise
        except Exception as e:
            raise DataGenerationError(
                f"An unexpected error occurred during batch generation: {e}"
            ) from e

    @app.post("/generate/async/{generator_name}")
    async def generate_data_async(
        background_tasks: BackgroundTasks,
        generator_name: str = Path(..., description="生成器名称"),
        request: GeneratorRequest = Body(...),
        registry: GeneratorRegistry = Depends(get_registry),
    ):
        """
        异步生成数据

        创建后台任务，返回任务ID，可以通过任务状态端点查询进度
        """
        if not registry.is_registered(generator_name):
            raise GeneratorNotFoundError(generator_name)
        request.generator_type = generator_name
        from ..core.redis_client import get_async_redis_client

        redis = get_async_redis_client()
        task_id = str(uuid.uuid4())
        task_key = f"{TASK_KEY_PREFIX}{task_id}"
        created_at = datetime.now()
        task_data = {
            "task_id": task_id,
            "status": "pending",
            "created_at": created_at.isoformat(),
            "generator_type": request.generator_type,
            "count": request.count,
            "progress": 0,
            "result": None,
            "error": None,
        }
        await redis.set(task_key, json.dumps(task_data), ex=TASK_EXPIRATION_SECONDS)
        await redis.zadd(ALL_TASKS_SORTED_SET, {task_id: created_at.timestamp()})
        background_tasks.add_task(execute_async_generation, task_id, request)
        return TaskResponse(
            task_id=task_id,
            status="pending",
            created_at=created_at,
            message="任务已创建，正在处理中",
        )

    @app.get("/tasks/{task_id}")
    async def get_task_status(task_id: str = Path(..., description="任务ID")):
        """
        获取与其他态

        查询异步任务的执行状态和结果
        """
        return await get_task_from_redis(task_id)

    @app.get("/tasks")
    async def list_tasks(
        status: str | None = Query(None, description="按状态过滤"),
        limit: int = Query(10, ge=1, le=100, description="返回数量限制"),
    ) -> dict[str, Any]:
        """
        列出所有任务

        获取后台任务列表，支持状态过滤和数量限制
        """
        redis, task_ids = await list_tasks_from_redis()

        if not task_ids:
            return {
                "total": await redis.zcard(ALL_TASKS_SORTED_SET),
                "filtered": 0,
                "tasks": [],
            }

        task_keys = [f"{TASK_KEY_PREFIX}{task_id}" for task_id in task_ids]
        tasks_data = await redis.mget(task_keys)
        tasks = []
        for data in tasks_data or []:
            if data:
                tasks.append(safe_json_loads(data))

        if status:
            tasks = [t for t in tasks if t.get("status") == status]

        tasks = tasks[:limit]

        return {
            "total": await redis.zcard(ALL_TASKS_SORTED_SET),
            "filtered": len(tasks),
            "tasks": tasks,
        }
