"""
CLI配置处理模块

处理配置文件加载和GeneratorConfig构建
"""

import json
from pathlib import Path
from typing import Any

import yaml

from ..config.parser import ConfigParser
from ..core.generator import GeneratorConfig
from ..core.logging_config import get_logger

logger = get_logger(__name__)
config_parser = ConfigParser()


def load_config_file(config_path: str) -> list[GeneratorConfig]:
    """
    加载配置文件

    Args:
        config_path: 配置文件路径

    Returns:
        GeneratorConfig列表

    Raises:
        FileNotFoundError: 当配置文件不存在时
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with open(path, encoding="utf-8") as f:
        if path.suffix.lower() in [".yaml", ".yml"]:
            config_data = yaml.safe_load(f)
        else:
            config_data = json.load(f)

    return config_parser.parse_config(config_data)


def build_configs_from_args(args, count: int) -> list[GeneratorConfig]:
    """
    从命令行参数构建配置

    Args:
        args: 解析后的命令行参数
        count: 生成数量

    Returns:
        GeneratorConfig列表
    """
    configs = []
    generators = args.generators.split(",")

    for gen_type in generators:
        gen_type = gen_type.strip()
        parameters = extract_generator_params(args, gen_type)

        config = GeneratorConfig(
            generator_type=gen_type,
            parameters=parameters,
            count=count,
            validate=args.validate,
        )
        configs.append(config)

    return configs


def extract_generator_params(args, gen_type: str) -> dict[str, Any]:
    """
    提取特定生成器的参数

    Args:
        args: 解析后的命令行参数
        gen_type: 生成器类型

    Returns:
        参数字典
    """
    params = {}
    prefix = f"{gen_type}_"

    for arg_name, arg_value in vars(args).items():
        if arg_name.startswith(prefix) and arg_value is not None:
            param_name = arg_name[len(prefix) :]
            params[param_name] = arg_value

    return params
