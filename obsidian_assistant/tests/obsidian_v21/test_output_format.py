import pytest
from obsidian_assistant.obsidian_assistant import create_obsidian_assistant_v2

@pytest.mark.skip(reason="Requires real model & env keys; remove skip when keys available")
def test_structured_output_keys():
    assistant = create_obsidian_assistant_v2(enable_model_adapter=True, enable_smart_routing=True)
    result = assistant.invoke({"messages": [("user", "如何创建链接？")]})
    assert isinstance(result, dict)
    expected = [
        "answer", "raw", "route_strategy", "route_coverage", "time_sensitive",
        "adapter_used", "token_usage", "sources", "messages"
    ]
    for key in expected:
        assert key in result, f"missing key: {key}"
    assert isinstance(result["token_usage"], (dict, object))
    assert isinstance(result["sources"], list)

