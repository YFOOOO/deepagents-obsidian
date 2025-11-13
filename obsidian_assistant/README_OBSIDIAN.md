# Obsidian 助手项目

基于 DeepAgents 框架的智能 Obsidian 知识库助手，支持本地文档搜索和网页搜索的混合查询。

## 📁 项目文件

### 核心模块

| 文件 | 版本 | 说明 |
|------|------|------|
| `obsidian_assistant.py` | v2.0 | 封装的 Obsidian 助手模块，提供一键创建功能 |
| `token_counter.py` | v1.0 | Token 使用监控工具，实时跟踪成本 |

### 测试文件

| 文件 | 说明 |
|------|------|
| `obsidian_test_with_tokens.ipynb` | 完整测试套件，包含 Token 计数功能 |

### 文档

| 文件 | 说明 |
|------|------|
| `obsidian_v2.1_optimization_plan.md` | V2.1 优化方案详细设计文档 |
| `README_OBSIDIAN.md` | 本文件 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install dashscope langchain-community tavily-python langgraph
```

### 2. 设置环境变量

```bash
export DASHSCOPE_API_KEY="your-dashscope-key"
export TAVILY_API_KEY="your-tavily-key"
```

### 3. 使用示例

```python
from obsidian_assistant import create_obsidian_assistant_v2
from token_counter import TokenCounter

# 创建助手
assistant = create_obsidian_assistant_v2(
    model_name="qwen-turbo",
    obsidian_path="/path/to/your/obsidian/vault"
)

# 创建 Token 计数器
counter = TokenCounter(model="qwen-turbo")

# 执行查询
counter.start_counting()
result = assistant.invoke({
    "messages": [("user", "如何在 Obsidian 中创建双向链接？")]
})

# 记录统计
from token_counter import count_tokens_for_result
record = count_tokens_for_result("问题", result, counter)
counter.print_current_usage(record)
```

---

## 📊 V2.0 功能特性

### ✨ 核心功能

1. **本地知识库搜索** (`search_obsidian_docs_v2`)
   - 支持 Obsidian 文档检索
   - 返回文件路径用于生成内部链接
   - 平均响应时间: ~4秒

2. **网页搜索子代理** (`web-search-agent-v2`)
   - 集成 Tavily API
   - 智能触发关键词: "最新", "推荐", "插件"
   - 平均响应时间: ~14秒

3. **混合引用格式**
   - Obsidian 内部链接: `[[path|name]]`
   - 网页链接: `[title](url)`
   - 自动分级标注参考来源

4. **Token 使用监控**
   - 实时统计输入/输出 tokens
   - 成本预估（基于 qwen-turbo 定价）
   - 累积统计报告

### 🎯 使用场景

- ✅ **本地知识查询**: Obsidian 操作指南、功能说明
- ✅ **最新信息获取**: 插件推荐、社区动态
- ✅ **混合查询**: 结合本地文档和网页资源

---

## 📈 性能数据 (V2.0)

### 基准测试结果

| 测试场景 | 响应时间 | Token 消耗 | 成本 |
|---------|---------|-----------|------|
| 纯本地搜索 | 4.31s | 512 | ¥0.0030 |
| 网页搜索 | 14.22s | 1,232 | ¥0.0073 |
| 混合搜索 | 3.55s | 515 | ¥0.0030 |

**成本预估** (100次查询/天):
- 纯本地: ¥9/月
- 纯网页: ¥22/月
- 混合模式: ¥13/月

---

## 🔧 配置说明

### `obsidian_assistant.py` 配置

```python
DEFAULT_OBSIDIAN_PATH = "/Users/yf/Documents/Obsidian Vault/我的知识库/Obsidian_Knowledge/obsidian-help-master"

# 修改默认路径
assistant = create_obsidian_assistant_v2(
    obsidian_path="/your/custom/path"
)
```

### Token 计数器配置

```python
from token_counter import TokenCounter, MODEL_PRICING

# 支持的模型
MODEL_PRICING = {
    "qwen-turbo": {"input": 0.002, "output": 0.006},
    "qwen-plus": {"input": 0.004, "output": 0.012},
}

# 创建计数器
counter = TokenCounter(model="qwen-turbo")
```

---

## 🛠️ V2.1 优化计划

详见 `obsidian_v2.1_optimization_plan.md`

### 核心优化方向

1. **智能路由器** (P0)
   - 自动判断查询类型
   - 选择最优搜索策略
   - 预期节省 40-60% tokens

2. **多级缓存系统** (P1)
   - 内存缓存 + 磁盘缓存
   - 重复查询 0 tokens
   - 预期节省 80% (高频问题)

3. **结果压缩** (P2)
   - 网页结果智能摘要
   - 去除冗余内容
   - 预期节省 30-50%

### 预期收益 (V2.1)

| 指标 | V2.0 | V2.1 预期 | 改善 |
|------|------|-----------|------|
| 平均响应时间 | 7.36s | 4.5s | ⬇️ 39% |
| 平均 Token | 753 | 380 | ⬇️ 50% |
| 月度成本 | ¥13 | ¥6.5 | ⬇️ 50% |

---

## 📝 API 参考

### `create_obsidian_assistant_v2()`

创建 Obsidian 助手 V2.0 实例

**参数**:
- `model_name` (str): 模型名称，默认 "qwen-turbo"
- `obsidian_path` (str): Obsidian 知识库路径
- `api_key` (str, optional): API Key，默认从环境变量读取

**返回**: 
- `CompiledGraph`: 可执行的 agent 实例

**示例**:
```python
assistant = create_obsidian_assistant_v2(
    model_name="qwen-turbo",
    obsidian_path="/path/to/vault"
)
```

### `TokenCounter`

Token 使用统计器

**方法**:
- `start_counting()`: 开始计时
- `record_usage(question, prompt_tokens, completion_tokens)`: 记录使用
- `print_current_usage(record)`: 打印当前统计
- `print_statistics()`: 打印累积统计

**示例**:
```python
counter = TokenCounter(model="qwen-turbo")
counter.start_counting()
# ... 执行查询 ...
record = counter.record_usage("问题", 100, 200)
counter.print_current_usage(record)
```

---

## 🧪 测试

运行测试 notebook:

```bash
jupyter notebook obsidian_test_with_tokens.ipynb
```

测试包括:
1. ✅ 环境变量检查
2. ✅ 模块加载验证
3. ✅ 纯本地搜索测试
4. ✅ 网页搜索测试
5. ✅ 混合搜索测试
6. ✅ Token 统计报告

---

## 📚 相关资源

- **DeepAgents 文档**: [deepagents_official/README.md](deepagents_official/README.md)
- **Qwen 示例**: [deepagents_official/examples/qwen/qwen_example.py](deepagents_official/examples/qwen/qwen_example.py)
- **Tavily API**: https://tavily.com
- **Obsidian API**: https://github.com/obsidianmd/obsidian-api

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发路线图

- [x] V2.0: 基础功能 + Token 监控
- [ ] V2.1: 智能路由 + 缓存系统
- [ ] V2.2: 结果压缩 + 性能优化
- [ ] V3.0: 语义缓存 + 多模态支持

---

## 📄 许可证

本项目遵循 DeepAgents 项目的许可证。

---

**最后更新**: 2025-11-13  
**当前版本**: V2.0  
**作者**: YF
