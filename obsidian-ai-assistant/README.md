# AI Assistant for Obsidian

An intelligent Obsidian plugin powered by DeepAgents that brings AI-powered assistance directly into your note-taking workflow.

**当前版本**: v0.1.0  
**测试状态**: ✅ 核心功能测试通过 (16/16)  
**发布状态**: 内部 Beta 测试就绪  
**最后更新**: 2025-11-14

## 📊 测试总结

| 测试类别 | 通过率 | 状态 |
|---------|--------|------|
| API 端点 | 3/3 (100%) | ✅ 通过 |
| 插件集成 | 5/5 (100%) | ✅ 通过 |
| 核心功能 | 9/9 (100%) | ✅ 通过 |
| **总计** | **17/17 (100%)** | ✅ **通过** |

**性能亮点**:
- ⚡ 响应时间：1.9秒（超预期 5倍）
- ✅ 本地搜索准确率：~95%
- 🎯 稳定性：无崩溃，100% 成功率
- 📊 可观测性：完整的运行日志（工具调用 + 路由策略 + 覆盖率）⬆️ **新增**

**已修复问题** (1个):
- ✅ P0: 内部链接跳转 - **已修复并验证**

**待优化项** (3个):
- P1: 缺少复制/插入功能
- P2: 参考来源重复显示  
- P2: 界面语言不可配置

详见：[测试报告](../docs/reports/20251114-testing-plugin-integration.md)

---

## Features

- 🤖 **AI-Powered Chat Interface** - Ask questions about your notes and get intelligent responses
- 🔍 **Smart Search** - Combines local note search with web search capabilities
- 📝 **Source Citations** - Every answer includes references to relevant notes or web sources
- � **Internal Link Navigation** - Click on note references to jump directly to them ✅ **已修复**
- �💰 **Cost Tracking** - Monitor token usage and estimated costs
- ⚡ **Caching** - Reduce API calls and costs with intelligent response caching
- 🎯 **Smart Routing** - Automatically chooses between local and web search
- � **Detailed Logging** - View tool calls, routing decisions, and coverage metrics ⬆️ **新增**

## Prerequisites

### Backend Setup

This plugin requires the DeepAgents Python backend to be running. Follow these steps:

1. **Navigate to the project root:**
   ```bash
   cd /path/to/deepagents
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -e deepagents_official/libs/deepagents
   pip install -r obsidian_assistant/requirements.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file in the project root:
   ```bash
   DASHSCOPE_API_KEY=your-qwen-api-key
   TAVILY_API_KEY=your-tavily-api-key
   ```

4. **Start the API server:**
   ```bash
   cd obsidian_assistant
   python api_server.py
   ```

   The server will start at `http://localhost:8000`

## Installation

### From Source (Development)

1. Clone this repository into your Obsidian plugins folder:
   ```bash
   cd /path/to/your/vault/.obsidian/plugins
   git clone https://github.com/YFOOOO/deepagents-obsidian.git obsidian-ai-assistant
   cd obsidian-ai-assistant
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Build the plugin:
   ```bash
   npm run build
   ```

4. Enable the plugin in Obsidian:
   - Open Settings → Community plugins
   - Turn off "Restricted mode"
   - Find "AI Assistant (DeepAgents)" and enable it

### From Release (Coming Soon)

Will be available in the Obsidian Community Plugins directory.

## Usage

### Open the AI Assistant

- **Ribbon Icon**: Click the robot icon in the left sidebar
- **Command Palette**: `Ctrl/Cmd + P` → "Open AI Assistant"

### Settings

Configure the plugin in Settings → AI Assistant:

| Setting | Description | Default |
|---------|-------------|---------|
| **Backend API URL** | URL of your Python backend | `http://localhost:8000` |
| **API Key** | Optional authentication key | (empty) |
| **Model** | AI model to use | `qwen-turbo` |
| **Enable Caching** | Cache responses to reduce costs | `true` |
| **Enable Smart Routing** | Auto-choose local vs web search | `true` |

### Example Queries

**Local Knowledge Base:**
- "How do I create backlinks in Obsidian?"
- "Summarize my notes about project management"
- "Find all mentions of 'daily note template'"

**Web Search:**
- "What are the latest Obsidian plugins for 2025?"
- "Recommend productivity apps that work with Obsidian"
- "What's new in Obsidian 1.5?"

**Mixed Queries:**
- "Compare my note-taking workflow with best practices"
- "How does Canvas feature work? Do I have notes about it?"

## Development

### Build for Development

```bash
npm run dev
```

This starts a watch mode that rebuilds on file changes.

### Build for Production

```bash
npm run build
```

### Linting and Formatting

```bash
npm run lint        # Check for errors
npm run lint:fix    # Auto-fix errors
npm run format      # Format with Prettier
```

