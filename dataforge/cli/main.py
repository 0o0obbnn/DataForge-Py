"""
DataForge CLI主入口
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Optional

import yaml

from ..config.parser import ConfigParser
from ..core.factory import default_factory, default_registry
from ..core.generator import GenerationContext, GeneratorConfig
from ..core.logging_config import setup_logging, get_logger
from ..output.formatter import OutputFormatter


class DataForgeCLI:
    """DataForge命令行界面"""

    def __init__(self):
        self.parser = self._create_parser()
        self.config_parser = ConfigParser()
        self.output_formatter = OutputFormatter()
        self.logger = get_logger(self.__class__.__name__)

    def _create_parser(self) -> argparse.ArgumentParser:
        """创建命令行参数解析器"""
        parser = argparse.ArgumentParser(
            prog="dataforge",
            description="DataForge - 高效、灵活的测试数据生成工具",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
示例用法:
  # 生成10个身份证号
  dataforge generate idcard --count 10

  # 生成银行卡号并输出为JSON
  dataforge generate bankcard --count 5 --output.format json

  # 根据配置文件生成数据
  dataforge generate --config user_data.yaml

  # 生成关联数据（身份证和对应年龄）
  dataforge generate idcard,age --count 10 --idcard.gender MALE --age.min 25 --age.max 45
            """,
        )

        # 全局参数
        parser.add_argument("--version", action="version", version="DataForge 1.0.0")
        parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
        parser.add_argument("--debug", action="store_true", help="调试模式")

        # 子命令
        subparsers = parser.add_subparsers(dest="command", help="可用命令")

        # generate 子命令
        generate_parser = subparsers.add_parser("generate", help="生成测试数据")
        self._add_generate_args(generate_parser)

        # list 子命令
        list_parser = subparsers.add_parser("list", help="列出可用的生成器")
        list_parser.add_argument(
            "--type",
            choices=["basic", "identifier", "contact", "network", "all"],
            default="all",
            help="生成器类型",
        )

        # validate 子命令
        validate_parser = subparsers.add_parser("validate", help="验证配置文件")
        validate_parser.add_argument("config_file", help="配置文件路径")

        return parser

    def _add_generate_args(self, parser: argparse.ArgumentParser):
        """添加generate命令的参数"""
        # 基本参数
        parser.add_argument("generators", nargs="?", help="生成器类型（逗号分隔）")
        parser.add_argument("--config", "-c", help="配置文件路径")
        parser.add_argument("--count", "-n", type=int, default=1, help="生成数量")

        # 输出参数
        output_group = parser.add_argument_group("输出选项")
        output_group.add_argument(
            "--output-format",
            dest="output_format",
            choices=["csv", "json", "xml", "sql", "yaml"],
            default="json",
            help="输出格式",
        )
        output_group.add_argument(
            "--output-file", dest="output_file", help="输出文件路径"
        )
        output_group.add_argument(
            "--output-pretty",
            dest="output_pretty",
            action="store_true",
            help="美化输出",
        )
        output_group.add_argument(
            "--output-encoding",
            dest="output_encoding",
            default="utf-8",
            help="输出编码",
        )

        # 数据校验参数
        validation_group = parser.add_argument_group("校验选项")
        validation_group.add_argument(
            "--validate", action="store_true", default=True, help="启用数据校验"
        )
        validation_group.add_argument(
            "--no-validate", dest="validate", action="store_false", help="禁用数据校验"
        )

        # 身份证参数
        idcard_group = parser.add_argument_group("身份证选项")
        idcard_group.add_argument(
            "--idcard-region", dest="idcard_region", help="地区代码或名称"
        )
        idcard_group.add_argument(
            "--idcard-gender",
            dest="idcard_gender",
            choices=["MALE", "FEMALE", "ANY"],
            help="性别",
        )
        idcard_group.add_argument(
            "--idcard-birth-date-range",
            dest="idcard_birth_date_range",
            help="出生日期范围 (格式: YYYY-MM-DD,YYYY-MM-DD)",
        )
        idcard_group.add_argument(
            "--idcard-valid",
            dest="idcard_valid",
            type=bool,
            default=True,
            help="是否生成有效身份证",
        )

        # 银行卡参数
        bankcard_group = parser.add_argument_group("银行卡选项")
        bankcard_group.add_argument(
            "--bankcard-type",
            dest="bankcard_type",
            choices=["DEBIT", "CREDIT", "BOTH"],
            help="卡类型",
        )
        bankcard_group.add_argument(
            "--bankcard-issuer", dest="bankcard_issuer", help="发卡机构"
        )
        bankcard_group.add_argument(
            "--bankcard-bank", dest="bankcard_bank", help="银行代码"
        )
        bankcard_group.add_argument(
            "--bankcard-valid",
            dest="bankcard_valid",
            type=bool,
            default=True,
            help="是否符合Luhn算法",
        )

        # 手机号参数
        phone_group = parser.add_argument_group("手机号选项")
        phone_group.add_argument(
            "--phone-operator",
            dest="phone_operator",
            choices=["MOBILE", "UNICOM", "TELECOM", "VIRTUAL", "ANY"],
            help="运营商",
        )
        phone_group.add_argument(
            "--phone-prefix", dest="phone_prefix", help="号码前缀（逗号分隔）"
        )
        phone_group.add_argument(
            "--phone-valid",
            dest="phone_valid",
            type=bool,
            default=True,
            help="是否生成有效手机号",
        )

        # 年龄参数
        age_group = parser.add_argument_group("年龄选项")
        age_group.add_argument(
            "--age-min", dest="age_min", type=int, default=18, help="最小年龄"
        )
        age_group.add_argument(
            "--age-max", dest="age_max", type=int, default=60, help="最大年龄"
        )

    def run(self, args: Optional[list[str]] = None) -> int:
        """运行CLI"""
        parsed_args = None
        try:
            parsed_args = self.parser.parse_args(args)

            if not parsed_args.command:
                self.parser.print_help()
                return 1

            if parsed_args.command == "generate":
                return self._handle_generate(parsed_args)
            elif parsed_args.command == "list":
                return self._handle_list(parsed_args)
            elif parsed_args.command == "validate":
                return self._handle_validate(parsed_args)
            else:
                self.logger.error(f"未知命令: {parsed_args.command}")
                return 1

        except KeyboardInterrupt:
            self.logger.warning("操作被用户中断")
            return 130
        except Exception as e:
            # 只有当 parsed_args 成功解析时才检查 debug 标志
            if parsed_args and hasattr(parsed_args, "debug") and parsed_args.debug:
                import traceback

                traceback.print_exc()
            else:
                self.logger.error(f"错误: {e}")
            return 1

    def _handle_generate(self, args) -> int:
        """处理generate命令"""
        # 从配置文件或命令行参数构建配置
        if args.config:
            configs = self._load_config_file(args.config)
        else:
            if not args.generators:
                self.logger.error("错误: 必须指定生成器类型或配置文件")
                return 1
            configs = self._build_configs_from_args(args)

        # 检查是否需要使用关联生成
        if len(configs) > 1:
            # 多个生成器，使用关联生成
            results = []
            context = GenerationContext()

            for _ in range(args.count):
                batch_result = default_factory.generate_batch_with_relations(
                    configs, context
                )
                results.append(batch_result)
        else:
            # 单个生成器，使用传统方法
            results = {}
            for config in configs:
                generator = default_factory.create_generator(config)
                data = generator.generate_batch(args.count)
                results[config.generator_type] = data

        # 输出结果
        self._output_results(results, args)
        return 0

    def _handle_list(self, args) -> int:
        """处理list命令"""
        generator_names = default_registry.list_generators()

        self.logger.info("可用的数据生成器:")
        for name in sorted(generator_names):
            # 获取生成器类来显示支持的参数
            try:
                temp_config = GeneratorConfig(generator_type=name, parameters={})
                generator = default_factory.create_generator(temp_config)
                params = ", ".join(generator.supported_parameters)
                self.logger.info(f"  {name:<20} - 参数: {params}")
            except Exception:
                self.logger.info(f"  {name}")

        return 0

    def _handle_validate(self, args) -> int:
        """处理validate命令"""
        try:
            self._load_config_file(args.config_file)
            self.logger.info(f"配置文件 {args.config_file} 验证成功")
            return 0
        except Exception as e:
            self.logger.error(f"配置文件验证失败: {e}")
            return 1

    def _load_config_file(self, config_path: str) -> list[GeneratorConfig]:
        """加载配置文件"""
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        with open(path, encoding="utf-8") as f:
            if path.suffix.lower() in [".yaml", ".yml"]:
                config_data = yaml.safe_load(f)
            else:
                config_data = json.load(f)

        return self.config_parser.parse_config(config_data)

    def _build_configs_from_args(self, args) -> list[GeneratorConfig]:
        """从命令行参数构建配置"""
        configs = []
        generators = args.generators.split(",")

        for gen_type in generators:
            gen_type = gen_type.strip()
            parameters = self._extract_generator_params(args, gen_type)

            config = GeneratorConfig(
                generator_type=gen_type,
                parameters=parameters,
                count=args.count,
                validate=args.validate,
            )
            configs.append(config)

        return configs

    def _extract_generator_params(self, args, gen_type: str) -> dict[str, Any]:
        """提取特定生成器的参数"""
        params = {}
        prefix = f"{gen_type}_"

        for arg_name, arg_value in vars(args).items():
            if arg_name.startswith(prefix) and arg_value is not None:
                param_name = arg_name[len(prefix) :]
                params[param_name] = arg_value

        return params

    def _output_results(self, results, args):
        """输出结果"""
        # 处理不同的结果格式
        if isinstance(results, list):
            # 关联生成的结果格式 - 已经是记录列表
            formatted_data = results
        else:
            # 传统格式 - 转换为记录列表
            formatted_data = []
            max_count = max(len(data) for data in results.values()) if results else 0

            for i in range(max_count):
                record = {}
                for gen_type, data_list in results.items():
                    if i < len(data_list):
                        record[gen_type] = data_list[i]
                formatted_data.append(record)

        # 修复属性访问 - 将点号替换为下划线
        output_format = getattr(args, "output_format", "json")
        output_pretty = getattr(args, "output_pretty", False)
        output_file = getattr(args, "output_file", None)
        output_encoding = getattr(args, "output_encoding", "utf-8")

        formatted_output = self.output_formatter.format(
            formatted_data, format_type=output_format, pretty=output_pretty
        )

        if output_file:
            with open(output_file, "w", encoding=output_encoding) as f:
                f.write(formatted_output)
            self.logger.info(f"结果已保存到: {output_file}")
        else:
            # 输出到标准输出（保留print用于数据输出）
            print(formatted_output)


def main():
    """CLI入口点"""
    cli = DataForgeCLI()
    return cli.run()


def cli():
    """Click CLI入口点"""
    cli_instance = DataForgeCLI()
    return cli_instance.run()


if __name__ == "__main__":
    sys.exit(main())
