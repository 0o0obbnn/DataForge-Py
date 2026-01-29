"""
API常量定义

任务管理和配置相关的常量
"""

# 任务管理相关常量
TASK_KEY_PREFIX = "dataforge:task:"
ALL_TASKS_SORTED_SET = "dataforge:tasks"
TASK_EXPIRATION_SECONDS = 86400  # 24小时

# 批处理相关常量
DEFAULT_BATCH_SIZE = 100
BATCH_DELAY_SECONDS = 0.01  # 批次之间的延迟（10毫秒）
