import os
import pathlib
import pytest

DASH = os.getenv("DASHSCOPE_API_KEY")
TAVILY = os.getenv("TAVILY_API_KEY")
pytestmark = pytest.mark.skipif(not (DASH and TAVILY), reason="API keys not set; skip")

from obsidian_assistant import create_obsidian_assistant_v2

TEST_DOCS_PATH = "/tmp/mini_vault"

@pytest.fixture(scope="session", autouse=True)
def prepare_docs():
    root = pathlib.Path(TEST_DOCS_PATH)
    root.mkdir(parents=True, exist_ok=True)
    # create a tiny markdown file to allow local_only route possibility later
    (root / "note.md").write_text("This is a test note about Obsidian caching and compression.")
    return root

def test_cache_second_hit(prepare_docs):
    assistant = create_obsidian_assistant_v2(docs_path=str(prepare_docs), enable_cache=True, enable_model_adapter=False, enable_smart_routing=False, verbose=False)
    q = "什么是缓存？"
    r1 = assistant.invoke({"messages": [("user", q)]})
    assert not r1.get("cache_hit")
    r2 = assistant.invoke({"messages": [("user", q)]})
    assert r2.get("cache_hit")


def test_compression_flag(prepare_docs):
    assistant = create_obsidian_assistant_v2(docs_path=str(prepare_docs), enable_compression=True, enable_model_adapter=False, enable_smart_routing=False, verbose=False)
    q = "请生成一个非常详细并且很长的说明文本以测试压缩功能，包含多个段落和大量描述。"
    r = assistant.invoke({"messages": [("user", q)]})
    comp = r.get("compression")
    assert comp is not None
    assert "applied" in comp
