import pytest
from obsidian_assistant.smart_router import SmartRouter

# 使用临时目录构建一个最小 markdown 索引

def test_router_basic_decisions(tmp_path):
    # 创建模拟文档
    (tmp_path / "note1.md").write_text("Obsidian 链接 双向 链接 示例", encoding="utf-8")
    (tmp_path / "note2.md").write_text("任务 管理 看板 标签", encoding="utf-8")

    router = SmartRouter(docs_path=str(tmp_path))

    # 高覆盖：包含多个已存在关键词
    assert router.route("如何使用双向链接") in {"local_only", "hybrid"}

    # 时效性触发
    assert router.route("最新 Obsidian 插件推荐") == "web_first"

    # 低覆盖：未知词触发 web_first
    decision = router.route("飞行汽车量子笔记结构")
    assert decision in {"web_first", "hybrid"}

