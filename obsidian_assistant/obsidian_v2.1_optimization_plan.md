# Obsidian 助手 V2.1 优化方案

**创建日期**: 2025-11-13  
**当前版本**: V2.0  
**目标版本**: V2.1  
**优化目标**: 降低 Token 消耗，提升响应速度，优化成本效益

---

## 📊 V2.0 性能基准测试

### 测试环境
- **模型**: ChatTongyi (qwen-turbo)
- **定价**: 输入 ¥0.002/1K tokens, 输出 ¥0.006/1K tokens
- **测试时间**: 2025-11-13
- **测试样本**: 3个典型场景

### 测试结果

| 场景 | 响应时间 | Token 消耗 | 成本 | 说明 |
|------|----------|-----------|------|------|
| 纯本地搜索 | 4.31s | 512 | ¥0.0030 | Obsidian 知识库查询 |
| 网页搜索 | 14.22s | 1,232 | ¥0.0073 | 使用触发关键词（"推荐"/"最新"） |
| 混合搜索 | 3.55s | 515 | ¥0.0030 | 优先本地，按需补充网页 |

**总计**: 3次调用，22.07秒，2,259 tokens，¥0.0133

### 关键发现

1. **性能差异显著**
   - 网页搜索 tokens 消耗是本地搜索的 **2.4倍**
   - 网页搜索响应时间是本地搜索的 **3.3倍**
   
2. **成本预估**（按每天100次查询）
   - 纯本地模式: ¥9/月
   - 纯网页模式: ¥22/月
   - 混合模式(70%本地+30%网页): ¥13/月

3. **优化空间**
   - 重复查询未被缓存
   - 网页搜索结果冗长（占用大量 tokens）
   - 缺乏智能路由机制判断是否需要网页搜索

---

## 🚀 V2.1 优化方案

### 方案 1: 智能路由器 🎯

**优先级**: 🥇 P0 (最高)  
**难度**: ⭐⭐ (中等)  
**预期收益**: 40-60% token 节省  
**适用场景**: 所有查询

#### 设计思路
通过语义分析和关键词检测，自动判断查询的最优搜索策略：
- **本地优先**: 基础知识、操作指南、已有文档
- **网页优先**: 时效性信息、最新动态、未覆盖内容
- **混合模式**: 需要本地+网页综合信息

#### 实现代码框架

```python
class SmartRouter:
    """智能路由器 - 自动选择最优搜索策略"""
    
    def __init__(self, obsidian_path: str):
        self.obsidian_path = obsidian_path
        self.time_sensitive_keywords = ["最新", "2025", "2024", "推荐", "现在", "今年"]
        self.local_knowledge_base = self._build_local_index()
    
    def route(self, query: str) -> str:
        """
        路由决策
        Returns: "local_only" | "web_first" | "hybrid"
        """
        # 1. 检测时效性需求
        if self._is_time_sensitive(query):
            return "web_first"
        
        # 2. 检测本地知识覆盖率
        coverage_score = self._check_local_coverage(query)
        
        if coverage_score > 0.8:
            return "local_only"  # 高覆盖，纯本地
        elif coverage_score > 0.4:
            return "hybrid"      # 中等覆盖，混合模式
        else:
            return "web_first"   # 低覆盖，网页优先
    
    def _is_time_sensitive(self, query: str) -> bool:
        """检测是否需要最新信息"""
        return any(keyword in query for keyword in self.time_sensitive_keywords)
    
    def _check_local_coverage(self, query: str) -> float:
        """计算本地知识库覆盖率 (0.0-1.0)"""
        keywords = self._extract_keywords(query)
        matched_count = sum(1 for kw in keywords if kw in self.local_knowledge_base)
        return matched_count / len(keywords) if keywords else 0.0
    
    def _build_local_index(self) -> set:
        """构建本地知识库索引"""
        # 扫描 Obsidian 文档，提取关键词
        # 实现: 读取所有 .md 文件，提取标题和关键词
        pass
    
    def _extract_keywords(self, text: str) -> list:
        """提取查询关键词"""
        # 简单实现：分词 + 去停用词
        import re
        words = re.findall(r'\w+', text.lower())
        stopwords = {'的', '是', '在', '了', '有', '和', '就', '不', 'the', 'is', 'a', 'an'}
        return [w for w in words if w not in stopwords and len(w) > 1]
```

