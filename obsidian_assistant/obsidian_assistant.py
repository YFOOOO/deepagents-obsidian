"""
Obsidian 智能助手 v2.0

集成本地知识库搜索和网页搜索功能，支持引用来源追溯。

功能特性：
- 📚 本地 Obsidian 文档搜索（递归搜索 .md 文件）
- 🌐 网页搜索补充最新信息（Tavily API）
- 🔗 Obsidian 内部链接格式引用 [[路径|名称]]
- 📊 引用来源可追溯性（重要性分级）

作者：DeepAgents Team
版本：2.0
更新日期：2025-11-13
"""

import os
import sys
from pathlib import Path
from typing import Literal, Optional
from langchain_core.tools import tool
from langchain_community.chat_models import ChatTongyi
from tavily import TavilyClient

# 添加 deepagents_official 路径（兼容 exec 和 import 两种方式）
_current_dir = Path(os.getcwd()) if '__file__' not in dir() else Path(__file__).parent
sys.path.insert(0, str(_current_dir / "deepagents_official" / "libs"))
from deepagents import create_deep_agent


# ============================================================================
# 配置常量
# ============================================================================

DEFAULT_DOCS_PATH = "/Users/yf/Documents/Obsidian Vault/我的知识库/Obsidian_Knowledge/obsidian-help-master"
DEFAULT_MODEL = "qwen-turbo"


# ============================================================================
# 工具定义 v2.0
# ============================================================================

def create_search_tool_v2(docs_path: str = DEFAULT_DOCS_PATH):
    """
    创建 v2.0 版本的本地搜索工具（支持路径返回）
    
    Args:
        docs_path: Obsidian 文档根目录路径
        
    Returns:
        LangChain Tool 对象
    """
    
    @tool
    def search_obsidian_docs_v2(query: str, max_results: int = 5) -> str:
        """
        在本地 Obsidian 知识库中搜索相关文档，返回包含文件路径的结果
        
        参数:
            query: 搜索关键词或问题
            max_results: 返回的最大结果数量（默认 5）
            
        返回:
            格式化的搜索结果，包含文档路径、文件名和相关内容片段
        """
        docs_dir = Path(docs_path)
        
        if not docs_dir.exists():
            return f"❌ 错误：文档目录不存在 - {docs_path}"
        
        results = []
        query_lower = query.lower()
        
        # 递归搜索所有 markdown 文件
        for md_file in docs_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                
                # 检查查询关键词是否在文件内容中
                if query_lower in content.lower():
                    # 获取相对路径（相对于根目录）
                    relative_path = md_file.relative_to(docs_dir)
                    
                    # 移除 .md 扩展名用于 Obsidian 链接
                    obsidian_path = str(relative_path).replace('.md', '')
                    
                    # 查找包含关键词的上下文（前后各100个字符）
                    content_lower = content.lower()
                    pos = content_lower.find(query_lower)
                    start = max(0, pos - 100)
                    end = min(len(content), pos + len(query_lower) + 100)
                    snippet = content[start:end].strip()
                    
                    results.append({
                        'file': md_file.name,
                        'path': obsidian_path,  # Obsidian 内部链接路径
                        'snippet': snippet
                    })
                    
                    if len(results) >= max_results:
                        break
            except Exception as e:
                continue
        
        if not results:
            return f"🔍 未找到与 '{query}' 相关的文档"
        
        # 格式化输出结果
        output = f"📚 找到 {len(results)} 个相关文档：\n\n"
        for i, result in enumerate(results, 1):
            output += f"{i}. 【文件】{result['file']}\n"
            output += f"   【路径】{result['path']}\n"
            output += f"   【内容】...{result['snippet']}...\n\n"
        
        return output
    
    return search_obsidian_docs_v2


def create_internet_search_tool_v2():
    """
    创建 v2.0 版本的网页搜索工具（使用 Tavily API）
    
    Returns:
        LangChain Tool 对象
    """
    # 初始化 Tavily 客户端
    tavily_api_key = os.environ.get("TAVILY_API_KEY")
    if not tavily_api_key:
        raise ValueError("❌ 错误：未设置 TAVILY_API_KEY 环境变量")
    
    tavily_client = TavilyClient(api_key=tavily_api_key)
    
    @tool
    def internet_search_v2(
        query: str,
        max_results: int = 3,
        topic: Literal["general", "news"] = "general",
    ) -> dict:
        """
        使用 Tavily 进行网页搜索，获取最新的在线信息
        
        参数:
            query: 搜索查询（如 "Obsidian 最新功能"）
            max_results: 返回最多几条搜索结果（默认 3）
            topic: 搜索主题，"general" 或 "news"
        
        返回:
            包含搜索结果的字典
        """
        search_docs = tavily_client.search(
            query,
            max_results=max_results,
            topic=topic,
        )
        return search_docs
    
    return internet_search_v2


