# 文档命名规范（混合方案）

**版本**: v1.0  
**制定日期**: 2025-11-14  
**适用范围**: DeepAgents-Obsidian 项目所有文档

---

## 📌 核心原则

1. **自解释性**：文件名应清晰表达内容，无需打开文件
2. **一致性**：同类文档遵循相同命名模式
3. **可搜索性**：支持通过前缀快速定位
4. **可扩展性**：便于添加新文档而不破坏现有结构
5. **版本友好**：重要文档包含版本或日期信息

---

## 🎯 混合命名规则

### 规则 1：索引文档（保持标准）

**用途**：目录级别的主入口文档

**命名规则**：`README.md`（全大写）

**适用场景**：
- 项目根目录
- 各子目录的入口文档
- 模块说明文档

**示例**：
```
/README.md                              # 项目主文档
/docs/README.md                         # 文档索引
/examples/notebooks/README.md           # Notebook 指南
/obsidian_assistant/README.md           # 模块说明
```

**规范**：
- ✅ 必须使用全大写 `README.md`
- ✅ 每个重要目录只有一个 README
- ✅ 内容应包含本目录的概述和导航

---

### 规则 2：模块功能文档（语义化命名）

**用途**：特定模块的功能、指南、对比等文档

**命名规则**：`{module}-{type}-{topic}.md`

**命名元素**：
- `{module}`：模块名（小写，连字符分隔）
  - `obsidian` - Obsidian 助手
  - `deepagents` - DeepAgents 框架
  - `project` - 项目级别
  - `dev` - 开发相关

- `{type}`：文档类型（小写）
  - `guide` - 指南
  - `api` - API 文档
  - `comparison` - 对比分析
  - `architecture` - 架构设计
  - `tutorial` - 教程
  - `reference` - 参考手册

- `{topic}`：具体主题（小写，连字符分隔）
  - `quickstart` - 快速开始
  - `advanced` - 高级用法
  - `troubleshooting` - 故障排除

**示例**：
```
obsidian-guide-quickstart.md            # Obsidian 快速入门指南
obsidian-api-reference.md               # Obsidian API 参考
obsidian-comparison-v2-vs-copilot.md    # Obsidian 对比分析
dev-guide-contributing.md               # 开发贡献指南
dev-architecture-overview.md            # 开发架构概览
project-guide-setup.md                  # 项目设置指南
```

**规范**：
- ✅ 使用小写字母
- ✅ 使用连字符 `-` 分隔单词
- ✅ 模块名在最前，便于文件排序
- ❌ 不使用下划线 `_`
- ❌ 不使用空格或中文

---

### 规则 3：版本化文档（带版本号）

**用途**：有明确版本的计划、优化方案等

**命名规则**：`{module}-{type}-{topic}-v{version}.md`

**版本格式**：
- `v1.0`, `v2.0`, `v2.1` - 主要版本
- `v2.1.0`, `v2.1.1` - 详细版本（可选）

**示例**：
```
obsidian-optimization-plan-v2.1.md      # V2.1 优化计划
obsidian-changelog-v2.0.md              # V2.0 更新日志
deepagents-integration-guide-v1.0.md    # V1.0 集成指南
```

**规范**：
- ✅ 版本号使用 `v` 前缀
- ✅ 主版本号必须，次版本号可选
- ✅ 版本号在文件名末尾（扩展名前）
- ✅ 大版本更新时，旧版本移至 `archive/` 目录

---

### 规则 4：时间记录文档（日期前缀）

**用途**：周期性报告、更新日志、会议记录等

**命名规则**：`YYYYMMDD-{type}-{topic}.md`

**日期格式**：
- `YYYYMMDD` - 年月日，无分隔符
- 例如：`20251114` 表示 2025年11月14日

**文档类型**：
- `summary` - 总结
- `report` - 报告
- `changelog` - 更新日志
- `meeting` - 会议记录
- `review` - 回顾

**示例**：
```
20251114-summary-optimization.md        # 2025-11-14 优化总结
20251113-report-performance.md          # 2025-11-13 性能报告
20251112-changelog-release.md           # 2025-11-12 发布日志
202511-review-monthly.md                # 2025-11 月度回顾
```

**规范**：
- ✅ 日期使用 ISO 格式（YYYYMMDD 或 YYYYMM）
- ✅ 日期在最前，按时间自然排序
- ✅ 类型和主题使用小写连字符
- ✅ 归档时保持文件名不变

---

### 规则 5：长期参考文档（简单命名）

