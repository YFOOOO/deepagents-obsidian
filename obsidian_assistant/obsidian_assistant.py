# 辅助函数：生成 Obsidian 内部链接格式
def format_note_reference(note_path: str, note_title: str) -> str:
    """
    生成 Obsidian 内部链接格式
    Args:
        note_path: 笔记相对路径，如 "Obsidian_Knowledge/欢迎.md"
        note_title: 显示标题，如 "欢迎"
    Returns:
        格式化的内部链接，如 "[[Obsidian_Knowledge/欢迎|欢迎]]"
    """
    clean_path = note_path.replace('.md', '')
    return f"[[{clean_path}|{note_title}]]"

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
import json
from pathlib import Path
from typing import Literal, Optional, Dict, Any
from langchain_core.tools import tool
from langchain_community.chat_models import ChatTongyi
from tavily import TavilyClient
from deepagents import create_deep_agent
try:
    from token_counter import TokenCounter, count_tokens_for_result
except ImportError:
    class TokenCounter:  # type: ignore
        def __init__(self, model: str = "qwen-turbo"): self.model = model
        def start_counting(self): pass
    def count_tokens_for_result(question: str, result: Dict[str, Any], counter: TokenCounter):  # type: ignore
        pt = len(question)//4; ct = len(str(result))//16
        return {"question": question, "prompt_tokens": pt, "completion_tokens": ct, "total_tokens": pt+ct, "model": counter.model, "cost": 0.0}
try:
    from model_adapters import get_model_adapter
except ImportError:
    def get_model_adapter(_name: Optional[str]):
        class _Dummy:
            def enhance_system_prompt(self, base: str, tool_descriptions: str) -> str: return base
            def enhance_user_message(self, msg: str, may_need_tools: bool) -> str: return msg
        return _Dummy()
try:
    from smart_router import create_smart_router, SmartRouter
except ImportError:
    SmartRouter = None
    def create_smart_router(_path: str): return None
try:
    from cache_layer import SimpleQueryCache, TextCompressor
