"""
服务层模块

包含后台任务执行、参数解析等业务逻辑函数
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Any

import redis.asyncio as aioredis

from ..core.factory import GeneratorFactory, GeneratorRegistry, default_registry
from ..core.generator import GeneratorConfig
from ..core.redis_client import get_async_redis_client
from ..core.relations import DataRelationManager, default_relation_manager
from .constants import (
    ALL_TASKS_SORTED_SET,
    BATCH_DELAY_SECONDS,
    DEFAULT_BATCH_SIZE,
    TASK_EXPIRATION_SECONDS,
    TASK_KEY_PREFIX,
)
from .models import GeneratorRequest

logger = logging.getLogger(__name__)


def parse_json_params(json_str: str) -> dict[str, Any]:
    """
    通用JSON参数解析函数

    Args:
        json_str: JSON字符串

    Returns:
        解析后的字典

    Raises:
        ValueError: 当JSON格式无效或不是对象类型时
    """
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
    """
    验证参数类型

    Args:
        params: 待验证的参数字典
        expected_types: 期望的参数类型映射

    Returns:
        验证通过后的参数字典

    Raises:
        ValueError: 当参数类型不匹配时
    """
    validated_params = {}
    for key, expected_type in expected_types.items():
        if key in params:
            if not isinstance(params[key], expected_type):
                raise ValueError(f"参数 {key} 必须是 {expected_type.__name__} 类型")
            validated_params[key] = params[key]
    return validated_params


def safe_json_loads(data) -> dict:
    """
    安全的JSON解析函数，处理字节和字符串数据

    Args:
        data: 字节或字符串数据

    Returns:
        解析后的字典，解析失败时返回空字典
    """
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


def get_example_parameters(generator_name: str) -> dict[str, Any]:
    """
    获取生成器的示例参数

    Args:
        generator_name: 生成器名称

    Returns:
        示例参数字典
    """
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
    result = examples.get(generator_name, {})
    return result if isinstance(result, dict) else {}  # type: ignore[return-value]


async def execute_async_generation(
    task_id: str,
    request: GeneratorRequest,
    registry: GeneratorRegistry | None = None,
    relation_manager: DataRelationManager | None = None,
) -> None:
    """
    执行异步数据生成任务

    Args:
        task_id: 任务ID
        request: 生成请求
        registry: 生成器注册表（可选，默认使用全局实例）
        relation_manager: 关系管理器（可选，默认使用全局实例）
    """
    redis: aioredis.Redis = get_async_redis_client()
    task_key = f"{TASK_KEY_PREFIX}{task_id}"

    # 如果未提供依赖，使用全局实例
    if registry is None:
        registry = default_registry

    if relation_manager is None:
        relation_manager = default_relation_manager

    factory = GeneratorFactory(registry, relation_manager)

    async def update_task_field(field: str, value: Any):
        """更新任务字段"""
        current_data = await redis.get(task_key)

        if current_data:
            # 确保数据是字符串再解析
            if isinstance(current_data, bytes):
                data_str = current_data.decode("utf-8")
            else:
                data_str = str(current_data)

            task_info = json.loads(data_str)
            task_info[field] = value

            await redis.set(task_key, json.dumps(task_info), ex=TASK_EXPIRATION_SECONDS)

    try:
        config = GeneratorConfig(
            generator_type=request.generator_type,
            parameters=request.parameters,
            count=request.count,
            validate=request.should_validate,
        )
        generator = factory.create_generator(config)

        # 优化批量生成效率
        batch_size = int(
            os.getenv("BATCH_SIZE", str(DEFAULT_BATCH_SIZE))
        )  # 可配置的批处理大小
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
                await update_task_field("progress", round(progress, 2))

                # 在批次之间添加小延迟，避免对系统造成过大压力
                if i + current_batch_size < request.count:
                    await asyncio.sleep(BATCH_DELAY_SECONDS)

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

        await redis.set(
            task_key, json.dumps(final_task_data), ex=TASK_EXPIRATION_SECONDS
        )

    except Exception as e:
        logger.error(f"Async generation failed for task {task_id}: {e}", exc_info=True)
        final_task_data = {
            "status": "failed",
            "progress": 0,
            "result": None,
            "error": str(e),
        }

        await redis.set(
            task_key, json.dumps(final_task_data), ex=TASK_EXPIRATION_SECONDS
        )


async def get_task_from_redis(task_id: str) -> dict:
    """
    从Redis获取任务信息

    Args:
        task_id: 任务ID

    Returns:
        任务信息字典

    Raises:
        HTTPException: 当任务不存在或已过期时
    """
    from fastapi import HTTPException

    redis = get_async_redis_client()
    task_key = f"{TASK_KEY_PREFIX}{task_id}"
    data = await redis.get(task_key)
    if not data:
        raise HTTPException(status_code=404, detail=f"任务 '{task_id}' 不存在或已过期")
    task_info = safe_json_loads(data)
    task_info["created_at"] = datetime.fromisoformat(task_info["created_at"])
    return task_info


async def list_tasks_from_redis() -> tuple[aioredis.Redis, list[str]]:
    """
    从Redis获取任务列表

    Returns:
        (redis客户端, 任务ID列表)
    """
    redis = get_async_redis_client()
    task_ids = await redis.zrevrange(ALL_TASKS_SORTED_SET, 0, 49)
    return redis, task_ids
