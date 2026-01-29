#!/usr/bin/env python3
"""
DataForge API 批量生成功能测试 (pytest风格)
"""

import pytest
from fastapi.testclient import TestClient

from dataforge.api.main import app


@pytest.fixture(scope="module")
def api_client():
    """提供一个FastAPI的TestClient"""
    with TestClient(app) as client:
        yield client


def test_batch_generate_empty_request(api_client: TestClient):
    """测试空的批量生成请求, 应返回422 Unprocessable Entity"""
    response = api_client.post("/batch/generate", json={})
    assert response.status_code == 422


def test_batch_generate_minimal_valid_request(api_client: TestClient):
    """测试最小化的有效批量生成请求"""
    # Note: The `uuid` generator is not in the default populated_registry.
    # We need a way to ensure it's available for this API test.
    # For now, we assume it's registered at startup.
    minimal_payload = {"generators": [{"generator_type": "uuid"}], "count": 2}
    response = api_client.post("/batch/generate", json=minimal_payload)
    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert "data" in result
    assert len(result["data"]) == 2
    assert "uuid" in result["data"][0]


def test_batch_generate_with_invalid_generator(api_client: TestClient):
    """测试当请求包含无效生成器时的行为"""
    payload = {"generators": [{"generator_type": "invalid-generator-type"}], "count": 1}
    response = api_client.post("/batch/generate", json=payload)
    assert response.status_code == 404  # Not Found
    result = response.json()
    # API错误响应格式: {"error": {"type": ..., "message": ..., "details": ...}}
    assert "error" in result
    assert (
        "invalid-generator-type" in result["error"]["message"]
        or "not found" in result["error"]["message"].lower()
    )


def test_batch_generate_multiple_generators(api_client: TestClient):
    """测试使用多个生成器的批量生成请求"""
    payload = {
        "generators": [{"generator_type": "name"}, {"generator_type": "email"}],
        "count": 3,
    }
    response = api_client.post("/batch/generate", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert len(result["data"]) == 3
    for record in result["data"]:
        assert "name" in record
        assert "email" in record
