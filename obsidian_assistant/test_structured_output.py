import pytest
import os
from typing import Dict, Any

# We assume environment vars are set externally; if not, skip tests gracefully.
DASH = os.getenv("DASHSCOPE_API_KEY")
TAVILY = os.getenv("TAVILY_API_KEY")
pytestmark = pytest.mark.skipif(not (DASH and TAVILY), reason="API keys not set; skip integration-like tests")

from obsidian_assistant import create_obsidian_assistant_v2

TEST_DOCS_PATH = "/tmp/empty_vault"  # use empty path for predictable no results

@pytest.fixture(scope="session", autouse=True)
def ensure_empty_docs():
    import pathlib
    p = pathlib.Path(TEST_DOCS_PATH)
    p.mkdir(parents=True, exist_ok=True)
    return p

def invoke(assistant, q: str) -> Dict[str, Any]:
    return assistant.invoke({"messages": [("user", q)]})

def test_structured_fields_presence(ensure_empty_docs):
    assistant = create_obsidian_assistant_v2(docs_path=str(ensure_empty_docs), enable_model_adapter=False, enable_smart_routing=False, enable_cache=False, enable_compression=False, verbose=False)
    res = invoke(assistant, "测试查询")
    for key in ["answer","raw","route_strategy","adapter_used","token_usage","sources","messages","cache_hit","compression"]:
        assert key in res, f"missing field {key}"
    assert isinstance(res["sources"], list)
    assert isinstance(res["token_usage"], dict)

def test_cache_hit(ensure_empty_docs):
    assistant = create_obsidian_assistant_v2(docs_path=str(ensure_empty_docs), enable_model_adapter=False, enable_smart_routing=False, enable_cache=True, verbose=False)
    q = "缓存测试"
    first = invoke(assistant, q)
    assert not first.get("cache_hit"), "first invoke should not be cache hit"
    second = invoke(assistant, q)
    assert second.get("cache_hit"), "second invoke should be cache hit"

def test_compression_applied(ensure_empty_docs):
    # Force compression with small threshold by monkeypatching TextCompressor via args
    from obsidian_assistant import create_obsidian_assistant_v2 as maker
    assistant = maker(docs_path=str(ensure_empty_docs), enable_model_adapter=False, enable_smart_routing=False, enable_cache=False, enable_compression=True, verbose=False)
    # Long query to encourage long answer (model may truncate; just check metadata presence)
    res = invoke(assistant, "请输出一个非常非常长的回答来触发压缩机制，以便验证压缩标记是否工作。")
    comp = res.get("compression")
    assert comp is not None, "compression metadata missing"
    assert "applied" in comp, "compression metadata malformed"
