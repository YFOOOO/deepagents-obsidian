import pytest
from obsidian_assistant.model_adapters import get_model_adapter

@pytest.mark.parametrize("model_name", ["qwen-turbo", "deepseek-chat", "unknown-model"])
def test_adapter_enhance_system_prompt(model_name):
    adapter = get_model_adapter(model_name)
    base_prompt = "BASE"
    tools_desc = "t1: tool one; t2: tool two"
    enhanced = adapter.enhance_system_prompt(base_prompt, tools_desc)
    assert isinstance(enhanced, str)
    assert len(enhanced) >= len(base_prompt)

