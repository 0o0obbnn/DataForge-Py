"""
DataForge Web API 服务
基于FastAPI的RESTful API服务
"""
import time
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks, Query, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

from ..core.factory import default_factory, default_registry
from ..core.generator import GeneratorConfig, GenerationContext
from ..output.formatter import OutputFormatter


# API数据模型
class GeneratorRequest(BaseModel):
    """数据生成请求模型"""
    generator_type: str = Field(..., description="生成器类型")
    count: int = Field(1, ge=1, le=10000, description="生成数量")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="生成器参数")
    validate: bool = Field(True, description="是否启用数据校验")
    output_format: str = Field("json", description="输出格式")


class BatchGeneratorRequest(BaseModel):
    """批量生成请求模型"""
    generators: List[Dict[str, Any]] = Field(..., description="生成器配置列表")
    count: int = Field(1, ge=1, le=1000, description="生成批次数")
    output_format: str = Field("json", description="输出格式")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "generators": [
                    {"generator_type": "name", "parameters": {"gender": "FEMALE"}},
                    {"generator_type": "email", "parameters": {"type": "COMMON"}}
                ],
                "count": 5,
                "output_format": "json"
            }
        }
    }


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
    parameters: List[str] = Field(..., description="支持的参数")
    description: str = Field("", description="生成器描述")


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str = Field(..., description="服务状态")
    timestamp: datetime = Field(..., description="检查时间")
    version: str = Field(..., description="版本信息")
    generators_count: int = Field(..., description="可用生成器数量")


