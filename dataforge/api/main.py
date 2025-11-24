import asyncio
import json
import logging
import os
import uuid
from datetime import datetime
from typing import Any, Optional, cast

import redis.asyncio as aioredis
import uvicorn
from fastapi import (
    BackgroundTasks,
    Body,
    Depends,
    FastAPI,
    HTTPException,
    Path,
    Query,
    Request,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# 导入生成器模块以触发注册
from ..config.settings import get_settings
from ..core.exceptions import (
    DataForgeException,
    DataGenerationError,
    GeneratorNotFoundError,
)
from ..core.factory import (
    GeneratorFactory,
    GeneratorRegistry,
    default_registry,
)
from ..core.generator import GenerationContext, GeneratorConfig
from ..core.redis_client import get_async_redis_client
from ..core.relations import DataRelationManager, default_relation_manager
from ..core.startup_checks import perform_startup_checks
from ..output.formatter import OutputFormatter

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

logger.info(f"Registered generators: {len(default_registry.list_generators())}")

# 执行启动检查
try:
    perform_startup_checks()
except RuntimeError as e:
    logger.error(f"Startup failed: {e}")
    raise

# --- App and Settings Initialization ---
settings = get_settings()
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url=(
        settings.docs_url if settings.development_mode else None
    ),  # 生产环境禁用docs
    redoc_url=settings.redoc_url if settings.development_mode else None,
)

# 记录配置信息
logger.info(
    f"Environment: {'Development' if settings.development_mode else 'Production'}"
)
logger.info(f"CORS Origins: {settings.allowed_origins}")
logger.info(f"API Docs: {'Enabled' if settings.development_mode else 'Disabled'}")
logger.info(f"Available generators: {len(default_registry.list_generators())}")

# --- Dependency Injection Providers ---


def get_registry() -> GeneratorRegistry:
    # The registry is populated at import time by decorators, so we still use the global instance.
    # A more advanced pattern would involve an app startup event to build the registry.
    return default_registry


def get_relation_manager() -> DataRelationManager:
    return default_relation_manager


def get_generator_factory(
    registry: GeneratorRegistry = Depends(get_registry),
    relation_manager: DataRelationManager = Depends(get_relation_manager),
) -> GeneratorFactory:
    return GeneratorFactory(registry, relation_manager)


# --- API Models ---
class GeneratorRequest(BaseModel):
    """数据生成请求模型"""

    generator_type: str = Field(..., description="生成器类型")
    count: int = Field(1, ge=1, le=10000, description="生成数量")
    parameters: dict[str, Any] = Field(default_factory=dict, description="生成器参数")
    should_validate: bool = Field(True, description="是否启用数据校验")
    output_format: str = Field("json", description="输出格式")


class BatchGeneratorRequest(BaseModel):
    """批量生成请求模型"""

    generators: list[dict[str, Any]] = Field(..., description="生成器配置列表")
    count: int = Field(1, ge=1, le=1000, description="生成批次数")
    output_format: str = Field("json", description="输出格式")


class TaskResponse(BaseModel):
    """异步任务响应模型"""

    task_id: str = Field(..., description="任务ID")
    status: str = Field(..., description="任务状态")
    created_at: datetime = Field(..., description="创建时间")
    message: str = Field("", description="状态信息")


class GeneratorInfo(BaseModel):
    """生成器信息模型"""

    name: str = Field(..., description="生成器名称")
    type: str = Field(..., description="生成器类型")
    parameters: list[str] = Field(..., description="支持的参数")
    description: str = Field("", description="生成器描述")


class HealthResponse(BaseModel):
    """健康检查响应模型"""

    status: str = Field(..., description="服务状态")
    timestamp: datetime = Field(..., description="检查时间")
    version: str = Field(..., description="版本信息")
    generators_count: int = Field(..., description="可用生成器数量")


# --- Exception Handlers ---
@app.exception_handler(DataForgeException)
async def dataforge_exception_handler(request: Request, exc: DataForgeException):
    status_code = 400
    if isinstance(exc, GeneratorNotFoundError):
        status_code = 404
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "type": exc.error_code or "DATA_FORGE_ERROR",
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception for request {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected internal server error occurred.",
            }
        },
    )


# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# --- Task Management Constants ---
TASK_KEY_PREFIX = "dataforge:task:"
ALL_TASKS_SORTED_SET = "dataforge:tasks"
TASK_EXPIRATION_SECONDS = 86400  # 24 hours


# --- API Endpoints ---
@app.get("/", response_class=JSONResponse)
async def root():
    return {
        "name": "DataForge API",
        "description": settings.api_description,
        "version": settings.api_version,
        "docs": settings.docs_url,
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check(registry: GeneratorRegistry = Depends(get_registry)):
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.api_version,
        generators_count=len(registry.list_generators()),
    )


@app.get("/generators", response_model=list[GeneratorInfo])
async def list_generators(factory: GeneratorFactory = Depends(get_generator_factory)):
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
    if not factory.registry.is_registered(generator_name):
        raise GeneratorNotFoundError(generator_name)
    temp_config = GeneratorConfig(generator_type=generator_name, parameters={})
    generator = factory.create_generator(temp_config)
    return {
        "name": generator_name,
        "type": str(generator.generator_type.value),
        "parameters": generator.supported_parameters,
        "description": f"{generator_name}生成器",
        "example_parameters": _get_example_parameters(generator_name),
    }


@app.post("/generate/{generator_name}")
async def generate_data(
    generator_name: str = Path(..., description="生成器名称"),
    request: GeneratorRequest = Body(...),
    factory: GeneratorFactory = Depends(get_generator_factory),
):
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
    generator_type = request.get("generator_type") or request.get("type")
    if not generator_type:
        raise HTTPException(status_code=422, detail="请求体缺少 generator_type 字段")
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
    try:
        configs = []
        for gen_config in request.generators:
            if "generator_type" not in gen_config:
                raise HTTPException(
                    status_code=400, detail="每个生成器配置必须包含 'generator_type'"
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
        for _i in range(request.count):
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
    if not registry.is_registered(generator_name):
        raise GeneratorNotFoundError(generator_name)
    request.generator_type = generator_name
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
    background_tasks.add_task(_execute_async_generation, task_id, request)
    return TaskResponse(
        task_id=task_id,
        status="pending",
        created_at=created_at,
        message="任务已创建，正在处理中",
    )


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str = Path(..., description="任务ID")):
    redis = get_async_redis_client()
    task_key = f"{TASK_KEY_PREFIX}{task_id}"
    data = await redis.get(task_key)
    if not data:
        raise HTTPException(status_code=404, detail=f"任务 '{task_id}' 不存在或已过期")
    task_info = safe_json_loads(data)

    task_info["created_at"] = datetime.fromisoformat(task_info["created_at"])

    return task_info


@app.get("/tasks")
async def list_tasks(
    status: Optional[str] = Query(None, description="按状态过滤"),
    limit: int = Query(10, ge=1, le=100, description="返回数量限制"),
) -> dict[str, Any]:
    redis = get_async_redis_client()
    task_ids = await redis.zrevrange(ALL_TASKS_SORTED_SET, 0, limit * 5 - 1)
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


