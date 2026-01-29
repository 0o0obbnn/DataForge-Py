"""
命令行参数解析器模块

负责创建和配置argparse.ArgumentParser
"""

import argparse


class CLIArgumentParser:
    """CLI参数解析器"""

    @staticmethod
    def create_parser() -> argparse.ArgumentParser:
        """
        创建命令行参数解析器

        Returns:
            配置好的ArgumentParser实例
        """
        parser = argparse.ArgumentParser(
            prog="dataforge",
            description="DataForge - 高效、灵活的测试数据生成工具",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
示例用法:
  # 生成10个身份证号
  dataforge generate idcard --count 10

  # 生成银行卡号并输出为JSON
  dataforge generate bankcard --count 5 --output-format json

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
        CLIArgumentParser._add_generate_args(generate_parser)

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

    @staticmethod
    def _add_generate_args(parser: argparse.ArgumentParser) -> None:
        """
        添加generate命令的参数

        Args:
            parser: generate子命令的解析器
        """
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

        # 车牌参数
        license_group = parser.add_argument_group("车牌选项")
        license_group.add_argument(
            "--license-plate-type",
            dest="license_plate_type",
            choices=["FUEL", "NEW_ENERGY", "BOTH"],
            help="车牌类型",
        )
        license_group.add_argument(
            "--license-plate-province",
            dest="license_plate_province",
            help="省份简称（如 京/沪/粤）",
        )
        license_group.add_argument(
            "--license-plate-city",
            dest="license_plate_city",
            help="城市字母代码（如 A/B）",
        )
        license_group.add_argument(
            "--license-plate-include-io",
            dest="license_plate_include_io",
            type=bool,
            default=False,
            help="是否包含 I 和 O 字母",
        )
        license_group.add_argument(
            "--license-plate-valid",
            dest="license_plate_valid",
            type=bool,
            default=True,
            help="是否生成有效车牌",
        )

        # 年龄参数
        age_group = parser.add_argument_group("年龄选项")
        age_group.add_argument(
            "--age-min", dest="age_min", type=int, default=18, help="最小年龄"
        )
        age_group.add_argument(
            "--age-max", dest="age_max", type=int, default=60, help="最大年龄"
        )