#### 集成到 V2.1

```python
def create_obsidian_assistant_v21(
    model_name: str = "qwen-turbo",
    obsidian_path: str = DEFAULT_OBSIDIAN_PATH,
    enable_smart_routing: bool = True  # 新增参数
):
    """创建带智能路由的 Obsidian 助手 V2.1"""
    
    # 初始化智能路由器
    router = SmartRouter(obsidian_path) if enable_smart_routing else None
    
    # 修改提示词，加入路由策略说明
    enhanced_prompt = OBSIDIAN_ASSISTANT_PROMPT_V2 + """

## 智能路由策略 (V2.1)
根据查询类型，系统会自动选择最优搜索策略：
- **本地优先**: 对于基础操作、已有文档的查询，直接使用本地知识库
- **网页优先**: 对于"最新"、"推荐"等时效性需求，优先网页搜索
- **混合模式**: 需要综合本地+网页信息时，按需组合
"""
    
    # ... (其他代码保持不变)
    
    return agent_executor
```

#### 预期效果
- 避免不必要的网页搜索调用（节省 14秒响应时间）
- 本地能解决的问题不触发子代理（节省 ~700 tokens）
- 整体 token 消耗降低 **40-60%**

---

### 方案 2: 多级缓存系统 🏆

**优先级**: 🥈 P1 (高)  
**难度**: ⭐⭐⭐ (较难)  
**预期收益**: 80% token 节省 (针对重复查询)  
**适用场景**: 高频问题、重复查询

#### 设计思路
建立三级缓存体系：
1. **内存缓存**: 秒级响应，当前会话有效
2. **磁盘缓存**: 跨会话持久化，1小时 TTL
3. **语义缓存**: 相似问题命中（未来扩展）

#### 实现代码框架

```python
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

class CachedObsidianAssistant:
    """带多级缓存的 Obsidian 助手"""
    
    def __init__(self, base_assistant, cache_dir: str = ".cache"):
        self.assistant = base_assistant
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # 内存缓存
        self.memory_cache = {}
        
        # 缓存配置
        self.ttl_seconds = 3600  # 1小时过期
    
    def query(self, question: str) -> dict:
        """带缓存的查询"""
        cache_key = self._get_cache_key(question)
        
        # 1. 检查内存缓存
        if cache_key in self.memory_cache:
            print("🚀 命中内存缓存")
            return self.memory_cache[cache_key]
        
        # 2. 检查磁盘缓存
        cached_result = self._load_from_disk(cache_key)
        if cached_result and not self._is_expired(cached_result):
            print(f"💾 命中磁盘缓存 (缓存于 {cached_result['cached_at']})")
            self.memory_cache[cache_key] = cached_result
            return cached_result
        
        # 3. 实际查询
        print("🔍 缓存未命中，执行实际查询...")
        result = self.assistant.invoke({"messages": [("user", question)]})
        
        # 4. 保存缓存
        cached_data = {
            "question": question,
            "result": result,
            "cached_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(seconds=self.ttl_seconds)).isoformat()
        }
        self._save_to_disk(cache_key, cached_data)
        self.memory_cache[cache_key] = cached_data
        
        return cached_data
    
    def _get_cache_key(self, question: str) -> str:
        """生成缓存键（MD5哈希）"""
        return hashlib.md5(question.encode('utf-8')).hexdigest()
    
    def _load_from_disk(self, cache_key: str) -> dict:
        """从磁盘加载缓存"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ 缓存加载失败: {e}")
        return None
    
    def _save_to_disk(self, cache_key: str, data: dict):
        """保存缓存到磁盘"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 缓存保存失败: {e}")
    
    def _is_expired(self, cached_data: dict) -> bool:
        """检查缓存是否过期"""
        expires_at = datetime.fromisoformat(cached_data['expires_at'])
        return datetime.now() > expires_at
    
    def clear_cache(self):
        """清空所有缓存"""
        self.memory_cache.clear()
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
        print("🗑️ 缓存已清空")
```

