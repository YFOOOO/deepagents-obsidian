# DeepAgents 扩展项目

本项目基于 [LangChain AI 的 DeepAgents](https://github.com/langchain-ai/deepagents) 框架，并进行了扩展和定制。

## 📦 项目结构

```
deepagents/
├── deepagents_official/       # DeepAgents 核心框架（带扩展）
├── obsidian_assistant/        # Obsidian 笔记助手（Python 后端）
├── obsidian-ai-assistant/     # Obsidian 插件（TypeScript）
├── examples/                  # 示例与演示
│   └── notebooks/            # Jupyter Notebook 演示
├── docs/                     # 项目文档
│   ├── obsidian/            # Obsidian 助手相关文档
│   ├── reports/             # 报告和总结
│   └── development/         # 开发文档
├── .github/                  # GitHub 配置
│   └── copilot-instructions.md  # Copilot 工作区说明
├── flowchart.mmd            # 流程图
└── README.md                # 本文件
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

#### Python 后端（obsidian_assistant/）

智能 Obsidian 笔记管理工具，具备：

- 📝 自动笔记整理与分类
- 🔍 智能笔记搜索（本地 + 网页）
- 🎯 Token 使用优化
- 💡 上下文感知的笔记建议
- 🔄 V2.1 优化功能（智能路由、缓存、模型适配器）

查看详细文档：
- [Python 后端指南](obsidian_assistant/README.md)
- [V2.0 vs Copilot 对比报告](docs/obsidian/obsidian-comparison-v2.0-vs-copilot.md)
- [V2.1 优化计划](docs/obsidian/obsidian-optimization-plan-v2.1.md)
- [Notebook 演示](examples/notebooks/)

#### Obsidian 插件（obsidian-ai-assistant/）

TypeScript 实现的 Obsidian 插件，提供：

- 🤖 **聊天界面** - 直接在 Obsidian 中与 AI 对话
- 🔗 **无缝集成** - 自动生成 Obsidian 内部链接 `[[path|name]]`
- 📊 **实时监控** - Token 使用统计和成本追踪
- ⚙️ **灵活配置** - 支持多种模型和搜索策略
- 🎨 **原生体验** - 完全融入 Obsidian 界面

查看详细文档：
- [插件开发指南](obsidian-ai-assistant/README.md)
- [安装说明](#obsidian-插件安装)
- [开发文档](#插件开发)

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

### Obsidian 插件安装

#### 开发模式（推荐用于测试）

1. **构建插件**：
   ```bash
   cd obsidian-ai-assistant
   npm install
   npm run build
   ```

2. **复制到 Obsidian 插件目录**：
   ```bash
   # macOS/Linux
   cp -r . ~/path/to/your/vault/.obsidian/plugins/obsidian-ai-assistant/
   
   # Windows
   xcopy /E /I . "C:\path\to\your\vault\.obsidian\plugins\obsidian-ai-assistant\"
   ```

3. **启动 Python 后端**：
   ```bash
   # 在另一个终端
   cd obsidian_assistant
   python api_server.py  # 需要创建此文件
   ```

4. **在 Obsidian 中启用**：
   - 打开 Settings → Community plugins
   - 关闭 "Restricted mode"
   - 启用 "AI Assistant (DeepAgents)"

#### 生产模式（即将推出）

将在 Obsidian Community Plugins 商店发布。

## 📚 文档资源

### 核心文档
- **DeepAgents 官方文档**: https://github.com/langchain-ai/deepagents
- **Qwen/通义千问**: https://help.aliyun.com/zh/dashscope/
- **Obsidian API**: https://docs.obsidian.md/

### Python 后端文档
- **后端指南**: [obsidian_assistant/README.md](obsidian_assistant/README.md)
- **V2.0 对比报告**: [docs/obsidian/obsidian-comparison-v2.0-vs-copilot.md](docs/obsidian/obsidian-comparison-v2.0-vs-copilot.md)
- **V2.1 优化计划**: [docs/obsidian/obsidian-optimization-plan-v2.1.md](docs/obsidian/obsidian-optimization-plan-v2.1.md)
- **价格管理指南**: [docs/obsidian/pricing-guide.md](docs/obsidian/pricing-guide.md)

### TypeScript 插件文档
- **插件指南**: [obsidian-ai-assistant/README.md](obsidian-ai-assistant/README.md)
- **测试日志**: [obsidian-ai-assistant/docs/TEST_LOG.md](obsidian-ai-assistant/docs/TEST_LOG.md)
- **优化计划**: [obsidian-ai-assistant/docs/OPTIMIZATION_PLAN.md](obsidian-ai-assistant/docs/OPTIMIZATION_PLAN.md)
- **集成测试清单**: [obsidian-ai-assistant/docs/INTEGRATION_TEST_CHECKLIST.md](obsidian-ai-assistant/docs/INTEGRATION_TEST_CHECKLIST.md)
- **开发工作区**: [.github/copilot-instructions.md](.github/copilot-instructions.md)

### 示例与演示
- **Jupyter Notebooks**: [examples/notebooks/](examples/notebooks/)
- **性能测试**: [examples/notebooks/obsidian_V2.0_test_with_tokens.ipynb](examples/notebooks/obsidian_V2.0_test_with_tokens.ipynb)
- **V2.1 验证**: [examples/notebooks/v21_validation.ipynb](examples/notebooks/v21_validation.ipynb)

### 规范文档
- **命名规范**: [docs/NAMING_CONVENTION.md](docs/NAMING_CONVENTION.md)
- **快速参考**: [docs/NAMING_QUICK_REFERENCE.md](docs/NAMING_QUICK_REFERENCE.md)
- **实施总结**: [docs/reports/NAMING_IMPLEMENTATION_SUMMARY.md](docs/reports/NAMING_IMPLEMENTATION_SUMMARY.md)

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

## 🔌 插件开发

### TypeScript 插件架构

```
obsidian-ai-assistant/
├── manifest.json          # 插件元数据
├── package.json           # npm 依赖
├── tsconfig.json          # TypeScript 配置
├── esbuild.config.mjs     # 构建配置
├── styles.css             # 插件样式
└── src/
    ├── main.ts            # 插件入口
    ├── settings.ts        # 设置接口
    ├── api/
    │   └── client.ts      # API 客户端
    └── ui/
        └── chat-view.ts   # 聊天界面
```

### 开发工作流

```bash
# 开发模式（热重载）
npm run dev

# 生产构建
npm run build

# 代码检查
npm run lint

# 代码格式化
npm run format
```

### API 接口设计

插件通过 HTTP REST API 与 Python 后端通信：

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/query` | POST | 发送查询请求 |
| `/models` | GET | 获取可用模型列表 |

详见：[插件 README](obsidian-ai-assistant/README.md)

## 🤝 贡献

本项目是 DeepAgents 的扩展版本，主要特性：

### 核心扩展
- ✅ 支持国内大语言模型（Qwen 系列）
- ✅ Obsidian 笔记管理集成（Python 后端 + TypeScript 插件）
- ✅ Token 计数器 v2.0（10 个主流模型）
- ✅ 智能路由系统（V2.1）
- ✅ 缓存与压缩（V2.1）
- ✅ 完整的文档体系

### 项目亮点
- 📊 **性能优化**: 本地搜索 ~4s，成本 ¥0.0003/次
- 🔧 **开发友好**: 完整的 TypeScript + Python 架构
- 📚 **文档完善**: 对比报告、优化计划、演示 Notebook
- 🎯 **生产就绪**: 可直接部署到 Obsidian

欢迎提交 Issue 和 Pull Request！

### 开发路线图

- [x] V2.0: 基础功能 + Token 计数器
- [x] Obsidian 插件初版（TypeScript）
- [x] Python API 服务器（FastAPI）✅ **2025-11-14 完成**
- [x] API 端点测试全部通过 (3/3) ✅
- [x] Obsidian 插件集成测试通过 ✅
- [ ] V2.1: 智能路由 + 缓存 + 模型适配器
- [ ] 插件核心功能优化（内部链接、复制/插入）🔄 **进行中**
- [ ] 插件 Beta 测试
- [ ] 插件发布到 Obsidian Community
- [ ] 向量索引 + 语义搜索

## 📄 许可证

- **deepagents_official**: 遵循原项目 [MIT License](deepagents_official/LICENSE)
- **obsidian_assistant**: MIT License
- **obsidian-ai-assistant**: MIT License
- **其他扩展代码**: MIT License

## 🙏 致谢

- [LangChain AI](https://github.com/langchain-ai) - 提供 DeepAgents 框架
- [Alibaba Cloud](https://www.aliyun.com/) - 提供通义千问（Qwen）模型
- [Obsidian](https://obsidian.md/) - 提供优秀的笔记软件
- 社区贡献者 - 感谢所有反馈和建议

## 📊 项目统计

### Python 后端（V2.0）

| 指标 | 数值 |
|------|------|
| 支持模型 | 10+ |
| 本地搜索响应时间 | ~4s |
| 本地搜索成本 | ¥0.0003/次 |
| 月度成本（100次/天） | ¥0.9-2.7 |

### TypeScript 插件

| 指标 | 数值 |
|------|------|
| 代码行数 | ~800 |
| 依赖包 | 149 |
| 构建时间 | <5s |
| 插件大小 | ~100KB |

---

**当前版本**: 
- Python 后端: V2.0
- TypeScript 插件: V0.1.0 (测试通过，待优化)

**项目状态**: 
- ✅ 核心功能已完成
- 🔄 插件优化进行中
- 📋 计划 Beta 测试

**最后更新**: 2025-11-14  
**维护者**: YF  
**仓库**: https://github.com/YFOOOO/deepagents-obsidian

---

## 📊 最新进展（2025-11-14）

### ✅ 已完成
1. **API 服务器测试** - 3/3 端点全部通过
   - `/health` - 健康检查 ✅
   - `/models` - 模型列表（10个模型）✅
   - `/query` - 查询处理（1.9秒响应）✅

2. **Obsidian 插件集成测试** - 核心功能验证通过
   - 插件加载和启用 ✅
   - 聊天界面显示 ✅
   - 基本对话功能 ✅
   - 本地笔记搜索 ✅（找到5个相关笔记）
   - 连接状态指示 ✅

### 🔄 进行中
- **内部链接跳转修复**（P0 最高优先级）
- **复制/插入功能开发**（P1 高优先级）
- **界面优化**（参考来源重复、多语言支持）

### 📅 近期计划
- 本周：修复核心问题（内部链接、复制/插入）
- 下周：完善用户体验，发布 v0.2.0 Beta
- 两周后：内部测试
- 一个月后：准备公开发布

详见：
- [测试日志](obsidian-ai-assistant/TEST_LOG.md)
- [优化计划](obsidian-ai-assistant/OPTIMIZATION_PLAN.md)
- [集成测试清单](obsidian-ai-assistant/INTEGRATION_TEST_CHECKLIST.md)

---

**注意**: 本项目基于 langchain-ai/deepagents 的开源代码进行扩展和定制，保留了原项目的所有功能，并添加了对中文模型、Obsidian 笔记系统和 TypeScript 插件的支持。