## Architecture

```
┌─────────────────────────────────────┐
│   Obsidian (Electron)               │
│  ┌───────────────────────────────┐  │
│  │  TypeScript Plugin            │  │
│  │  - Chat UI                    │  │
│  │  - Settings                   │  │
│  │  - API Client                 │  │
│  └───────────┬───────────────────┘  │
└──────────────┼──────────────────────┘
               │ HTTP REST API
┌──────────────▼──────────────────────┐
│   Python Backend (FastAPI)          │
│  ┌───────────────────────────────┐  │
│  │  DeepAgents Framework         │  │
│  │  - Smart Router               │  │
│  │  - Model Adapter              │  │
│  │  - Cache Layer                │  │
│  │  - Obsidian Search            │  │
│  │  - Web Search (Tavily)        │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

## Performance

Based on testing with `qwen-turbo` model:

| Query Type | Response Time | Tokens | Cost/Query | Monthly Cost (100/day) |
|------------|---------------|---------|-----------|----------------------|
| Local Search | ~4s | ~512 | ¥0.0003 | ¥0.9 |
| Web Search | ~12s | ~1,232 | ¥0.0009 | ¥2.7 |
| Mixed | ~9s | ~530 | ¥0.0003 | ¥0.9 |

## Troubleshooting

### Plugin doesn't load
- Check that you've built the plugin (`npm run build`)
- Ensure `main.js` exists in the plugin folder
- Check the console for error messages (Ctrl/Cmd + Shift + I)

### "Disconnected" status
- Verify the Python backend is running
- Check the API URL in settings matches the backend
- Test the backend directly: `curl http://localhost:8000/health`

### No responses from AI
- Check your API keys in the backend `.env` file
- View backend logs for errors
- Ensure you have internet connectivity (for web search)

### Viewing Backend Logs

The backend now provides detailed logging for debugging:

**What you'll see in the logs:**
```
============================================================
📝 查询请求: your query here
============================================================
🔍 [search_obsidian_docs_v2] 工具被调用
   查询: 'your search query'
   最大结果数: 5
   搜索目录: /path/to/vault
   目录存在: True
   📄 .md 文件总数: 671
   🔎 搜索关键词: 'keyword'
   ✅ 搜索完成: 检查了 X 个文件，找到 Y 个结果

============================================================
✅ 查询完成
------------------------------------------------------------
🧭 路由策略: local_only | hybrid | web_first
📊 覆盖率: XX.X%
⚡ 缓存命中: 是 (if applicable)
🔢 Token 使用: (if available)
   - Prompt: XXX tokens
   - Completion: XXX tokens
   - Total: XXX tokens
   - Cost: ¥X.XXXXXX
📚 参考来源: X 个
============================================================
```

**Log indicators:**
- 🔍 Local search tool invocation
- 🌐 Web search tool invocation
- 🧭 Routing strategy decision
- 📊 Coverage percentage
- ⚡ Cache hit status
- 🔢 Token usage and cost

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Related Projects

- **DeepAgents**: https://github.com/langchain-ai/deepagents
- **Backend Repository**: https://github.com/YFOOOO/deepagents-obsidian

## 📚 Documentation

### Plugin Documentation
- **README** (this file) - Overview and quick start
- **[docs/TEST_LOG.md](docs/TEST_LOG.md)** - Detailed test logs and results
- **[docs/OPTIMIZATION_PLAN.md](docs/OPTIMIZATION_PLAN.md)** - Next steps and optimization roadmap
- **[docs/INTEGRATION_TEST_CHECKLIST.md](docs/INTEGRATION_TEST_CHECKLIST.md)** - Complete testing checklist
- **[docs/API_SERVER_TROUBLESHOOTING.md](docs/API_SERVER_TROUBLESHOOTING.md)** - API server troubleshooting guide
- **[docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md)** - Pre-release checklist

### Project Documentation
- **[Testing Report](../docs/reports/20251114-testing-plugin-integration.md)** - Complete integration test report
- **[Project README](../README.md)** - Main project documentation
- **[Backend Guide](../obsidian_assistant/README.md)** - Python backend documentation

## License

MIT License - see [LICENSE](../LICENSE) for details

## Support

- **Issues**: https://github.com/YFOOOO/deepagents-obsidian/issues
- **Documentation**: https://github.com/YFOOOO/deepagents-obsidian/tree/main/docs

---

**Current Version**: 0.1.1 ⬆️  
**Last Updated**: 2025-11-14 18:15  
**Maintainer**: YF

**Recent Updates**:
- ✅ Fixed internal link navigation (sourcePath correction)
- ✅ Enhanced backend logging (tool calls + routing + coverage)
- ✅ Verified 100% test pass rate (17/17)