**用途**：长期维护、内容稳定的文档

**命名规则**：`{topic}.md` 或 `{topic}-{subtopic}.md`

**适用文档**：
- 贡献指南（contributing.md）
- 许可证（LICENSE.md）
- 行为准则（code-of-conduct.md）
- 安全政策（security.md）
- 支持信息（support.md）

**示例**：
```
contributing.md                         # 贡献指南
license.md                              # 许可证
code-of-conduct.md                      # 行为准则
security.md                             # 安全政策
troubleshooting.md                      # 故障排除
```

**规范**：
- ✅ 使用小写
- ✅ 常用词汇优先（如 contributing 而非 contribution-guide）
- ✅ 内容相对稳定，不频繁更新
- ❌ 不需要模块前缀

---

### 规则 6：配置和规范文档（全大写）

**用途**：项目级别的重要规范、配置文档

**命名规则**：`{TYPE}_{TOPIC}.md` 或 `{TYPE}.md`

**适用文档**：
- 命名规范（NAMING_CONVENTION.md）
- 代码规范（CODE_STYLE.md）
- 发布流程（RELEASE_PROCESS.md）

**示例**：
```
NAMING_CONVENTION.md                    # 命名规范
CODE_STYLE.md                          # 代码风格
RELEASE_PROCESS.md                     # 发布流程
CONTRIBUTING.md                        # 贡献指南（可大写）
CHANGELOG.md                           # 变更日志（可大写）
```

**规范**：
- ✅ 使用全大写
- ✅ 使用下划线 `_` 分隔（全大写时推荐）
- ✅ 放在明显位置（通常在根目录或 docs/）
- ✅ 内容为项目级别的重要规范

---

## 📂 目录结构与命名示例

### 完整示例

```
deepagents/
├── README.md                                      # 规则1：索引文档
├── LICENSE.md                                     # 规则5：长期文档
│
├── docs/
│   ├── README.md                                 # 规则1：文档索引
│   ├── NAMING_CONVENTION.md                      # 规则6：规范文档
│   ├── CONTRIBUTING.md                           # 规则6：贡献指南
│   │
│   ├── obsidian/
│   │   ├── obsidian-guide-quickstart.md          # 规则2：功能文档
│   │   ├── obsidian-api-reference.md             # 规则2：API 文档
│   │   ├── obsidian-comparison-v2-vs-copilot.md  # 规则2：对比分析
│   │   ├── obsidian-optimization-plan-v2.1.md    # 规则3：版本化文档
│   │   └── obsidian-changelog-v2.0.md            # 规则3：版本日志
│   │
│   ├── development/
│   │   ├── dev-guide-contributing.md             # 规则2：开发指南
│   │   ├── dev-architecture-overview.md          # 规则2：架构文档
│   │   ├── dev-api-deepagents.md                 # 规则2：API 文档
│   │   └── troubleshooting.md                    # 规则5：故障排除
│   │
│   ├── reports/
│   │   ├── 20251114-summary-optimization.md      # 规则4：时间记录
│   │   ├── 20251113-report-performance.md        # 规则4：性能报告
│   │   └── 202511-review-monthly.md              # 规则4：月度回顾
│   │
│   └── archive/                                  # 历史文档归档
│       ├── obsidian-optimization-plan-v2.0.md
│       └── 20251001-summary-initial.md
│
├── examples/
│   └── notebooks/
│       ├── README.md                             # 规则1：索引文档
│       └── notebooks-guide-setup.md              # 规则2：设置指南
│
└── obsidian_assistant/
    └── README.md                                 # 规则1：模块说明
```

---

## 🔄 文档生命周期管理

### 新建文档

1. **确定文档类型**：参考上述 6 条规则
2. **选择命名模式**：根据文档用途选择合适规则
3. **检查重复**：确保不与现有文档冲突
4. **更新索引**：在相应的 README.md 中添加链接

### 更新文档

1. **小更新**：直接修改，更新文档内的版本号/日期
2. **大版本更新**：
   - 创建新版本文件（如 `v2.1` → `v2.2`）
   - 旧版本移至 `archive/` 目录
   - 更新所有引用链接

### 归档文档

**归档条件**：
- 文档内容已过时
- 新版本已发布
- 不再被其他文档引用

**归档流程**：
```bash
# 移动到归档目录
mv docs/obsidian/obsidian-optimization-plan-v2.0.md \
   docs/archive/obsidian/obsidian-optimization-plan-v2.0.md

# 或按年份归档
mv docs/reports/20241015-report-test.md \
   docs/archive/2024/20241015-report-test.md
```