except ImportError:
    SimpleQueryCache = None  # type: ignore
    TextCompressor = None  # type: ignore

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
            JSON 格式的搜索结果，包含状态、消息和文档列表
        """
        # 🔍 调试日志：工具被调用
        print(f"🔍 [search_obsidian_docs_v2] 工具被调用")
        print(f"   查询: '{query}'")
        print(f"   最大结果数: {max_results}")
        
        docs_dir = Path(docs_path)
        print(f"   搜索目录: {docs_dir}")
        print(f"   目录存在: {docs_dir.exists()}")
        
        if not docs_dir.exists():
            return json.dumps({
                "status": "error",
                "message": f"❌ 错误：文档目录不存在 - {docs_path}",
                "results": []
            }, ensure_ascii=False)
        
        results = []
        query_lower = query.lower()
        
        # 🔍 调试日志：开始搜索
        all_md_files = list(docs_dir.rglob("*.md"))
        print(f"   📄 .md 文件总数: {len(all_md_files)}")
        print(f"   🔎 搜索关键词: '{query_lower}'")
        
        # 递归搜索所有 markdown 文件
        searched_count = 0
        for md_file in all_md_files:
            searched_count += 1
            try:
                content = md_file.read_text(encoding='utf-8')
                # 检查查询关键词是否在文件内容中
                if query_lower in content.lower():
                    # 获取相对路径（相对于根目录）
                    relative_path = md_file.relative_to(docs_dir)
                    obsidian_path = str(relative_path)
                    # 查找包含关键词的上下文（前后各100个字符）
                    content_lower = content.lower()
                    pos = content_lower.find(query_lower)
                    start = max(0, pos - 100)
                    end = min(len(content), pos + len(query_lower) + 100)
                    snippet = content[start:end].strip()
                    # 使用 format_note_reference 生成内部链接
                    note_link = format_note_reference(obsidian_path, md_file.stem)
                    results.append({
                        'file': md_file.name,
                        'path': obsidian_path.replace('.md', ''),
                        'snippet': snippet,
                        'note_link': note_link
                    })
                    if len(results) >= max_results:
                        break
            except Exception:
                continue
        
        # 🔍 调试日志：搜索完成
        print(f"   ✅ 搜索完成: 检查了 {searched_count} 个文件，找到 {len(results)} 个结果")
        
        if not results:
            return json.dumps({
                "status": "no_results",
                "message": f"🔍 未找到与「{query}」相关的文档。建议：1) 尝试其他关键词 2) 使用网络搜索获取最新信息",
                "query": query,
                "results": []
            }, ensure_ascii=False)
        
        # 返回结构化结果
        return json.dumps({
            "status": "success",
            "query": query,
            "count": len(results),
            "message": f"📚 找到 {len(results)} 个相关文档",
            "results": results
        }, ensure_ascii=False, indent=2)
    
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
        # 🌐 调试日志：网络搜索被调用
        print(f"🌐 [internet_search_v2] 工具被调用")
        print(f"   查询: '{query}'")
        print(f"   最大结果: {max_results}, 主题: {topic}")
        
        search_docs = tavily_client.search(
            query,
            max_results=max_results,
            topic=topic,
        )
        
        print(f"   ✅ 网络搜索完成: 返回 {len(search_docs.get('results', []))} 个结果")
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

**🚨 核心约束（必须严格遵守）**：

1. **真实性原则 - 禁止编造内容**：
   - ❌ **绝对禁止**编造不存在的文件名、路径或文档
   - ❌ **绝对禁止**引用工具未返回的任何路径或链接
   - ✅ **只能引用** search_obsidian_docs_v2 或 internet_search_v2 工具实际返回的内容

2. **工具使用规范**：
   - 第一步：使用 search_obsidian_docs_v2 搜索本地知识库
   - 如果本地搜索返回空结果或"未找到"，必须：
     a) 明确告知用户"本地文档中未找到相关内容"
     b) 询问是否需要搜索网络获取信息
   - 只有在用户同意或明确需要最新信息时，才使用 internet_search_v2

3. **引用格式严格要求**：
   - 本地文档：`[[工具返回的完整路径|显示名称]]`
   - 网页来源：`[标题](工具返回的完整URL)`
   - 每个引用必须对应工具的实际返回结果

**正确示例**（Few-shot）：

**示例 1 - 本地文档有结果**：
```
工具返回：
{
  "results": [
    {"path": "Linking notes and files/Internal links", "title": "内部链接", "snippet": "...双方括号..."}
  ]
}

正确回答：
在 Obsidian 中创建内部链接非常简单，使用双方括号 `[[]]` 即可。

例如：`[[我的笔记]]` 会创建指向"我的笔记"的链接。

**参考来源**：
- [[Linking notes and files/Internal links|内部链接]]
```

**示例 2 - 本地文档无结果**：
```
工具返回：
{
  "status": "no_results",
  "message": "未找到相关文档"
}

正确回答：
抱歉，我在您的本地 Obsidian 文档中未找到关于「内部链接」的相关内容。

我可以：
1. 🌐 搜索网络获取 Obsidian 官方文档
2. 💡 基于 Obsidian 的通用知识为您解答

您希望我采取哪种方式？
```

**示例 3 - 错误示范（禁止模仿）**：
```
❌ 错误：编造不存在的路径
"根据 [[笔记/内部链接教程|内部链接教程]] 所述..."
（如果工具未返回这个路径，这就是编造）

❌ 错误：本地无结果时继续详细回答并假装有引用
工具返回空 → 仍然回答"根据 [[某某文档]] ..."

✅ 正确：明确告知无结果，询问下一步
```

**引用格式模板**：
```
### 问题解答

[具体回答内容]（参考：[[工具返回的路径|显示名称]]）

### 参考来源
⭐⭐⭐ [[路径1|标题1]] - 核心参考
⭐⭐ [[路径2|标题2]] - 补充阅读
```

**特殊情况处理**：
- 如果用户问题超出本地文档范围，诚实告知并建议网络搜索
- 如果需要引用网页，必须使用 internet_search_v2 获取真实URL
- 不要凭空推测或编造任何文档路径

请始终以专业、准确、诚实的方式回答问题，确保每个引用都对应工具的实际返回结果。
"""


# ============================================================================
# 主函数：创建 Obsidian 助手 v2.0
# ============================================================================

