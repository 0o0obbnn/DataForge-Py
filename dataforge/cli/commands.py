"""
CLI命令处理模块

处理list、validate等子命令
"""

from ..core.factory import default_factory, default_registry
from ..core.generator import GeneratorConfig
from ..core.logging_config import get_logger
from .config import load_config_file

logger = get_logger(__name__)


def handle_list(args) -> int:
    """
    处理list命令

    Args:
        args: 解析后的命令行参数

    Returns:
        退出码
    """
    generator_names = default_registry.list_generators()

    logger.info("可用的数据生成器:")
    for name in sorted(generator_names):
        # 获取生成器类来显示支持的参数
        try:
            temp_config = GeneratorConfig(generator_type=name, parameters={})
            generator = default_factory.create_generator(temp_config)
            params = ", ".join(generator.supported_parameters)
            logger.info(f"  {name:<20} - 参数: {params}")
        except Exception:
            logger.info(f"  {name}")

    return 0


def handle_validate(args) -> int:
    """
    处理validate命令

    Args:
        args: 解析后的命令行参数

    Returns:
        退出码
    """
    try:
        load_config_file(args.config_file)
        logger.info(f"配置文件 {args.config_file} 验证成功")
        return 0
    except Exception as e:
        logger.error(f"配置文件验证失败: {e}")
        return 1