#### 使用示例

```python
# 创建带缓存的助手
base_assistant = create_obsidian_assistant_v21()
cached_assistant = CachedObsidianAssistant(base_assistant)

# 第一次查询（实际调用 LLM）
result1 = cached_assistant.query("如何创建双向链接？")

# 第二次相同查询（命中缓存，0 tokens）
result2 = cached_assistant.query("如何创建双向链接？")
```

#### 预期效果
- 重复查询 **0 tokens** 消耗
- 响应时间从 4秒降至 **<0.1秒**
- 针对高频问题（FAQ），节省 **80%+ tokens**

---

### 方案 3: 结果压缩与摘要 📦

**优先级**: 🥉 P2 (中)  
**难度**: ⭐⭐⭐⭐ (困难)  
**预期收益**: 30-50% token 节省 (针对网页搜索)  
**适用场景**: 网页搜索结果处理

#### 设计思路
网页搜索返回的内容通常冗长，包含大量冗余信息：
- **问题**: 测试 2 显示网页搜索消耗 1,232 tokens（本地搜索的 2.4倍）
- **解决方案**: 对网页结果进行智能压缩和摘要

#### 实现代码框架

```python
from typing import List
import re

class WebResultCompressor:
    """网页搜索结果压缩器"""
    
    def __init__(self, max_tokens_per_result: int = 150):
        self.max_tokens_per_result = max_tokens_per_result
    
    def compress(self, web_results: List[dict]) -> str:
        """压缩网页搜索结果"""
        if not web_results:
            return ""
        
        compressed_items = []
        
        for idx, result in enumerate(web_results[:5], 1):  # 最多保留5条
            # 1. 提取关键信息
            title = result.get("title", "")
            url = result.get("url", "")
            content = result.get("content", "")
            
            # 2. 内容摘要（保留前150个字符或核心句子）
            summary = self._extract_key_sentences(content)
            
            # 3. 格式化输出
            compressed_items.append(f"{idx}. **{title}**\n   {summary}\n   🔗 {url}")
        
        return "\n\n".join(compressed_items)
    
    def _extract_key_sentences(self, text: str, max_length: int = 150) -> str:
        """提取核心句子"""
        # 简单实现：取前两句话
        sentences = re.split(r'[。！？.!?]\s*', text)
        result = []
        current_length = 0
        
        for sentence in sentences:
            if current_length + len(sentence) > max_length:
                break
            result.append(sentence)
            current_length += len(sentence)
        
        summary = '。'.join(result)
        return summary + '...' if len(text) > current_length else summary
    
    def _deduplicate(self, results: List[dict]) -> List[dict]:
        """去除重复内容"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get("url", "")
            if url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        return unique_results
```

#### 集成到网页搜索工具

```python
def internet_search_v21(query: str, compressor: WebResultCompressor) -> str:
    """V2.1 增强版网页搜索（带结果压缩）"""
    try:
        tavily = TavilySearchResults(
            max_results=5,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=False  # 减少冗余内容
        )
        
        results = tavily.invoke({"query": query})
        
        # 🆕 压缩结果
        compressed = compressor.compress(results)
        
        return f"""
### 网页搜索结果 (已优化)
{compressed}

💡 提示: 以上内容已自动压缩，仅保留核心信息
"""
    except Exception as e:
        return f"⚠️ 网页搜索出错: {str(e)}"
```

#### 预期效果
- 网页搜索结果 tokens 从 1,232 降至 **600-800**
- 保留核心信息，去除冗余内容
- 响应速度提升（更少 tokens 需要处理）

---

## 📋 实施路线图

### Phase 1: 快速收益 (1-2天)
- [x] V2.0 基准测试完成
- [x] Token 计数器集成
- [ ] **实施智能路由器** (方案1) - 最快见效

### Phase 2: 深度优化 (3-5天)
- [ ] **实施多级缓存** (方案2) - 最大收益
- [ ] 缓存性能测试
- [ ] 调优 TTL 和缓存策略

