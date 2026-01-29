"""
API请求和响应模型

定义所有Pydantic模型，用于请求验证和响应格式化
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


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
