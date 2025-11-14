# Obsidian 助手 - Jupyter Notebook 演示

本目录包含 Obsidian 助手的交互式演示和测试用例。

## 📚 Notebook 列表

### 1. `deepagents_demo.ipynb`
**DeepAgents 基础演示**
- DeepAgents 框架基本使用
- 工具调用示例
- Agent 配置演示

### 2. `obsidian_V2.0_test_with_tokens.ipynb` ⭐
**V2.0 性能测试与成本分析**
- 多场景 Token 消耗对比测试
- 智能价格管理系统 (v2.0)
- 10 个主流模型成本对比
- qwen-max 降价分析 (47% 降幅)
- 月度成本预估与优化建议

**核心发现**:
- 本地搜索: ~512 tokens, ¥0.0003/次
- 网页搜索: ~1232 tokens, ¥0.0009/次  
- 混合搜索: ~530 tokens, ¥0.0003/次
- 月度成本: ¥0.9-2.7 (100次/天)

### 3. `v21_validation.ipynb`
**V2.1 功能验证**
- 智能路由器测试
- 缓存系统验证
- 模型适配器测试
- 性能对比分析

## 🚀 快速开始

### 1. 环境准备

确保你已经安装了项目依赖：

```bash
# 返回项目根目录
cd /Users/yf/Documents/GitHub/deepagents

# 激活虚拟环境（如果使用）
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 或者安装核心包
pip install jupyter dashscope langchain-community tavily-python langgraph
```

### 2. 环境变量配置

创建 `.env` 文件（已在 `.gitignore` 中）：

```bash
# 在项目根目录创建 .env 文件
cat > ../../.env << EOF
# Qwen/通义千问 API Key
DASHSCOPE_API_KEY=your-dashscope-api-key

# Tavily 搜索 API Key
TAVILY_API_KEY=your-tavily-api-key

# Obsidian 知识库路径（可选）
OBSIDIAN_PATH=/path/to/your/obsidian/vault
EOF
```

或者直接在终端设置：

```bash
export DASHSCOPE_API_KEY="your-dashscope-key"
export TAVILY_API_KEY="your-tavily-key"
export OBSIDIAN_PATH="/path/to/your/vault"
```

### 3. 启动 Jupyter

```bash
# 在当前目录启动
jupyter notebook

# 或者使用 Jupyter Lab
jupyter lab
```

### 4. 路径导入说明

由于 notebook 位于 `examples/notebooks/` 目录，代码中已经包含了自动路径处理：

```python
import sys
from pathlib import Path

# 自动添加项目根目录到 Python 路径
project_root = Path.cwd().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 现在可以导入项目模块
from obsidian_assistant import create_obsidian_assistant_v2
from token_counter import TokenCounter
```

## 📊 运行测试

### 基础测试流程

1. **打开** `obsidian_V2.0_test_with_tokens.ipynb`
2. **检查**环境变量是否正确设置
3. **运行**所有单元格（Kernel → Restart & Run All）
4. **查看**测试结果和 Token 统计

### 预期输出

```
================================================================================
✅ Token 计数器模块 v2.0 加载完成
--------------------------------------------------------------------------------
📦 价格库版本: 2.0
📅 数据更新: 2025-11-14
📚 数据来源: 阿里云百炼官方文档
🔧 支持模型: 10 个
✅ 价格数据新鲜 (更新于 0 天前)
================================================================================

✅ 测试 1: 本地搜索 (~4s, ~512 tokens, ¥0.0003)
✅ 测试 2: 网页搜索 (~12s, ~1,232 tokens, ¥0.0009)
✅ 测试 3: 混合搜索 (~9s, ~530 tokens, ¥0.0003)

📊 累积统计:
  - 总调用: 3 次
  - 总耗时: 25.13 秒
  - 总 Token: 2,274
  - 总成本: ¥0.0134
  - 用量预估 (100次/天): ¥0.45/天 ≈ ¥13.5/月
```

## 🔧 常见问题

### Q1: 导入模块失败
**错误**: `ModuleNotFoundError: No module named 'obsidian_assistant'`

**解决方法**:
```python
# 确保路径添加代码已执行
import sys
from pathlib import Path
project_root = Path.cwd().parent.parent
sys.path.insert(0, str(project_root))
```

### Q2: API Key 未设置
**错误**: `ValueError: DASHSCOPE_API_KEY not found`

**解决方法**:
```python
import os
os.environ['DASHSCOPE_API_KEY'] = 'your-api-key'
os.environ['TAVILY_API_KEY'] = 'your-api-key'
```

### Q3: Obsidian 路径错误
**错误**: `FileNotFoundError: Obsidian vault not found`

**解决方法**:
```python
# 在创建助手时指定正确路径
assistant = create_obsidian_assistant_v2(
    obsidian_path="/correct/path/to/vault"
)
```

## 📦 依赖包列表

### 核心依赖
```
jupyter>=1.0.0
ipykernel>=6.0.0
dashscope>=1.14.0
langchain-community>=0.0.20
tavily-python>=0.3.0
langgraph>=0.0.26
python-dotenv>=1.0.0
```

### 可选依赖
```
matplotlib>=3.7.0  # 用于可视化
pandas>=2.0.0      # 用于数据分析
```

## 📝 开发 Notebook

### 创建新的测试 Notebook