### Phase 3: 精细化 (5-7天)
- [ ] **实施结果压缩** (方案3)
- [ ] 压缩效果评估
- [ ] A/B 测试对比

### Phase 4: 监控与迭代 (持续)
- [ ] Token 使用监控面板
- [ ] 成本预警机制
- [ ] 定期性能回归测试

---

## 🎯 预期总体收益

| 指标 | V2.0 基线 | V2.1 预期 | 改善幅度 |
|------|-----------|-----------|----------|
| 平均响应时间 | 7.36s | 4.5s | ⬇️ 39% |
| 平均 Token 消耗 | 753 | 380 | ⬇️ 50% |
| 月度成本 (100次/天) | ¥13 | ¥6.5 | ⬇️ 50% |
| 缓存命中率 | 0% | 30-50% | ⬆️ 50% |

---

## 📊 监控指标

### 关键性能指标 (KPIs)
1. **Token 使用率**: 单次查询 tokens / 目标阈值 (500)
2. **缓存命中率**: 缓存命中次数 / 总查询次数
3. **路由准确率**: 智能路由决策正确率
4. **成本效益**: 节省的成本 / 总成本

### 监控工具集成
```python
class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.metrics = {
            "total_queries": 0,
            "cache_hits": 0,
            "local_only_queries": 0,
            "web_search_queries": 0,
            "total_tokens": 0,
            "total_cost": 0.0
        }
    
    def log_query(self, query_type: str, tokens: int, cost: float, cache_hit: bool):
        """记录查询指标"""
        self.metrics["total_queries"] += 1
        self.metrics["total_tokens"] += tokens
        self.metrics["total_cost"] += cost
        
        if cache_hit:
            self.metrics["cache_hits"] += 1
        
        if query_type == "local":
            self.metrics["local_only_queries"] += 1
        elif query_type == "web":
            self.metrics["web_search_queries"] += 1
    
    def get_report(self) -> dict:
        """生成性能报告"""
        if self.metrics["total_queries"] == 0:
            return {}
        
        return {
            "cache_hit_rate": self.metrics["cache_hits"] / self.metrics["total_queries"],
            "avg_tokens": self.metrics["total_tokens"] / self.metrics["total_queries"],
            "avg_cost": self.metrics["total_cost"] / self.metrics["total_queries"],
            "web_search_ratio": self.metrics["web_search_queries"] / self.metrics["total_queries"]
        }
```

---

## 🔧 配置建议

### 开发环境配置
```python
# config_v21.py

V21_CONFIG = {
    # 智能路由器配置
    "routing": {
        "enabled": True,
        "local_coverage_threshold": 0.7,  # 本地覆盖率阈值
        "time_sensitive_keywords": ["最新", "推荐", "2025", "现在"]
    },
    
    # 缓存配置
    "cache": {
        "enabled": True,
        "ttl_seconds": 3600,  # 1小时
        "cache_dir": ".cache/obsidian",
        "max_cache_size_mb": 100  # 最大缓存100MB
    },
    
    # 压缩配置
    "compression": {
        "enabled": True,
        "max_tokens_per_result": 150,
        "max_results": 5
    },
    
    # Token 预算
    "budget": {
        "max_tokens_per_query": 800,  # 单次查询上限
        "daily_token_limit": 50000,   # 每日 token 限制
        "alert_threshold": 0.8        # 80%时发送警告
    }
}
```

---

## 📚 参考资源

1. **LangChain 缓存文档**: https://python.langchain.com/docs/modules/model_io/llms/llm_caching
2. **Token 优化最佳实践**: https://platform.openai.com/docs/guides/prompt-engineering
3. **Obsidian API 文档**: https://github.com/obsidianmd/obsidian-api

---

## ✅ 验收标准

### V2.1 版本发布条件
- [ ] 智能路由器实现并通过单元测试
- [ ] 缓存系统实现并验证命中率 > 30%
- [ ] Token 消耗相比 V2.0 降低 > 40%
- [ ] 所有原有功能正常工作（回归测试通过）
- [ ] 更新用户文档和 README

---

**文档版本**: V2.1-PLAN-20251113  
**负责人**: YF  
**审核状态**: 待实施
