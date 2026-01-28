#!/usr/bin/env python3
"""
DataForge 测试配置文件
统一配置测试环境和Python路径
"""

import os
import sys
from pathlib import Path

# Set a dummy JWT secret key for API tests before any other imports
os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-pytest"
os.environ["ALLOWED_ORIGINS"] = "http://localhost:3000,http://127.0.0.1:3000"

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# 将项目根目录添加到Python路径
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# 确保dataforge包可以被导入
DATAFORGE_PATH = PROJECT_ROOT / "dataforge"
if DATAFORGE_PATH.exists() and str(DATAFORGE_PATH.parent) not in sys.path:
    sys.path.insert(0, str(DATAFORGE_PATH.parent))

# 设置环境变量
os.environ["PYTHONPATH"] = str(PROJECT_ROOT)

# pytest配置
import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """自动设置测试环境"""
    print("✅ 测试环境已配置")
    print(f"📁 项目根目录: {PROJECT_ROOT}")
    print(f"🐍 Python路径: {sys.path[:3]}...")  # 只显示前3个路径

    # 验证dataforge包可以导入
    try:
        import dataforge

        print(
            f"✅ dataforge包导入成功: {dataforge.__file__ if hasattr(dataforge, '__file__') else 'built-in'}"
        )
    except ImportError as e:
        print(f"❌ dataforge包导入失败: {e}")
        pytest.fail(f"无法导入dataforge包: {e}")


@pytest.fixture
def project_root():
    """提供项目根目录路径"""
    return PROJECT_ROOT


@pytest.fixture
def test_data_dir():
    """提供测试数据目录路径"""
    return PROJECT_ROOT / "tests" / "data"


@pytest.fixture
def test_fixtures_dir():
    """提供测试固定数据目录路径"""
    return PROJECT_ROOT / "tests" / "fixtures"


# 测试标记配置
def pytest_configure(config):
    """配置pytest标记"""
    config.addinivalue_line("markers", "unit: 单元测试标记")
    config.addinivalue_line("markers", "integration: 集成测试标记")
    config.addinivalue_line("markers", "api: API测试标记")
    config.addinivalue_line("markers", "performance: 性能测试标记")
    config.addinivalue_line("markers", "security: 安全测试标记")


def pytest_collection_modifyitems(config, items):
    """自动为测试添加标记"""
    for item in items:
        # 根据文件路径自动添加标记
        test_path = str(item.fspath)

        if "/unit/" in test_path:
            item.add_marker(pytest.mark.unit)
        elif "/integration/" in test_path:
            item.add_marker(pytest.mark.integration)
        elif "/api/" in test_path:
            item.add_marker(pytest.mark.api)
        elif "/performance/" in test_path:
            item.add_marker(pytest.mark.performance)
        elif "/security/" in test_path:
            item.add_marker(pytest.mark.security)


# --- Core Application Fixtures ---

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.relations import DataRelationManager
from dataforge.generators.basic.address import AddressGenerator
from dataforge.generators.basic.age import AgeGenerator
from dataforge.generators.basic.company_name import CompanyNameGenerator
from dataforge.generators.basic.idcard import IDCardGenerator
from dataforge.generators.basic.license_plate import LicensePlateGenerator
from dataforge.generators.basic.name import NameGenerator
from dataforge.generators.basic.uuid import UUIDGenerator
from dataforge.generators.contact.email import EmailGenerator
from dataforge.generators.contact.phone import PhoneNumberGenerator
from dataforge.generators.finance.streaming import (
    StreamNewsGenerator,
    StreamOrderbookGenerator,
    StreamPriceGenerator,
    StreamTradeGenerator,
)
from dataforge.generators.identifier.bankcard import BankCardGenerator
from dataforge.generators.identifier.lei import LEIGenerator
from dataforge.generators.identifier.organization_code import OrganizationCodeGenerator
from dataforge.generators.identifier.uscc import USCCGenerator


@pytest.fixture(scope="module")
def empty_registry() -> GeneratorRegistry:
    """Provides an empty generator registry."""
    return GeneratorRegistry()


@pytest.fixture(scope="module")
def populated_registry(empty_registry: GeneratorRegistry) -> GeneratorRegistry:
    """Provides a registry populated with basic and streaming generators."""
    registry = empty_registry
    # Basic
    registry.register("name", NameGenerator)
    registry.register("age", AgeGenerator)
    registry.register("email", EmailGenerator)
    registry.register("idcard", IDCardGenerator)
    registry.register("bankcard", BankCardGenerator)
    registry.register(
        "phone", PhoneNumberGenerator
    )  # Note: PhoneNumberGenerator, not PhoneGenerator
    registry.register("uuid", UUIDGenerator)
    registry.register("address", AddressGenerator)
    registry.register("license_plate", LicensePlateGenerator)
    registry.register("company_name", CompanyNameGenerator)
    registry.register("uscc", USCCGenerator)
    registry.register("organization_code", OrganizationCodeGenerator)
    registry.register("lei", LEIGenerator)
    # Streaming
    registry.register("stream_price", StreamPriceGenerator)
    registry.register("stream_orderbook", StreamOrderbookGenerator)
    registry.register("stream_trade", StreamTradeGenerator)
    registry.register("stream_news", StreamNewsGenerator)
    return registry


@pytest.fixture
def generator_factory(populated_registry: GeneratorRegistry) -> GeneratorFactory:
    """Provides a GeneratorFactory with a populated registry."""
    relation_manager = DataRelationManager()  # Use a fresh relation manager
    return GeneratorFactory(
        registry=populated_registry, relation_manager=relation_manager
    )