def create_obsidian_assistant_v2(
    docs_path: str = DEFAULT_DOCS_PATH,
    model_name: str = DEFAULT_MODEL,
    api_key: Optional[str] = None,
    enable_model_adapter: bool = True,
    enable_smart_routing: bool = False,
    enable_cache: bool = False,
    cache_max_items: int = 256,
    enable_compression: bool = False,
    verbose: Optional[bool] = None,
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
    
    # 精简日志输出
    if verbose is None:
        env_flag = os.getenv("OBSIDIAN_ASSISTANT_VERBOSE") or os.getenv("DEEPAGENTS_VERBOSE")
        if env_flag and str(env_flag).lower() not in {"0", "false", "no"}:
            verbose = True
        else:
            verbose = False
    if verbose:
        print(f"🔧 构建 Obsidian 助手 v2.0 model={model_name} docs={docs_path} cache={enable_cache} compression={enable_compression}")
    # 1. 创建模型
    model = ChatTongyi(model=model_name)
    
    # 2. 创建工具
    # 创建工具（省略详细日志）
    search_tool_v2 = create_search_tool_v2(docs_path)
    internet_search_tool_v2 = create_internet_search_tool_v2()
    
    # 3. 创建子代理
    # 配置网页搜索子代理
    web_agent_v2 = create_web_search_agent_v2(internet_search_tool_v2)
    
    # 4. 创建主代理
    # 组装主代理
    # 5. 模型适配器处理系统提示词 (V2.1 骨架)
    system_prompt_final = OBSIDIAN_ASSISTANT_PROMPT_V2
    adapter = None
    if enable_model_adapter:
        adapter = get_model_adapter(model_name)
        tool_desc = "search_obsidian_docs_v2: 本地文档检索; internet_search_v2: 网页搜索 (Tavily)"
        system_prompt_final = adapter.enhance_system_prompt(system_prompt_final, tool_desc)

    router = None
    routing_note = ""
    if enable_smart_routing:
        router = create_smart_router(docs_path)
        routing_note = (
            "\n\n## 智能路由策略 (启用)\n"
            "- local_only: 高覆盖率时仅本地搜索\n"
            "- hybrid: 中等覆盖率 → 先本地后按需网页补充\n"
            "- web_first: 低覆盖或命中时效关键词 → 直接网页搜集信息\n"
            "(内部将根据查询关键词与覆盖率自动选择策略)"
        )
        system_prompt_final += routing_note

    assistant = create_deep_agent(
        model=model,
        tools=[search_tool_v2],
        subagents=[web_agent_v2],
        system_prompt=system_prompt_final,
    )
    
    if verbose:
        print(f"✅ 助手就绪 adapter={adapter.__class__.__name__ if adapter else 'none'} routing={'on' if enable_smart_routing else 'off'} cache={'on' if enable_cache else 'off'} compression={'on' if enable_compression else 'off'}")
    
    # 包装一次调用接口，若启用路由则在 messages 前添加策略注释
    # ---------------- Structured invoke wrapper (V2.1 enhancement) -----------------
    original_invoke = assistant.invoke
    token_counter = TokenCounter(model=model_name)
    query_cache = SimpleQueryCache(max_items=cache_max_items) if (enable_cache and SimpleQueryCache) else None
    compressor = TextCompressor() if (enable_compression and TextCompressor) else None

    def _extract_user_content(msgs) -> Optional[str]:
        for m in reversed(msgs):
            if isinstance(m, tuple):
                if m[0] == "user":
                    return m[1]
            else:
                role = getattr(m, "role", None) or (isinstance(m, dict) and m.get("role"))
                if role == "user":
                    return getattr(m, "content", None) or (isinstance(m, dict) and m.get("content"))
        return None

    def structured_invoke(state: Dict[str, Any]) -> Dict[str, Any]:
        """统一返回结构: {answer, raw, route_strategy, adapter_used, token_usage, messages}"""
        token_counter.start_counting()
        msgs = state.get("messages", [])
        user_content = _extract_user_content(msgs)
        route_strategy = None
        route_coverage = None
        time_sensitive = None
        mutated_state = dict(state)
        cache_hit = False
        compression_meta = None
        if query_cache and isinstance(user_content, str):
            cached_entry = query_cache.get(user_content)
            if cached_entry:
                cached_result = cached_entry['result']
                cache_hit = True
                return {
                    **cached_result,
                    "cache_hit": True,
                    "adapter_used": adapter.__class__.__name__ if adapter else None,
                }

        # 路由 & 用户消息增强
        if enable_smart_routing and router is not None and isinstance(user_content, str) and user_content.strip():
            try:
                route_strategy, route_coverage, time_sensitive = router.route_details(user_content)
            except Exception:
                route_strategy = router.route(user_content)
            annotated = f"[路由策略]={route_strategy} → {user_content}"
            state_msgs = list(mutated_state.get("messages", []))
            state_msgs.insert(0, ("system", annotated))
            # 适配器增强
            if enable_model_adapter and adapter is not None and route_strategy != "local_only":
                enhanced = adapter.enhance_user_message(user_content, may_need_tools=True)
                if enhanced != user_content:
                    for i in range(len(state_msgs)-1, -1, -1):
                        role, content = state_msgs[i]
                        if role == "user" and content == user_content:
                            state_msgs[i] = (role, enhanced)
                            break
            mutated_state["messages"] = state_msgs
        else:
            # 适配器在未启用路由情况下也可增强（假设都需要工具预判由简单启发决定）
            if enable_model_adapter and adapter is not None and isinstance(user_content, str):
                enhanced = adapter.enhance_user_message(user_content, may_need_tools=True)
                if enhanced != user_content:
                    state_msgs = list(mutated_state.get("messages", []))
                    for i in range(len(state_msgs)-1, -1, -1):
                        role, content = state_msgs[i]
                        if role == "user" and content == user_content:
                            state_msgs[i] = (role, enhanced)
                            break
                    mutated_state["messages"] = state_msgs

        # === 执行底层调用 ===
        raw_result = original_invoke(mutated_state)
        # Token usage 统计
        usage_record = {}
        try:
            usage_record = count_tokens_for_result(user_content or "", raw_result, token_counter)
        except Exception as e:
            usage_record = {"error": f"token_count_failed: {e}"}

        # 提取最终回答文本
        answer_text = None
        try:
            from utils import extract_final_answer
            answer_text = extract_final_answer(raw_result)
        except Exception:
            msgs_out = raw_result.get("messages", []) if isinstance(raw_result, dict) else []
            for m in reversed(msgs_out):
                if isinstance(m, tuple) and m[0] == "assistant":
                    answer_text = m[1]; break
                if isinstance(m, dict) and m.get("role") == "assistant":
                    answer_text = m.get("content"); break
        if answer_text is None:
            answer_text = "(未能提取回答内容)"
        if compressor:
            comp = compressor.maybe_compress(answer_text)
            compression_meta = comp
            if comp.get("applied"):
                answer_text = comp.get("compressed") or answer_text

        # 引用来源解析
        sources = []
        try:
            import re
            for match in re.findall(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", answer_text):
                p, disp = match
                display_text = (disp or p).strip()
                sources.append({
                    "type": "internal", 
                    "path": p.strip(), 
                    "display": display_text,
                    "title": display_text  # 添加 title 字段用于 API 兼容
                })
            for match in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", answer_text):
                txt, url = match
                sources.append({
                    "type": "external", 
                    "text": txt.strip(), 
                    "url": url.strip(),
                    "title": txt.strip()  # 添加 title 字段用于 API 兼容
                })
        except Exception:
            pass

        final_payload = {
            "answer": answer_text,
            "raw": raw_result,
            "route_strategy": route_strategy,
            "route_coverage": route_coverage,
            "time_sensitive": time_sensitive,
            "adapter_used": adapter.__class__.__name__ if adapter else None,
            "token_usage": usage_record,
            "sources": sources,
            "messages": raw_result.get("messages") if isinstance(raw_result, dict) else None,
            "cache_hit": cache_hit,
            "compression": compression_meta,
        }
        if query_cache and isinstance(user_content, str):
            try:
                query_cache.set(user_content, final_payload)
            except Exception:
                pass
        return final_payload

    assistant.invoke = structured_invoke  # type: ignore

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
    
    result = assistant.invoke({"messages": [("user", question)]})
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