1. **复制模板**：
   ```bash
   cp obsidian_V2.0_test_with_tokens.ipynb my_test.ipynb
   ```

2. **标准头部**：
   ```python
   """
   Notebook 标题
   
   描述：这个 notebook 做什么
   作者：你的名字
   日期：2025-11-14
   """
   
   # 路径设置
   import sys
   from pathlib import Path
   project_root = Path.cwd().parent.parent
   sys.path.insert(0, str(project_root))
   
   # 环境变量
   import os
   from dotenv import load_dotenv
   load_dotenv(project_root / '.env')
   
   # 导入模块
   from obsidian_assistant import create_obsidian_assistant_v2
   from token_counter import TokenCounter
   ```

3. **测试结构**：
   - Section 1: 环境检查
   - Section 2: 功能测试
   - Section 3: 性能分析
   - Section 4: 结果总结

## 📊 性能基准

### V2.0 实测数据 (qwen-turbo)

| 场景 | 响应时间 | Token | 实际成本 | 月度成本 (100次/天) |
|-----|---------|-------|---------|-------------------|
| 📚 本地搜索 | ~4s | ~512 | ¥0.0003 | **¥0.9/月** |
| 🌐 网页搜索 | ~12s | ~1,232 | ¥0.0009 | **¥2.7/月** |
| 🔀 混合搜索 | ~9s | ~530 | ¥0.0003 | **¥0.9/月** |

### 模型成本对比 (本地搜索场景)

| 模型 | 成本/次 | 月度成本 | 相对差异 | 适用场景 |
|------|---------|---------|---------|---------|
| qwen-turbo | ¥0.0002 | ¥0.6 | 基准 (1×) | 日常查询 ✅ |
| qwen-plus | ¥0.0007 | ¥2.1 | 3.5× | 平衡需求 |
| qwen-max | ¥0.0037 | ¥11.1 | 18.5× | 复杂推理 |
| qwen3-max | ¥0.0037 | ¥11.1 | 18.5× | 最新旗舰 |

**重要更新**: qwen-max 已降价 47% (从 ¥6/¥24 降至 ¥3.2/¥12.8)

### 价格管理工具 (v2.0 新增)

```python
from obsidian_assistant.token_counter import (
    list_available_models,      # 查看 10 个支持的模型
    compare_model_costs,         # 对比不同模型成本
    get_pricing_info,           # 获取价格详情
    check_pricing_freshness     # 检查数据新鲜度
)
```

**功能特性**:
- ✅ 版本控制 (v2.0, 更新于 2025-11-14)
- ⚠️ 自动过期检测 (超过30天警告)
- 📋 多模型支持 (Qwen 全系列 + 主流厂商)
- 🔄 便捷更新机制

### V2.1 目标 (规划中)

| 场景 | 目标时间 | 目标 Token | Token 节省 | 成本节省 |
|-----|----------|-----------|-----------|---------|
| 本地搜索 | 3.0s | 350 | ⬇️ 32% | ⬇️ 32% |
| 网页搜索 | 10.0s | 700 | ⬇️ 43% | ⬇️ 43% |
| 混合搜索 | 2.5s | 350 | ⬇️ 34% | ⬇️ 34% |

**优化方向**:
- 智能缓存系统
- Prompt 优化
- 结果过滤增强
- 响应流式输出

## 🔗 相关资源

- **项目主 README**: [../../README.md](../../README.md)
- **Obsidian 助手文档**: [../../obsidian_assistant/README_OBSIDIAN.md](../../obsidian_assistant/README_OBSIDIAN.md)
- **价格管理指南**: [../../docs/obsidian/pricing-guide.md](../../docs/obsidian/pricing-guide.md) ⭐
- **对比报告**: [../../obsidian_assistant/obsidian_comparison_report_v2.0_vs_copilot.md](../../obsidian_assistant/obsidian_comparison_report_v2.0_vs_copilot.md)
- **优化计划**: [../../obsidian_assistant/obsidian_v2.1_optimization_plan.md](../../obsidian_assistant/obsidian_v2.1_optimization_plan.md)
- **命名规范**: [../../docs/NAMING_CONVENTION.md](../../docs/NAMING_CONVENTION.md)

## 💡 最新更新

### 2025-11-14 - Token 计数器 v2.0

**新功能**:
- ✅ 智能价格管理系统
- ✅ 10个主流模型支持
- ✅ 自动过期检测机制
- ✅ 多模型成本对比工具

**价格更新**:
- ✅ qwen-turbo 价格修正 (实际为 ¥0.3/¥0.6)
- ✅ qwen-max 降价 47% (¥3.2/¥12.8)
- ✅ 新增 7 个模型价格数据

**文档**:
- 📖 `pricing-guide.md` - 完整价格管理指南（位于 docs/obsidian/）
- 📊 `README.md` (本文件) - 更新性能基准
- 📓 `obsidian_V2.0_test_with_tokens.ipynb` - 重新梳理结构

## 🤝 贡献

如果你创建了新的测试或演示 notebook：

1. 确保代码可以独立运行
2. 添加清晰的注释和 Markdown 说明
3. 更新本 README 的 Notebook 列表
4. 提交 Pull Request

---

**维护者**: YF  
**最后更新**: 2025-11-14  
**版本**: V2.0 (Token 计数器升级版)  
**价格数据**: v2.0 (2025-11-14)
