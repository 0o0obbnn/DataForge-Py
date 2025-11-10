"""
数据关联性管理器
"""

import logging
import random
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable

from .generator import GenerationContext, GeneratorConfig

logger = logging.getLogger(__name__)


@dataclass
class RelationRule:
    """关联规则定义"""

    source_field: str  # 源字段名
    target_field: str  # 目标字段名
    relation_type: str  # 关联类型：derive, constrain, correlate
    rule_func: Callable[[Any, GenerationContext], Any]  # 关联函数
    priority: int = 0  # 优先级，数字越大优先级越高


class DataRelationManager:
    """数据关联性管理器"""

    def __init__(self):
        self.relation_rules: list[RelationRule] = []
        self._builtin_rules = {}
        self._setup_builtin_rules()

    def _setup_builtin_rules(self):
        """设置内置关联规则"""

        # 身份证 -> 年龄关联
        def idcard_to_age(idcard: str, context: GenerationContext) -> int:
            """从身份证号推导年龄"""
            if len(idcard) == 18 and idcard[:17].isdigit():
                birth_year = int(idcard[6:10])
                current_year = datetime.now().year
                return current_year - birth_year
            return random.randint(18, 60)

        # 身份证 -> 性别关联
        def idcard_to_gender(idcard: str, context: GenerationContext) -> str:
            """从身份证号推导性别"""
            if len(idcard) == 18 and idcard[:17].isdigit():
                gender_digit = int(idcard[16])
                return "MALE" if gender_digit % 2 == 1 else "FEMALE"
            return random.choice(["MALE", "FEMALE"])

        # 身份证 -> 出生日期关联
        def idcard_to_birthdate(idcard: str, context: GenerationContext) -> str:
            """从身份证号推导出生日期"""
            if len(idcard) == 18 and idcard[:17].isdigit():
                birth_str = idcard[6:14]
                return f"{birth_str[:4]}-{birth_str[4:6]}-{birth_str[6:8]}"
            return "1990-01-01"

        # 性别 -> 姓名关联
        def gender_to_name_constraint(
            gender: str, context: GenerationContext
        ) -> dict[str, Any]:
            """性别约束姓名生成"""
            return {"gender": gender}

        # 年龄 -> 身份证关联
        def age_to_idcard_constraint(
            age: int, context: GenerationContext
        ) -> dict[str, Any]:
            """年龄约束身份证生成"""
            current_year = datetime.now().year
            birth_year = current_year - age
            start_date = f"{birth_year}-01-01"
            end_date = f"{birth_year}-12-31"
            return {"birth_date_range": (start_date, end_date)}

        # 地址 -> 身份证地区关联
        def address_to_idcard_region(
            address: str, context: GenerationContext
        ) -> dict[str, Any]:
            """地址约束身份证地区"""
            # 简化实现：从地址中提取省份信息
            province_mapping = {
                "北京": "110000",
                "上海": "310000",
                "广东": "440000",
                "浙江": "330000",
                "江苏": "320000",
            }

            for province, code in province_mapping.items():
                if province in address:
                    return {"region": code}

            return {}

        # 注册内置规则
        self._builtin_rules = {
            ("idcard", "age"): idcard_to_age,
            ("idcard", "gender"): idcard_to_gender,
            ("idcard", "birthdate"): idcard_to_birthdate,
            ("gender", "name"): gender_to_name_constraint,
            ("age", "idcard"): age_to_idcard_constraint,
            ("address", "idcard"): address_to_idcard_region,
        }

    def add_relation_rule(self, rule: RelationRule):
        """添加关联规则"""
        self.relation_rules.append(rule)
        # 按优先级排序
        self.relation_rules.sort(key=lambda r: r.priority, reverse=True)

    def add_builtin_relation(
        self,
        source_field: str,
        target_field: str,
        relation_type: str = "derive",
        priority: int = 0,
    ):
        """添加内置关联规则"""
        rule_key = (source_field, target_field)
        if rule_key in self._builtin_rules:
            rule = RelationRule(
                source_field=source_field,
                target_field=target_field,
                relation_type=relation_type,
                rule_func=self._builtin_rules[rule_key],
                priority=priority,
            )
            self.add_relation_rule(rule)

    def apply_relations(
        self,
        generated_data: dict[str, Any],
        pending_configs: list[GeneratorConfig],
        context: GenerationContext,
    ) -> dict[str, Any]:
        """应用关联规则"""
        result_data = generated_data.copy()

        # 为待生成的字段应用关联规则
        for config in pending_configs:
            target_field = config.generator_type

            # 查找该字段的关联规则
            applicable_rules = [
                rule
                for rule in self.relation_rules
                if rule.target_field == target_field
                and rule.source_field in result_data
            ]

            if applicable_rules:
                # 应用优先级最高的规则
                rule = applicable_rules[0]
                source_value = result_data[rule.source_field]

                try:
                    if rule.relation_type == "derive":
                        # 直接推导目标值
                        derived_value = rule.rule_func(source_value, context)
                        result_data[target_field] = derived_value
                    elif rule.relation_type == "constrain":
                        # 约束目标生成器的参数
                        constraints = rule.rule_func(source_value, context)
                        if isinstance(constraints, dict):
                            config.parameters.update(constraints)
                    elif rule.relation_type == "correlate":
                        # 关联生成
                        correlation_data = rule.rule_func(source_value, context)
                        if isinstance(correlation_data, dict):
                            # 更新上下文的关联数据
                            if context.related_data is None:
                                context.related_data = {}
                            context.related_data.update(correlation_data)

                except Exception as e:
                    # 关联规则执行失败时记录错误但不中断生成
                    logger.warning(
                        f"Relation rule failed for {rule.source_field} -> {rule.target_field}: {e}"
                    )

        return result_data

    def get_relation_dependencies(self, field_names: list[str]) -> list[str]:
        """获取字段的关联依赖顺序"""
        # 构建依赖图
        dependencies = {}
        in_degree = {}

        for field in field_names:
            dependencies[field] = []
            in_degree[field] = 0

        # 构建依赖关系
        for rule in self.relation_rules:
            if rule.target_field in field_names and rule.source_field in field_names:
                dependencies[rule.source_field].append(rule.target_field)
                in_degree[rule.target_field] += 1

        # 拓扑排序（Kahn算法）
        result = []
        queue = [field for field in field_names if in_degree[field] == 0]

        while queue:
            current = queue.pop(0)
            result.append(current)

            for neighbor in dependencies[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # 如果还有剩余字段（存在循环依赖），添加到结果末尾
        remaining = [field for field in field_names if field not in result]
        result.extend(remaining)

        return result


# 全局关联管理器实例
default_relation_manager = DataRelationManager()

# 注册一些默认的关联规则
default_relation_manager.add_builtin_relation("idcard", "age", "derive", priority=10)
default_relation_manager.add_builtin_relation("idcard", "gender", "derive", priority=10)
default_relation_manager.add_builtin_relation(
    "idcard", "birthdate", "derive", priority=10
)
default_relation_manager.add_builtin_relation("gender", "name", "constrain", priority=5)
default_relation_manager.add_builtin_relation("age", "idcard", "constrain", priority=5)
default_relation_manager.add_builtin_relation(
    "address", "idcard", "constrain", priority=3
)