# ============================================================================
# 代理配置 v2.0
# ============================================================================

def create_web_search_agent_v2(internet_search_tool):
    """
    创建 v2.0 版本的网页搜索子代理配置
    
    Args:
        internet_search_tool: 网页搜索工具对象
        
    Returns:
        子代理配置字典
    """
    return {
        "name": "web-search-agent-v2",
        "description": "用于搜索 Obsidian 相关的最新在线信息、社区讨论、插件推荐等。当本地文档信息不够全面或需要最新资讯时调用此代理。",
        "system_prompt": """你是一个专门负责网络搜索的子代理，专注于查找 Obsidian 相关的最新信息。

**触发场景**：
当用户问题包含以下关键词时，你应该被调用：
- "最新"、"最近"、"新版本"、"更新"
- "推荐"、"热门"、"流行"
- "插件"、"主题"、"扩展"
- "社区"、"论坛"、"讨论"
- 或者当本地知识库无法回答问题时

**搜索策略**：
1. 使用 internet_search_v2 工具进行精准搜索
2. 优先搜索官方网站、GitHub、官方论坛等权威来源
3. 对于插件推荐，搜索关键词应包含 "Obsidian plugin"
4. 对于使用技巧，搜索关键词应包含具体功能名称

**返回要求**：
- 提供清晰的搜索结果摘要
- **必须包含网页链接**，格式：`[标题](URL)`
- 标注信息来源的可信度（官方/社区/第三方）
- 如果找到多个来源，按可信度排序

请确保搜索结果准确、及时、有用。
""",
        "tools": [internet_search_tool]
    }


# ============================================================================
# 主代理系统提示词 v2.0
# ============================================================================

OBSIDIAN_ASSISTANT_PROMPT_V2 = """你是一个专业的 Obsidian 使用助手。你的任务是帮助用户解决 Obsidian 相关的问题。

**核心规则**：
1. 优先使用 search_obsidian_docs_v2 工具搜索本地知识库
2. 如果本地文档无法解决问题，使用 web-search-agent-v2 子代理进行网络搜索
3. **必须在回答中添加引用来源**

**引用格式要求**：
- 对于本地文档：使用 Obsidian 内部链接格式 `[[路径|显示名称]]`
  例如：`[[Editing and formatting/Basic formatting syntax|基础格式化语法]]`
- 对于网页来源：使用标准 Markdown 链接 `[显示文本](URL)`
  例如：`[Obsidian 官网](https://obsidian.md)`
- **引用位置**：
  - **必需**：在回答末尾添加"参考来源"章节，列出所有引用
  - **推荐**：在具体知识点后直接标注来源，格式如 `（参考：[[路径|文件名]]）`
  - **可选**：对于复杂回答，在引用列表中标注重要程度（⭐⭐⭐ 核心参考，⭐⭐ 补充阅读）

**引用示例**：
```
### 如何创建链接

1. **内部链接**：使用双方括号 `[[]]` 包裹笔记名称（参考：[[Linking notes and files/Internal links|内部链接]]）
2. **外部链接**：使用 Markdown 格式 `[文本](URL)`（参考：[[Editing and formatting/Basic formatting syntax|基础格式化语法]]）

### 参考来源
⭐⭐⭐ [[Linking notes and files/Internal links|内部链接]] - 核心参考
⭐⭐ [[Editing and formatting/Basic formatting syntax|基础格式化语法]] - 补充阅读
```

**特殊情况**：
- 如果需要引用文档中的特定段落，可以使用引用块格式：
  ```
  > 原文：「在 Obsidian 中，双向链接是核心功能...」
  > 
  > 来源：[[Linking notes and files/Internal links|内部链接]]
  ```

请始终以专业、准确、结构化的方式回答问题，并确保每个回答都包含清晰的引用来源。
"""


# ============================================================================
# 主函数：创建 Obsidian 助手 v2.0
# ============================================================================