### 删除文档

**删除原则**：谨慎删除，优先归档

**可删除情况**：
- 临时草稿
- 测试文档
- 完全错误的内容

---

## 🎯 快速参考卡片

### 我应该使用什么命名？

| 文档用途 | 命名规则 | 示例 |
|---------|---------|------|
| 目录索引 | `README.md` | `docs/README.md` |
| 功能指南 | `{module}-guide-{topic}.md` | `obsidian-guide-quickstart.md` |
| API 文档 | `{module}-api-{scope}.md` | `obsidian-api-reference.md` |
| 对比分析 | `{module}-comparison-{detail}.md` | `obsidian-comparison-v2-vs-copilot.md` |
| 版本计划 | `{module}-{type}-{topic}-v{ver}.md` | `obsidian-optimization-plan-v2.1.md` |
| 时间报告 | `YYYYMMDD-{type}-{topic}.md` | `20251114-summary-optimization.md` |
| 长期文档 | `{topic}.md` | `contributing.md` |
| 规范文档 | `{TYPE}_{TOPIC}.md` | `NAMING_CONVENTION.md` |

### 命名检查清单

- [ ] 使用小写字母（除非是规则6）
- [ ] 使用连字符 `-` 分隔单词
- [ ] 模块名在最前（如果适用）
- [ ] 包含版本号（如果是版本化文档）
- [ ] 包含日期（如果是时间记录）
- [ ] 文件名自解释，无需打开即知内容
- [ ] 不使用空格、下划线（除全大写文档）
- [ ] 不使用中文或特殊字符

---

## 📝 常见场景示例

### 场景 1：创建新的优化方案

```bash
# ✅ 推荐
docs/obsidian/obsidian-optimization-plan-v2.2.md

# ❌ 不推荐
docs/obsidian/optimization_plan_v2.2.md
docs/obsidian/v2.2优化计划.md
docs/obsidian/Optimization Plan V2.2.md
```

### 场景 2：添加每周进度报告

```bash
# ✅ 推荐
docs/reports/20251118-report-weekly-progress.md

# ❌ 不推荐
docs/reports/weekly_report_2025_11_18.md
docs/reports/Week47-2025-Progress.md
```

### 场景 3：创建新模块的快速入门

```bash
# ✅ 推荐
docs/newmodule/newmodule-guide-quickstart.md

# ❌ 不推荐
docs/newmodule/QuickStartGuide.md
docs/newmodule/quick_start.md
docs/newmodule/README-quickstart.md
```

### 场景 4：编写测试文档

```bash
# ✅ 推荐（长期参考）
docs/development/testing.md

# ✅ 推荐（模块特定）
docs/development/dev-guide-testing.md

# ❌ 不推荐
docs/development/TEST.md
docs/development/Testing_Guide.md
```

---

## 🔧 重命名现有文档

如果需要将现有文档重命名以符合规范：

```bash
# 重命名命令（示例）
mv old-name.md new-name.md

# 批量更新引用（使用 sed 或编辑器的查找替换）
grep -r "old-name.md" . --include="*.md" | while read -r line; do
    # 手动或脚本替换
done
```

**重命名后必做**：
1. 更新所有引用该文档的链接
2. 更新 README.md 中的索引
3. 提交 git 时说明重命名原因

---

## 🌐 多语言文档（未来扩展）

如需支持多语言：

```bash
# 方案1：后缀标识
obsidian-guide-quickstart.md         # 默认（英文或中文）
obsidian-guide-quickstart.en.md      # 英文版
obsidian-guide-quickstart.zh.md      # 中文版

# 方案2：目录分离
docs/en/obsidian/obsidian-guide-quickstart.md
docs/zh/obsidian/obsidian-guide-quickstart.md
```

---

## 📞 反馈与改进

本命名规范是一个活文档（living document），如有以下情况请更新：

1. 发现规则不适用的场景
2. 有更好的命名建议
3. 项目规模变化需要调整规则

**更新流程**：
1. 在本文档末尾的"变更记录"部分添加条目
2. 更新版本号
3. 通知团队成员

---

## 📊 变更记录

| 版本 | 日期 | 变更内容 | 变更人 |
|------|------|---------|--------|
| v1.0 | 2025-11-14 | 初始版本，制定混合命名方案 | YF |

---

**维护者**: YF  
**最后更新**: 2025-11-14  
**下次审查**: 2026-02-14（3个月后）

