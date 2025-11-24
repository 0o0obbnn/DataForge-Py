# dataforge/core/redis_client.py
import os
from typing import TYPE_CHECKING

import redis
import redis.asyncio as aioredis
from redis.connection import ConnectionPool

if TYPE_CHECKING:
    pass


class RedisClient:
    """Redis客户端管理类，支持连接池"""

    def __init__(self):
        # 从环境变量或默认值获取Redis配置
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", 6379))
        self.password = os.getenv("REDIS_PASSWORD", None)
        self.db = int(os.getenv("REDIS_DB", 0))
        self.max_connections = int(os.getenv("REDIS_MAX_CONNECTIONS", 20))  # 连接池大小

        # 创建同步连接池
        self.sync_pool = ConnectionPool(
            host=self.host,
            port=self.port,
            password=self.password,
            db=self.db,
            max_connections=self.max_connections,
            decode_responses=True,
        )

        # 创建异步连接池
        self.async_pool = aioredis.ConnectionPool(
            host=self.host,
            port=self.port,
            password=self.password,
            db=self.db,
            max_connections=self.max_connections,
            decode_responses=True,
        )

        # 创建客户端实例
        self.sync_client = redis.Redis(connection_pool=self.sync_pool)
        self.async_client = aioredis.Redis(connection_pool=self.async_pool)

    def close(self):
        """关闭连接池"""
        if hasattr(self, "sync_pool"):
            self.sync_pool.disconnect()
        if hasattr(self, "async_pool"):
            self.async_pool.disconnect()


# 创建全局Redis客户端实例
_redis_client = RedisClient()


def get_redis_client() -> redis.Redis:
    """返回同步Redis客户端实例"""
    return _redis_client.sync_client


def get_async_redis_client() -> aioredis.Redis:  # type: ignore[type-arg]
    """返回异步Redis客户端实例"""
    return _redis_client.async_client
