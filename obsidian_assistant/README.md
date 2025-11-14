# Obsidian 助手

基于 DeepAgents 框架的智能 Obsidian 知识库助手，支持本地文档搜索和网页搜索的混合查询。

##  快速开始

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

## 📊 核心功能

### V2.0 特性

1. **本地知识库搜索** - 支持 Obsidian 文档检索，返回文件路径用于生成内部链接
2. **网页搜索子代理** - 集成 Tavily API，智能触发关键词: "最新", "推荐", "插件"
3. **混合引用格式** - 自动生成 Obsidian 内部链接和网页链接
4. **Token 使用监控** - 实时统计输入/输出 tokens，成本预估

### 性能数据

| 测试场景 | 响应时间 | Token 消耗 | 成本 |
|---------|---------|-----------|------|
| 纯本地搜索 | 4.31s | 512 | ¥0.0030 |
| 网页搜索 | 14.22s | 1,232 | ¥0.0073 |
| 混合搜索 | 3.55s | 515 | ¥0.0030 |

## 📁 项目文件

### 核心模块

| 文件 | 说明 |
|------|------|
| `obsidian_assistant.py` | 封装的 Obsidian 助手模块 |
| `token_counter.py` | Token 使用监控工具 |
| `model_adapters.py` | 多模型适配器 |
| `smart_router.py` | 智能路由器（V2.1） |
| `cache_layer.py` | 缓存层（V2.1） |

### 测试文件

测试文件位于 `tests/obsidian_v21/` 目录。

## 📚 详细文档

- **完整使用指南**: 本文件
- **V2.0 vs Copilot 对比**: [对比报告](../docs/obsidian/obsidian-comparison-v2.0-vs-copilot.md)
- **V2.1 优化计划**: [优化方案](../docs/obsidian/obsidian-optimization-plan-v2.1.md)
- **示例 Notebooks**: [演示代码](../examples/notebooks/)
- **命名规范**: [文档命名规范](../docs/NAMING_CONVENTION.md)

## 🔧 配置说明

### 默认路径配置

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

counter = TokenCounter(model="qwen-turbo")
```

## 🧪 运行测试

查看 Notebook 示例：

```bash
cd ../examples/notebooks
jupyter notebook
```

测试包括:
1. ✅ 环境变量检查
2. ✅ 模块加载验证
3. ✅ 纯本地搜索测试
4. ✅ 网页搜索测试
5. ✅ 混合搜索测试
6. ✅ Token 统计报告

## 📈 V2.1 路线图

详见 [V2.1 优化计划](../docs/obsidian/obsidian-optimization-plan-v2.1.md)

- [ ] 智能路由器 (降低不必要网页调用)
- [ ] 多级缓存 (高频零成本响应)
- [ ] 结果压缩 (网页 token 减少 30-50%)
- [ ] 模型适配器 (提升工具调用稳定性)
- [ ] 时间范围搜索
- [ ] 向量索引 + 相关笔记推荐

预期收益：
- 平均响应时间: 7.36s → 4.5s (⬇️ 39%)
- 平均 Token: 753 → 380 (⬇️ 50%)
- 月度成本: ¥13 → ¥6.5 (⬇️ 50%)

## 📄 许可证

本项目遵循 DeepAgents 项目的许可证。

---

**当前版本**: V2.0  
**最后更新**: 2025-11-14  
**维护者**: YF