# 全局变量
app = FastAPI(
    title="DataForge API",
    description="高效、灵活的测试数据生成API服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 任务存储（生产环境应使用Redis等）
tasks_storage = {}
task_counter = 0

# 添加CORS支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=JSONResponse)
async def root():
    """根路径，返回API信息"""
    return {
        "name": "DataForge API",
        "description": "高效、灵活的测试数据生成API服务",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查端点"""
    generators = default_registry.list_generators()
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0",
        generators_count=len(generators)
    )


@app.get("/generators", response_model=List[GeneratorInfo])
async def list_generators():
    """列出所有可用的数据生成器"""
    generators = default_registry.list_generators()
    generator_info = []
    
    for name in generators:
        try:
            # 创建临时实例获取信息
            temp_config = GeneratorConfig(generator_type=name, parameters={})
            generator = default_factory.create_generator(temp_config)
            
            generator_info.append(GeneratorInfo(
                name=name,
                type=str(generator.generator_type.value),
                parameters=generator.supported_parameters,
                description=f"{name}生成器"
            ))
        except Exception as e:
            # 如果创建失败，提供基本信息
            generator_info.append(GeneratorInfo(
                name=name,
                type="unknown",
                parameters=[],
                description=f"{name}生成器 (配置错误: {str(e)})"
            ))
    
    return sorted(generator_info, key=lambda x: x.name)


@app.get("/generators/{generator_name}")
async def get_generator_info(generator_name: str = Path(..., description="生成器名称")):
    """获取特定生成器的详细信息"""
    if not default_registry.is_registered(generator_name):
        raise HTTPException(status_code=404, detail=f"生成器 '{generator_name}' 不存在")
    
    try:
        temp_config = GeneratorConfig(generator_type=generator_name, parameters={})
        generator = default_factory.create_generator(temp_config)
        
        return {
            "name": generator_name,
            "type": str(generator.generator_type.value),
            "parameters": generator.supported_parameters,
            "description": f"{generator_name}生成器",
            "example_parameters": _get_example_parameters(generator_name)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取生成器信息失败: {str(e)}")


@app.post("/generate/{generator_name}")
async def generate_data(
    generator_name: str = Path(..., description="生成器名称"),
    request: GeneratorRequest = Body(...)
):
    """生成指定类型的数据"""
    if not default_registry.is_registered(generator_name):
        raise HTTPException(status_code=404, detail=f"生成器 '{generator_name}' 不存在")
    
    # 使用路径参数中的生成器类型
    request.generator_type = generator_name
    
    try:
        # 创建生成器配置
        config = GeneratorConfig(
            generator_type=request.generator_type,
            parameters=request.parameters,
            count=request.count,
            validate=request.validate
        )
        
        # 生成数据
        generator = default_factory.create_generator(config)
        data = generator.generate_batch(request.count)
        
        # 格式化输出
        formatter = OutputFormatter()
        if request.output_format.lower() == 'json':
            # 转换为记录格式
            records = [{request.generator_type: item} for item in data]
            return {
                "success": True,
                "generator_type": request.generator_type,
                "count": len(data),
                "data": records,
                "timestamp": datetime.now().isoformat()
            }
        else:
            # 其他格式
            records = [{request.generator_type: item} for item in data]
            formatted_data = formatter.format(records, request.output_format)
            return {
                "success": True,
                "generator_type": request.generator_type,
                "count": len(data),
                "format": request.output_format,
                "data": formatted_data,
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"数据生成失败: {str(e)}")


@app.post("/batch/generate")
async def generate_batch_data(request: BatchGeneratorRequest):
    """批量生成多种类型的关联数据"""
    try:
        # 构建生成器配置列表
        configs = []
        for gen_config in request.generators:
            if 'generator_type' not in gen_config:
                raise HTTPException(status_code=400, detail="每个生成器配置必须包含 'generator_type'")
            
            generator_type = gen_config['generator_type']
            if not default_registry.is_registered(generator_type):
                raise HTTPException(status_code=404, detail=f"生成器 '{generator_type}' 不存在")
            
            config = GeneratorConfig(
                generator_type=generator_type,
                parameters=gen_config.get('parameters', {}),
                validate=gen_config.get('validate', True)
            )
            configs.append(config)
        
        # 生成关联数据
        results = []
        for i in range(request.count):
            context = GenerationContext()
            batch_result = default_factory.generate_batch_with_relations(configs, context)
            results.append(batch_result)
        
        return {
            "success": True,
            "generators": [config.generator_type for config in configs],
            "count": len(results),
            "data": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"批量数据生成失败: {str(e)}")


@app.post("/generate/async/{generator_name}")
async def generate_data_async(
    background_tasks: BackgroundTasks,
    generator_name: str = Path(..., description="生成器名称"),
    request: GeneratorRequest = Body(...)
):
    """异步生成数据（用于大量数据生成）"""
    global task_counter
    
    if not default_registry.is_registered(generator_name):
        raise HTTPException(status_code=404, detail=f"生成器 '{generator_name}' 不存在")
    
    request.generator_type = generator_name
    
    # 创建任务ID
    task_counter += 1
    task_id = f"task_{task_counter}_{int(time.time())}"
    
    # 初始化任务状态
    tasks_storage[task_id] = {
        "task_id": task_id,
        "status": "pending",
        "created_at": datetime.now(),
        "generator_type": request.generator_type,
        "count": request.count,
        "progress": 0,
        "result": None,
        "error": None
    }
    
    # 添加后台任务
    background_tasks.add_task(
        _execute_async_generation,
        task_id,
        request
    )
    
    return TaskResponse(
        task_id=task_id,
        status="pending",
        created_at=tasks_storage[task_id]["created_at"],
        message="任务已创建，正在处理中"
    )


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str = Path(..., description="任务ID")):
    """获取异步任务状态"""
    if task_id not in tasks_storage:
        raise HTTPException(status_code=404, detail=f"任务 '{task_id}' 不存在")
    
    task_info = tasks_storage[task_id]
    
    return {
        "task_id": task_id,
        "status": task_info["status"],
        "created_at": task_info["created_at"],
        "generator_type": task_info["generator_type"],
        "count": task_info["count"],
        "progress": task_info["progress"],
        "result": task_info["result"] if task_info["status"] == "completed" else None,
        "error": task_info["error"] if task_info["status"] == "failed" else None
    }


@app.get("/tasks")
async def list_tasks(
    status: Optional[str] = Query(None, description="按状态过滤"),
    limit: int = Query(10, ge=1, le=100, description="返回数量限制")
):
    """列出所有任务"""
    tasks = list(tasks_storage.values())
    
    # 按状态过滤
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    
    # 按创建时间排序（最新的在前）
    tasks.sort(key=lambda x: x["created_at"], reverse=True)
    
    # 限制返回数量
    tasks = tasks[:limit]
    
    return {
        "total": len(tasks_storage),
        "filtered": len(tasks),
        "tasks": tasks
    }


async def _execute_async_generation(task_id: str, request: GeneratorRequest):
    """执行异步数据生成"""
    try:
        # 更新任务状态
        tasks_storage[task_id]["status"] = "running"
        tasks_storage[task_id]["progress"] = 0
        
        # 创建生成器
        config = GeneratorConfig(
            generator_type=request.generator_type,
            parameters=request.parameters,
            validate=request.validate
        )
        generator = default_factory.create_generator(config)
        
        # 分批生成数据（避免内存溢出）
        batch_size = min(1000, request.count)
        all_data = []
        
        for i in range(0, request.count, batch_size):
            current_batch_size = min(batch_size, request.count - i)
            batch_data = generator.generate_batch(current_batch_size)
            all_data.extend(batch_data)
            
            # 更新进度
            progress = (i + current_batch_size) / request.count * 100
            tasks_storage[task_id]["progress"] = round(progress, 2)
        
        # 格式化结果
        formatter = OutputFormatter()
        records = [{request.generator_type: item} for item in all_data]
        
        result = {
            "generator_type": request.generator_type,
            "count": len(all_data),
            "data": records,
            "timestamp": datetime.now().isoformat()
        }
        
        # 完成任务
        tasks_storage[task_id]["status"] = "completed"
        tasks_storage[task_id]["progress"] = 100
        tasks_storage[task_id]["result"] = result
        
    except Exception as e:
        # 任务失败
        tasks_storage[task_id]["status"] = "failed"
        tasks_storage[task_id]["error"] = str(e)


def _get_example_parameters(generator_name: str) -> Dict[str, Any]:
    """获取生成器的示例参数"""
    examples = {
        'idcard': {'region': '110000', 'gender': 'MALE'},
        'name': {'gender': 'FEMALE', 'include_pinyin': True},
        'email': {'type': 'COMMON', 'domains': ['example.com']},
        'phone': {'operator': 'MOBILE'},
        'integer': {'min': 1, 'max': 100},
        'string': {'length': 10, 'charset': 'ALPHANUMERIC'},
        'uuid': {'version': 4, 'format': 'STANDARD'},
        'date': {'start_date': '2020-01-01', 'end_date': '2023-12-31'},
        'ip_address': {'version': 4, 'type': 'PUBLIC'},
        'url': {'scheme': 'https', 'include_path': True}
    }
    
    return examples.get(generator_name, {})


def create_app():
    """创建FastAPI应用实例"""
    return app


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """运行API服务器"""
    uvicorn.run(
        "dataforge.api.main:app",
        host=host,
        port=port,
        reload=reload,
        access_log=True
    )


if __name__ == "__main__":
    run_server(reload=True)