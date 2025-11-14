"""Model Adapter Skeleton for Obsidian Assistant V2.1

Provides a pluggable abstraction to customize system prompt and user message
handling for different LLM providers (Qwen, DeepSeek, etc.).

Design Goals:
- Keep core interface minimal and extensible.
- Allow per-model injection of behavioral constraints (tool usage order,
  language preferences, brevity hints, reasoning control).
- Provide safe fallbacks so unsupported models degrade gracefully.

Public API:
- BaseAdapter: Default no-op implementation.
- QwenAdapter: Enforces "tool first, then answer" pattern and Chinese locale bias.
- DeepSeekAdapter: Encourages concise multi-step reasoning and limits redundant tool usage.
- get_model_adapter(model_name: str) -> BaseAdapter: Factory selector.

Future Extension Points:
- parse_tool_calls: For custom tool call syntaxes (XML / JSON tags) if needed.
- add validation / normalization of tool parameter values.
- integrate telemetry hooks (e.g., counting missed tool opportunities).
"""
from __future__ import annotations
from typing import List, Optional
import re

# ---------------------------------------------------------------------------
# Base Adapter
# ---------------------------------------------------------------------------
class BaseAdapter:
    """Default adapter: passes through prompt and message unchanged.

    Subclasses should override methods selectively. Each method returns a new
    string; original content should be preserved unless modification is required.
    """

    name: str = "base"

    def enhance_system_prompt(self, base: str, tool_descriptions: str) -> str:
        """Return enhanced system prompt.

        Parameters:
            base: Original prompt text.
            tool_descriptions: A joined textual description of tools accessible.
        """
        parts = [base.strip()]
        if tool_descriptions:
            parts.append(f"\n\n# 可用工具列表\n{tool_descriptions.strip()}")
        return "\n".join(parts)

    def enhance_user_message(self, message: str, may_need_tools: bool) -> str:
        """Optionally augment user message before sending to the model.

        Parameters:
            message: Original user text.
            may_need_tools: Heuristic flag indicating tool use likely.
        """
        return message

    def parse_tool_calls(self, response: str) -> List[dict]:
        """Parse tool call directives from model raw response.

        Base skeleton returns empty list. Future: implement regex/XML/JSON parsing.
        """
        return []

    def message_requires_tools(self, message: str) -> bool:
        """Simple heuristic: detect search / update / latest style intents.
        Can be overridden for model-specific nuance.
        """
        triggers = ["搜索", "search", "最新", "推荐", "update", "修改", "查找", "总结", "分析"]
        lowered = message.lower()
        return any(t in lowered for t in triggers)

# ---------------------------------------------------------------------------
# Qwen Adapter
# ---------------------------------------------------------------------------
class QwenAdapter(BaseAdapter):
    name: str = "qwen"

    def enhance_system_prompt(self, base: str, tool_descriptions: str) -> str:
        addon = (
            "\n\n## Qwen 专用执行规范\n"
            "1. 如涉及信息检索或需要外部/本地内容, 必须先调用相关工具再回答。\n"
            "2. 严禁在跳过必要搜索时直接给出最终总结。\n"
            "3. 本地知识库优先; 只有命中时效/推荐类关键词再触发网页搜索。\n"
            "4. 避免连续相同类型工具重复调用, 增量补充必须说明目的。\n"
            "5. 输出保持结构化: 使用分级标题与引用来源列表。\n"
            "6. 默认以用户语言(若含中文字符则中文优先)进行回答。"
        )
        return super().enhance_system_prompt(base + addon, tool_descriptions)

    def enhance_user_message(self, message: str, may_need_tools: bool) -> str:
        if may_need_tools and self.message_requires_tools(message):
            hint = (
                "\n\n[指令提示-Qwen]: 请先列出需要调用的工具计划(若需要), 然后执行工具, 获得结果后再总结。"
            )
            return message + hint
        return message

# ---------------------------------------------------------------------------
# DeepSeek Adapter
# ---------------------------------------------------------------------------
class DeepSeekAdapter(BaseAdapter):
    name: str = "deepseek"

    def enhance_system_prompt(self, base: str, tool_descriptions: str) -> str:
        addon = (
            "\n\n## DeepSeek 专用执行规范\n"
            "1. 复杂问题分步处理: 每步仅在必要时调用 1~2 个工具。\n"
            "2. 工具调用后暂停, 不要立即产出整篇最终答案, 先评估是否需要继续。\n"
            "3. 避免冗长自我思考输出, 简洁说明调用原因。\n"
            "4. 不臆造参数 (时间范围/文件路径), 无法确认则通过本地搜索/结构化工具获取。\n"
            "5. 若连续两步没有新增信息, 建议结束工具调用并总结。"
        )
        return super().enhance_system_prompt(base + addon, tool_descriptions)

    def enhance_user_message(self, message: str, may_need_tools: bool) -> str:
        if may_need_tools and self.message_requires_tools(message):
            hint = (
                "\n\n[指令提示-DeepSeek]: 采用小步迭代, 每次仅必要工具, 工具结果出来后再决定是否继续。"
            )
            return message + hint
        return message

# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------
_ADAPTER_MAP = {
    "qwen": QwenAdapter,
    "tongyi": QwenAdapter,  # 通义生态别名
    "deepseek": DeepSeekAdapter,
}

def get_model_adapter(model_name: Optional[str]) -> BaseAdapter:
    """Return adapter instance based on model name substring matching.

    Fallback to BaseAdapter if no specific implementation is available.
    """
    if not model_name:
        return BaseAdapter()
    lowered = model_name.lower()
    for key, cls in _ADAPTER_MAP.items():
        if key in lowered:
            return cls()
    return BaseAdapter()

__all__ = [
    "BaseAdapter",
    "QwenAdapter",
    "DeepSeekAdapter",
    "get_model_adapter",
]
