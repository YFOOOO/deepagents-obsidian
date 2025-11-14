# 文档命名快速参考卡片 🚀

**快速查询表**，创建新文档时使用。详细规则请查看 [NAMING_CONVENTION.md](NAMING_CONVENTION.md)

---

## 🎯 我应该用什么命名？

### 1️⃣ 目录索引
```
✅ README.md
```
用于：每个目录的主入口文档

### 2️⃣ 功能指南
```
✅ {module}-guide-{topic}.md

示例：
obsidian-guide-quickstart.md
obsidian-guide-advanced.md
dev-guide-contributing.md
```
用于：使用指南、教程

### 3️⃣ API 文档
```
✅ {module}-api-{scope}.md

示例：
obsidian-api-reference.md
obsidian-api-tools.md
dev-api-deepagents.md
```
用于：API 参考、接口文档

### 4️⃣ 对比分析
```
✅ {module}-comparison-{detail}.md

示例：
obsidian-comparison-v2-vs-copilot.md
deepagents-comparison-langgraph-vs-crewai.md
```
用于：功能对比、方案对比

### 5️⃣ 架构文档
```
✅ {module}-architecture-{aspect}.md

示例：
obsidian-architecture-overview.md
dev-architecture-middleware.md
project-architecture-system.md
```
用于：架构设计、系统设计

### 6️⃣ 版本化文档
```
✅ {module}-{type}-{topic}-v{version}.md

示例：
obsidian-optimization-plan-v2.1.md
obsidian-changelog-v2.0.md
deepagents-integration-guide-v1.0.md
```
用于：有版本的计划、日志

### 7️⃣ 时间报告
```
✅ YYYYMMDD-{type}-{topic}.md

示例：
20251114-summary-optimization.md
20251113-report-performance.md
202511-review-monthly.md
```
用于：周报、月报、总结

### 8️⃣ 长期文档
```
✅ {topic}.md

示例：
contributing.md
troubleshooting.md
security.md
```
用于：稳定的参考文档

### 9️⃣ 规范文档
```
✅ {TYPE}_{TOPIC}.md 或 {TYPE}.md

示例：
NAMING_CONVENTION.md
CODE_STYLE.md
CONTRIBUTING.md
```
用于：项目级别的规范

---

## ✅ 命名检查清单

创建新文档前，快速检查：

- [ ] 使用小写字母（除非是规范文档）
- [ ] 使用连字符 `-` 分隔单词
- [ ] 不使用空格、下划线（除全大写）
- [ ] 不使用中文或特殊字符
- [ ] 模块名在最前（如适用）
- [ ] 包含版本号（如是版本化文档）
- [ ] 包含日期（如是时间记录）
- [ ] 文件名能自解释内容

---

## ❌ 常见错误

| ❌ 错误 | ✅ 正确 |
|--------|--------|
| `Quick Start.md` | `{module}-guide-quickstart.md` |
| `optimization_plan.md` | `{module}-optimization-plan-v{X}.md` |
| `测试文档.md` | `{module}-guide-testing.md` |
| `API.md` | `{module}-api-reference.md` |
| `v2.1优化.md` | `{module}-optimization-plan-v2.1.md` |
| `Comparison_Report.md` | `{module}-comparison-{detail}.md` |
| `2025-11-14-report.md` | `20251114-report-{topic}.md` |

---

## 📂 示例目录结构

```
docs/
├── README.md                                      # 索引
├── NAMING_CONVENTION.md                           # 规范
├── CONTRIBUTING.md                                # 贡献
│
├── obsidian/
│   ├── obsidian-guide-quickstart.md              # 指南
│   ├── obsidian-api-reference.md                 # API
│   ├── obsidian-comparison-v2-vs-copilot.md      # 对比
│   ├── obsidian-optimization-plan-v2.1.md        # 版本计划
│   └── obsidian-changelog-v2.0.md                # 版本日志
│
├── development/
│   ├── dev-guide-contributing.md                 # 开发指南
│   ├── dev-architecture-overview.md              # 架构
│   └── troubleshooting.md                        # 长期文档
│
└── reports/
    ├── 20251114-summary-optimization.md          # 总结
    └── 202511-review-monthly.md                  # 月报
```

---

## 🔧 重命名工具

```bash
# 重命名文件
mv old-name.md new-name.md

# 更新引用（在项目根目录执行）
grep -r "old-name.md" . --include="*.md"

# 批量查找并替换（使用 sed）
sed -i '' 's/old-name.md/new-name.md/g' file.md
```

---

## 💡 快速决策树

```
开始
 ↓
是目录索引吗？
 ├─ 是 → README.md
 └─ 否 ↓
是规范类文档吗？
 ├─ 是 → UPPERCASE_NAME.md
 └─ 否 ↓
是时间相关报告吗？
 ├─ 是 → YYYYMMDD-type-topic.md
 └─ 否 ↓
是长期稳定文档吗？
 ├─ 是 → topic.md
 └─ 否 ↓
有版本号吗？
 ├─ 是 → module-type-topic-vX.X.md
 └─ 否 ↓
是功能/指南类文档吗？
 └─ 是 → module-type-topic.md
```

---

## 📞 需要帮助？

- **详细规则**: [NAMING_CONVENTION.md](NAMING_CONVENTION.md)
- **示例参考**: 查看 `docs/obsidian/` 目录
- **有疑问**: 提交 Issue 或联系维护者

---

**最后更新**: 2025-11-14  
**维护者**: YF
