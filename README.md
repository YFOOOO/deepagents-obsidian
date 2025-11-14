# DeepAgents 扩展项目

本项目基于 [LangChain AI 的 DeepAgents](https://github.com/langchain-ai/deepagents) 框架，并进行了扩展和定制。

## 📦 项目结构

```
deepagents/
├── deepagents_official/    # DeepAgents 核心框架（带扩展）
├── obsidian_assistant/     # Obsidian 笔记助手（核心代码）
├── examples/               # 示例与演示
│   └── notebooks/         # Jupyter Notebook 演示
├── docs/                  # 项目文档
│   ├── obsidian/         # Obsidian 助手相关文档
│   └── development/      # 开发文档
├── flowchart.mmd         # 流程图
└── README.md             # 本文件
```

## ✨ 主要扩展

### 1. Qwen 模型集成

我们为 DeepAgents 添加了**通义千问（Qwen）模型**的支持：

- 📁 `deepagents_official/examples/qwen/qwen_example.py` - Qwen 模型使用示例
- 🔧 `deepagents_official/examples/research/research_agent.py` - 研究 Agent 支持 Qwen
- 🌐 通过 `langchain-community` 的 `ChatTongyi` 集成

**使用方法：**

```bash
# 安装依赖
pip install dashscope langchain-community

# 设置环境变量
export DASHSCOPE_API_KEY="your-api-key"

# 运行示例
python deepagents_official/examples/qwen/qwen_example.py
```

### 2. Obsidian 助手

智能 Obsidian 笔记管理工具，具备：

- 📝 自动笔记整理与分类
- 🔍 智能笔记搜索
- 🎯 Token 使用优化
- 💡 上下文感知的笔记建议

查看详细文档：
- [快速开始指南](obsidian_assistant/README.md)
- [V2.0 vs Copilot 对比报告](docs/obsidian/obsidian-comparison-v2.0-vs-copilot.md)
- [V2.1 优化计划](docs/obsidian/obsidian-optimization-plan-v2.1.md)
- [Notebook 演示](examples/notebooks/)

## 🚀 快速开始

### 安装 DeepAgents

```bash
cd deepagents_official
pip install -e libs/deepagents
pip install -e libs/deepagents-cli
```

### 运行 Qwen 示例

```bash
# 确保已设置 DASHSCOPE_API_KEY
cd deepagents_official/examples/qwen
python qwen_example.py
```

### 运行 Obsidian 助手

```bash
cd obsidian_assistant
python obsidian_assistant.py
```

## 📚 文档资源

### 核心文档
- **DeepAgents 官方文档**: https://github.com/langchain-ai/deepagents
- **Qwen/通义千问**: https://help.aliyun.com/zh/dashscope/
- **Obsidian 助手文档**: [README](obsidian_assistant/README.md)

### 详细文档
- **Obsidian 助手对比报告**: [V2.0 vs Copilot](docs/obsidian/obsidian-comparison-v2.0-vs-copilot.md)
- **优化计划**: [V2.1 版本规划](docs/obsidian/obsidian-optimization-plan-v2.1.md)
- **示例代码**: [Jupyter Notebooks](examples/notebooks/)
- **命名规范**: [文档命名规范](docs/NAMING_CONVENTION.md)

## 🔧 开发环境设置

### 1. 克隆仓库

```bash
git clone <your-repo-url>
cd deepagents
```

### 2. 安装依赖

```bash
# 安装 DeepAgents
pip install -e deepagents_official/libs/deepagents
pip install -e deepagents_official/libs/deepagents-cli

# 安装 Qwen 支持
pip install dashscope langchain-community

# 安装其他依赖
pip install python-dotenv
```

### 3. 配置环境变量

创建 `.env` 文件（已在 `.gitignore` 中忽略）：

```bash
# Qwen/通义千问 API Key
DASHSCOPE_API_KEY=your-dashscope-api-key

# Tavily 搜索 API（用于研究 Agent）
TAVILY_API_KEY=your-tavily-api-key

# 其他 API Keys...
```

## 🤝 贡献

本项目是 DeepAgents 的扩展版本，主要用于：
- 支持国内大语言模型（如 Qwen）
- Obsidian 笔记管理集成
- 其他定制化功能

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

- **deepagents_official**: 遵循原项目 [MIT License](deepagents_official/LICENSE)
- **obsidian_assistant**: MIT License
- **其他扩展代码**: MIT License

## 🙏 致谢

- [LangChain AI](https://github.com/langchain-ai) - 提供 DeepAgents 框架
- [Alibaba Cloud](https://www.aliyun.com/) - 提供通义千问（Qwen）模型
- Obsidian 社区 - 提供优秀的笔记软件

---

**注意**: 本项目基于 langchain-ai/deepagents 的开源代码进行扩展和定制，保留了原项目的所有功能，并添加了对中文模型和 Obsidian 的支持。
