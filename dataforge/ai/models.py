"""
AI 模型管理器。

该模块负责管理本地与云端大语言模型实例，为上层生成器提供统一接口。
当前仅实现基础骨架，后续阶段将逐步接入具体模型（Ollama、Transformers、OpenAI 等）。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class ModelUnavailableError(RuntimeError):
    """单个模型不可用时抛出。"""


class AllModelsUnavailableError(RuntimeError):
    """所有候选模型均不可用时抛出。"""


@dataclass(slots=True)
class ModelConfig:
    """模型配置。

    Attributes:
        name: 模型名称（如 \"qwen2.5\", \"gpt-4\"）。
        provider: 提供方标识（local、ollama、transformers、openai、anthropic 等）。
        endpoint: 可选的远端地址或本地路径。
    """

    name: str
    provider: str = "local"
    endpoint: str | None = None


class AIModelManager:
    """AI 模型管理器。

    统一管理本地与云端模型的生命周期，提供按名称/提供方检索模型的能力。
    目前仅提供接口和基础结构，实际加载逻辑将在后续阶段接入。
    """

    def __init__(self) -> None:
        self._models: dict[str, Any] = {}
        self._configs: dict[str, ModelConfig] = {}
        self._default_model: str | None = None

    def register_model(self, config: ModelConfig, instance: Any) -> None:
        """注册一个已经初始化完成的模型实例。

        Args:
            config: 模型配置。
            instance: 已初始化完成的模型对象（如 LangChain LLM）。
        """
        key = self._make_key(config.name, config.provider)
        self._models[key] = instance
        self._configs[key] = config
        if self._default_model is None:
            self._default_model = key

    def get_model(
        self, name: str | None = None, provider: str | None = None
    ) -> Any:
        """根据名称与提供方获取模型实例。

        如果未显式指定，则返回默认模型。
        """
        if name is None and provider is None:
            if self._default_model is None:
                raise AllModelsUnavailableError("No default AI model registered")
            key = self._default_model
        else:
            key = self._make_key(name or "", provider or "local")

        try:
            return self._models[key]
        except KeyError as exc:
            raise ModelUnavailableError(f"AI model not available: {key}") from exc

    def get_model_with_fallback(self, candidates: list[ModelConfig]) -> Any:
        """按候选顺序获取第一个可用模型。

        Args:
            candidates: 按优先级排序的候选模型配置列表。

        Raises:
            AllModelsUnavailableError: 所有候选模型均不可用。
        """
        last_error: Exception | None = None
        for config in candidates:
            key = self._make_key(config.name, config.provider)
            try:
                return self._models[key]
            except KeyError as exc:
                last_error = exc
                continue

        raise AllModelsUnavailableError(
            "No AI models available from candidates"
        ) from last_error

    @staticmethod
    def _make_key(name: str, provider: str) -> str:
        return f"{provider}:{name}"
