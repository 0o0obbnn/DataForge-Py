"""
CLI输出处理模块

处理结果格式化和输出
"""

from ..core.logging_config import get_logger
from ..output.formatter import OutputFormatter

logger = get_logger(__name__)
output_formatter = OutputFormatter()


def output_results(results, args):
    """
    输出结果

    Args:
        results: 生成结果（可能是dict或list）
        args: 命令行参数
    """
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
    output = getattr(args, "output_pretty", False)
    output_file = getattr(args, "output_file", None)
    output_encoding = getattr(args, "output_encoding", "utf-8")

    formatted_output = output_formatter.format(
        formatted_data, format_type=output_format, pretty=output
    )

    if output_file:
        with open(output_file, "w", encoding=output_encoding) as f:
            f.write(formatted_output)
        logger.info(f"结果已保存到: {output_file}")
    else:
        # 输出到标准输出（（保留print用于数据输出）
        print(formatted_output)
