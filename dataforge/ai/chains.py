"""
LangChain 链封装。

该模块为 DataForge 提供一个轻量级的 LangChain 适配层，用于构建和执行
基于提示模板的数据生成链。当前仅定义骨架，后续将按需扩展。
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class PromptTemplateConfig:
    """提示模板配置。

    Attributes:
        template: 文本模板，使用 {var} 形式的占位符。
        input_variables: 模板中使用的变量名列表。
    """

    template: str
    input_variables: list[str]


class DataGenerationChain:
    """数据生成链的抽象封装。

    该类刻意不直接依赖具体的 LangChain 类型，以降低耦合。
    实际集成时，可以在内部持有 LLM/Chain 实例。
    """

    def __init__(self, llm: Any, prompt_config: PromptTemplateConfig) -> None:
        self._llm = llm
        self._prompt_config = prompt_config

    def _build_prompt(self, variables: Mapping[str, Any]) -> str:
        """根据变量构建最终提示字符串。"""
        missing = [
            name
            for name in self._prompt_config.input_variables
            if name not in variables
        ]
        if missing:
            raise ValueError(f"Missing prompt variables: {', '.join(missing)}")

        return self._prompt_config.template.format(**variables)

    def generate(self, variables: Mapping[str, Any]) -> str:
        """执行一次生成调用。

        当前实现仅假定 `self._llm` 是一个可调用对象，后续可以替换为
        LangChain 的 LLM 或 Chain 实例。
        """
        prompt = self._build_prompt(variables)
        # 这里暂时只定义接口，具体 LangChain 集成在后续阶段实现。
        if not callable(self._llm):
            raise TypeError("LLM backend is not callable")
        result = self._llm(prompt)
        return str(result)

    def generate_batch(self, batch_variables: list[Mapping[str, Any]]) -> list[str]:
        """批量生成数据。

        默认串行实现，后续可以根据需要改为并行或异步。
        """
        results: list[str] = []
        for variables in batch_variables:
            results.append(self.generate(variables))
        return results