async def _execute_async_generation(task_id: str, request: GeneratorRequest) -> None:
    redis: aioredis.Redis = get_async_redis_client()
    task_key = f"{TASK_KEY_PREFIX}{task_id}"
    # Manually create dependencies for background task
    registry = get_registry()
    relation_manager = get_relation_manager()
    factory = GeneratorFactory(registry, relation_manager)

    def _update_task_field(field: str, value: Any):
        current_data = redis.get(task_key)

        if current_data:
            # Ensure data is a string before parsing
            if isinstance(current_data, bytes):
                data_str = current_data.decode("utf-8")
            else:
                data_str = str(current_data)

            task_info = json.loads(data_str)

            task_info[field] = value

            redis.set(task_key, json.dumps(task_info), ex=TASK_EXPIRATION_SECONDS)

    try:
        config = GeneratorConfig(
            generator_type=request.generator_type,
            parameters=request.parameters,
            count=request.count,
            validate=request.should_validate,
        )
        generator = factory.create_generator(config)

        # 优化批量生成效率
        batch_size = int(os.getenv("BATCH_SIZE", 100))  # 可配置的批处理大小
        all_data = []

        if request.count <= batch_size:
            # 如果数量小于等于批处理大小，直接处理
            batch_data = generator.generate_batch(request.count)
            all_data.extend(batch_data)
        else:
            # 分批处理大批量数据
            for i in range(0, request.count, batch_size):
                current_batch_size = min(batch_size, request.count - i)
                batch_data = generator.generate_batch(current_batch_size)
                all_data.extend(batch_data)
                progress = (i + current_batch_size) / request.count * 100
                _update_task_field("progress", round(progress, 2))

                # 在批次之间添加小延迟，避免对系统造成过大压力
                if i + current_batch_size < request.count:
                    await asyncio.sleep(0.01)  # 10毫秒延迟

        records = [{request.generator_type: item} for item in all_data]
        result = {
            "generator_type": request.generator_type,
            "count": len(all_data),
            "data": records,
            "timestamp": datetime.now().isoformat(),
        }

        final_task_data = {
            "status": "completed",
            "progress": 100,
            "result": result,
            "error": None,
        }

        await cast(Any, redis.hset(task_key, mapping=final_task_data))
        await cast(Any, redis.expire(task_key, TASK_EXPIRATION_SECONDS))

    except Exception as e:
        final_task_data = {
            "status": "failed",
            "progress": 0,
            "result": None,
            "error": str(e),
        }

        await cast(Any, redis.hset(task_key, mapping=final_task_data))
        await cast(Any, redis.expire(task_key, TASK_EXPIRATION_SECONDS))


def parse_json_params(json_str: str) -> dict[str, Any]:
    """通用JSON参数解析函数"""
    try:
        params = json.loads(json_str)
        if not isinstance(params, dict):
            raise ValueError("参数必须是JSON对象")
        return params
    except json.JSONDecodeError as e:
        raise ValueError("无效的JSON格式") from e
    except Exception as e:
        raise ValueError(f"参数解析错误: {str(e)}") from e


def validate_params_type(
    params: dict[str, Any], expected_types: dict[str, type]
) -> dict[str, Any]:
    """验证参数类型"""
    validated_params = {}
    for key, expected_type in expected_types.items():
        if key in params:
            if not isinstance(params[key], expected_type):
                raise ValueError(f"参数 {key} 必须是 {expected_type.__name__} 类型")
            validated_params[key] = params[key]
    return validated_params


def safe_json_loads(data) -> dict:
    """安全的JSON解析函数，处理字节和字符串数据"""
    if data is None:
        return {}
    if isinstance(data, bytes):
        data_str = data.decode("utf-8")
    else:
        data_str = str(data) if data else "{}"
    try:
        return json.loads(data_str)
    except json.JSONDecodeError:
        return {}


def _get_example_parameters(generator_name: str) -> dict[str, Any]:
    examples = {
        "idcard": {"region": "110000", "gender": "MALE"},
        "name": {"gender": "FEMALE", "include_pinyin": True},
        "email": {"type": "COMMON", "domains": ["example.com"]},
        "phone": {"operator": "MOBILE"},
        "integer": {"min": 1, "max": 100},
        "string": {"length": 10, "charset": "ALPHANUMERIC"},
        "uuid": {"version": 4, "format": "STANDARD"},
        "date": {"start_date": "2020-01-01", "end_date": "2023-12-31"},
        "ip_address": {"version": 4, "type": "PUBLIC"},
        "url": {"scheme": "https", "include_path": True},
    }
    return examples.get(generator_name, {})


def create_app() -> FastAPI:
    return app


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False) -> None:
    uvicorn.run(
        "dataforge.api.main:app", host=host, port=port, reload=reload, access_log=True
    )


if __name__ == "__main__":
    run_server(reload=True)