def create_obsidian_assistant_v2(
    docs_path: str = DEFAULT_DOCS_PATH,
    model_name: str = DEFAULT_MODEL,
    api_key: Optional[str] = None
):
    """
    创建 Obsidian 智能助手 v2.0
    
    集成了本地知识库搜索、网页搜索和引用功能。
    
    Args:
        docs_path: Obsidian 文档根目录路径
        model_name: 使用的模型名称（默认 qwen-turbo）
        api_key: API Key（如果未设置则从环境变量读取）
        
    Returns:
        CompiledStateGraph: 可以直接调用的助手代理
        
    Example:
        ```python
        # 创建助手
        assistant = create_obsidian_assistant_v2()
        
        # 提问
        result = assistant.invoke({
            "messages": [("user", "如何创建链接？")]
        })
        
        # 查看结果
        from utils import display_agent_execution
        display_agent_execution(result)
        ```
    """
    
    # 验证环境变量
    if api_key:
        os.environ["DASHSCOPE_API_KEY"] = api_key
    
    dashscope_key = os.environ.get("DASHSCOPE_API_KEY")
    tavily_key = os.environ.get("TAVILY_API_KEY")
    
    if not dashscope_key:
        raise ValueError("❌ 错误：未设置 DASHSCOPE_API_KEY 环境变量")
    if not tavily_key:
        raise ValueError("❌ 错误：未设置 TAVILY_API_KEY 环境变量")
    
    # 验证文档路径
    if not Path(docs_path).exists():
        raise ValueError(f"❌ 错误：文档路径不存在 - {docs_path}")
    
    print("🔧 正在创建 Obsidian 助手 v2.0...")
    
    # 1. 创建模型
    print(f"  ✓ 初始化模型: {model_name}")
    model = ChatTongyi(model=model_name)
    
    # 2. 创建工具
    print(f"  ✓ 创建搜索工具（文档路径: {docs_path}）")
    search_tool_v2 = create_search_tool_v2(docs_path)
    internet_search_tool_v2 = create_internet_search_tool_v2()
    
    # 3. 创建子代理
    print("  ✓ 配置网页搜索子代理")
    web_agent_v2 = create_web_search_agent_v2(internet_search_tool_v2)
    
    # 4. 创建主代理
    print("  ✓ 组装主代理...")
    assistant = create_deep_agent(
        model=model,
        tools=[search_tool_v2],
        subagents=[web_agent_v2],
        system_prompt=OBSIDIAN_ASSISTANT_PROMPT_V2
    )
    
    print("✅ Obsidian 助手 v2.0 创建成功！\n")
    print("📋 配置信息：")
    print(f"  - 模型: ChatTongyi ({model_name})")
    print(f"  - 搜索工具: search_obsidian_docs_v2（支持路径返回）")
    print(f"  - 子代理: web-search-agent-v2（增强触发逻辑）")
    print(f"  - 引用格式: Obsidian 内部链接 + 网页链接")
    print(f"  - 文档路径: {docs_path}\n")
    
    return assistant


# ============================================================================
# 便捷函数
# ============================================================================

def quick_ask(question: str, assistant=None, docs_path: str = DEFAULT_DOCS_PATH):
    """
    快速提问（用于测试）
    
    Args:
        question: 用户问题
        assistant: 助手实例（如果为 None 则自动创建）
        docs_path: 文档路径
        
    Returns:
        Agent 执行结果
    """
    if assistant is None:
        assistant = create_obsidian_assistant_v2(docs_path=docs_path)
    
    result = assistant.invoke({
        "messages": [("user", question)]
    })
    
    return result


def get_final_answer(result) -> str:
    """
    从结果中提取最终答案
    
    Args:
        result: Agent 执行结果
        
    Returns:
        最终答案字符串
    """
    from utils import extract_final_answer
    return extract_final_answer(result)


# ============================================================================
# 主程序入口（测试用）- 已注释以避免导入时执行
# ============================================================================

# 注意：使用 exec() 或 import 导入时，以下代码不会自动执行
# 如需测试，请直接运行: python obsidian_assistant.py

# if __name__ == "__main__":
#     from dotenv import load_dotenv
#     from utils import display_agent_execution, extract_final_answer
#     
#     # 加载环境变量
#     load_dotenv()
#     
#     print("=" * 80)
#     print("🚀 Obsidian 智能助手 v2.0 - 测试模式")
#     print("=" * 80)
#     print()
#     
#     # 创建助手
#     assistant = create_obsidian_assistant_v2()
#     
#     # 测试问题
#     test_questions = [
#         "如何在 Obsidian 中使用标签功能？",
#         "推荐一些最新的 Obsidian 插件",
#         "Canvas 功能是什么？如何使用？"
#     ]
#     
#     for i, question in enumerate(test_questions, 1):
#         print(f"\n{'=' * 80}")
#         print(f"📝 测试 {i}: {question}")
#         print(f"{'=' * 80}\n")
#         
#         result = assistant.invoke({
#             "messages": [("user", question)]
#         })
#         
#         # 展示完整流程
#         display_agent_execution(result)
#         
#         # 提取最终答案
#         print(f"\n{'─' * 80}")
#         print("💡 最终答案：")
#         print(f"{'─' * 80}\n")
#         print(extract_final_answer(result))
#         
#         print("\n" + "=" * 80 + "\n")
