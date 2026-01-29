"""
DataForge CLI主入口
"""

import sys
from typing import Any

from ..core.factory import default_factory
from ..core.generator import GenerationContext
from ..core.logging_config import get_logger

# 导入CLI模块
from .argparser import CLIArgumentParser
from .commands import handle_list, handle_validate
from .config import build_configs_from_args, load_config_file
from .output import output_results


class DataForgeCLI:
    """DataForge命令行界面"""

    def __init__(self):
        self.parser = CLIArgumentParser.create_parser()
        self.logger = get_logger(self.__class__.__name__)

    def run(self, args: list[str] | None = None) -> int:
        """
        运行CLI

        Args:
            args: 命令行参数列表

        Returns:
            退出码（0表示成功，非0表示失败）
        """
        parsed_args = None
        try:
            parsed_args = self.parser.parse_args(args)

            if not parsed_args.command:
                self.parser.print_help()
                return 1

            if parsed_args.command == "generate":
                return self._handle_generate(parsed_args)
            elif parsed_args.command == "list":
                return handle_list(parsed_args)
            elif parsed_args.command == "validate":
                return handle_validate(parsed_args)
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
        """
        处理generate命令

        Args:
            args: 解析后的命令行参数

        Returns:
            退出码
        """
        # 从配置文件或命令行参数构建配置
        if args.config:
            configs = load_config_file(args.config)
        else:
            if not args.generators:
                self.logger.error("错误: 必须指定生成器类型或配置文件")
                return 1
            configs = build_configs_from_args(args, args.count)

        # 检查是否需要使用关联生成
        results: list[dict[str, Any]] | dict[str, list[dict[str, Any]]]  # type: ignore[assignment]
        if len(configs) > 1:
            # 多个生成器，使用关联生成
            results_list: list[dict[str, Any]] = []
            context = GenerationContext()

            for _ in range(args.count):
                batch_result = default_factory.generate_batch_with_relations(
                    configs, context
                )
                results_list.append(batch_result)
            results = results_list
        else:
            # 单个生成器，使用传统方法
            results_dict: dict[str, list[dict[str, Any]]] = {}
            for config in configs:
                generator = default_factory.create_generator(config)
                data = generator.generate_batch(args.count)
                results_dict[config.generator_type] = data
            results = results_dict

        # 输出结果
        output_results(results, args)
        return 0


def main() -> int:
    """
    CLI入口点

    Returns:
        退出码
    """
    cli = DataForgeCLI()
    return cli.run()


def cli() -> int:
    """
    Click CLI入口点（备用）

    Returns:
        退出码
    """
    cli_instance = DataForgeCLI()
    return cli_instance.run()


if __name__ == "__main__":
    sys.exit(main())
