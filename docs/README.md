# DeepAgents 项目文档导航

本目录包含 DeepAgents 项目的所有详细文档。

## 📂 文档结构

```
docs/
├── README.md                          # 本文件（文档导航）
├── NAMING_CONVENTION.md               # 文档命名规范（详细版）
├── NAMING_QUICK_REFERENCE.md          # 命名快速参考卡片
├── obsidian/                          # Obsidian 助手文档
│   ├── obsidian-comparison-v2.0-vs-copilot.md       # V2.0 对比报告
│   ├── obsidian-optimization-plan-v2.1.md           # V2.1 优化计划
│   └── pricing-guide.md                             # 价格管理指南
├── development/                       # 开发文档（预留）
└── reports/                          # 时间记录和报告
    ├── 20251114-summary-optimization.md              # 项目优化总结
    ├── 20251114-testing-plugin-integration.md        # 插件集成测试报告 ⭐ 新增
    └── NAMING_IMPLEMENTATION_SUMMARY.md              # 命名规范实施总结
```

## 📚 文档索引

### Obsidian 助手文档

#### [对比报告](obsidian/obsidian-comparison-v2.0-vs-copilot.md)
**DeepAgents Obsidian 助手 V2.0 与 Obsidian-Copilot 对比分析**

内容概览：
- 项目定位对比
- 架构与 Agent 能力
- 模型支持对比
- 工具与操作能力
- 用户体验层对比
- V2.1 目标增强项
- 差异化定位策略
- 行动路线图

**适合阅读对象**：
- 了解项目定位和竞争优势
- 评估技术选型
- 规划产品路线

---

#### [V2.1 优化计划](obsidian/obsidian-optimization-plan-v2.1.md)
**Obsidian 助手 V2.1 版本详细优化方案**

内容概览：
- V2.0 性能基准测试
- 智能路由器设计（P0）
- 多级缓存系统（P1）
- 结果压缩与摘要（P2）
- 模型适配器模式（P0）
- 实施路线图
- 预期收益分析
- 监控指标设计

**适合阅读对象**：
- 参与 V2.1 开发
- 了解优化方向
- 学习性能优化技巧

**关键收益**：
- 平均响应时间降低 39%
- Token 消耗降低 50%
- 月度成本降低 50%

---

#### [价格管理指南](obsidian/pricing-guide.md) ⭐
**Token 计数器 v2.0 价格管理完整指南**

内容概览：
- 智能价格跟踪系统
- 10 个主流模型价格库
- 价格更新流程详解
- 多模型成本对比工具
- 实际应用案例分析
- FAQ 与最佳实践

**适合阅读对象**：
- 使用 Token 计数器
- 需要成本优化
- 维护价格数据

**核心价值**：
- 自动过期检测（30天提醒）
- 版本控制机制
- 便捷更新流程
- qwen-max 降价 47% 分析

---

### 测试报告

#### [插件集成测试报告](reports/20251114-testing-plugin-integration.md) ⭐ **最新**
**Obsidian AI Assistant 插件集成测试完整报告**

内容概览：
- 测试结果总览（16/16 通过）
- API 端点测试详情
- Obsidian 插件集成测试
- 性能分析与对比
- 发现的 4 个问题详解
- 下一步行动计划

**关键数据**：
- API 响应时间：1.9秒（超预期 5倍）
- 测试通过率：100%
- 整体评价：良好（70/100）
- 发布建议：内部 Beta 测试就绪

**适合阅读对象**：
- 了解插件测试进度
- 查看发现的问题
- 规划下一步开发

---

### 开发文档（预留）

以下文档计划添加：

- [ ] **贡献指南** (`development/contributing.md`)
  - 代码规范
  - 提交流程
  - 测试要求

- [ ] **架构文档** (`development/architecture.md`)
  - 系统架构图
  - 模块设计
  - 数据流

- [ ] **API 文档** (`development/api.md`)
  - 核心 API 参考
  - 使用示例
  - 最佳实践

## 🔗 快速链接

### 核心文档
- [项目主 README](../README.md)
- [Obsidian 助手快速开始](../obsidian_assistant/README.md)
- [Notebook 演示](../examples/notebooks/README.md)
- [文档命名规范](NAMING_CONVENTION.md)

### DeepAgents 官方
- [DeepAgents GitHub](https://github.com/langchain-ai/deepagents)
- [LangChain 文档](https://python.langchain.com/)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)

### API 服务
- [通义千问（Qwen）](https://help.aliyun.com/zh/dashscope/)
- [Tavily 搜索](https://tavily.com/)

## 📝 文档贡献

### 添加新文档

1. 在相应目录创建 Markdown 文件
2. 遵循以下格式：

```markdown
# 文档标题

**创建日期**: YYYY-MM-DD  
**维护者**: 姓名  
**版本**: vX.X

## 概述
简要说明文档内容...

## 详细内容
...
```

3. 更新本导航文件的索引
4. 在相关 README 中添加链接

### 文档规范

- 使用清晰的标题层级
- 添加目录（内容较长时）
- 包含代码示例
- 注明创建/更新日期
- 使用表格和图表增强可读性

## 🔄 文档更新记录

| 日期 | 文档 | 更改内容 |
|-----|------|---------|
| 2025-11-14 | 命名规范 | 创建混合命名方案规范文档 |
| 2025-11-14 | 文档重命名 | 所有文档按新规范重命名 |
| 2025-11-14 | 导航索引 | 创建文档导航系统 |
| 2025-11-14 | 对比报告 | 从 obsidian_assistant 移动至此 |
| 2025-11-14 | 优化计划 | 从 obsidian_assistant 移动至此 |
| 2025-11-14 | 测试报告 | ⭐ 新增插件集成测试报告 |

---

**维护者**: YF  
**最后更新**: 2025-11-14 17:50
