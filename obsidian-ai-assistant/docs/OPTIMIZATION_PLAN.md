# Obsidian AI Assistant - 优化计划

**版本**: 0.1.0 → 0.2.0  
**规划日期**: 2025-11-14  
**目标**: 修复核心问题，提升用户体验

---

## 📊 测试结果总结

### 已验证功能 ✅
- API 端点全部通过 (3/3)
- 插件成功加载和启用
- 基本对话功能正常
- 本地笔记搜索准确
- 性能超预期（1.9秒响应）

### 发现的问题 ⚠️
1. **P0 - 内部链接无法跳转** 🔥
2. **P1 - 缺少复制/插入功能** 📋
3. **P2 - 参考来源重复显示** 🐛
4. **P2 - 界面语言不可配置** 🌐
5. **P3 - Token 统计未显示** 📊

---

## 🎯 优化目标

### 第一阶段：修复核心问题（本周，11.15-11.17）

#### 任务 1: 修复内部链接跳转 🔥 **最高优先级**

**问题描述**:
- 回答中的笔记引用无法点击
- 只在尾部显示来源，且点击无效
- 缺少 Obsidian 内部链接的核心体验

**根本原因分析**:
```typescript
// 当前问题：使用 innerHTML 直接渲染文本
messageDiv.innerHTML = marked.parse(message.content);

// 问题：
// 1. marked.parse() 会将 [[link]] 转为普通文本或 <a> 标签
// 2. Obsidian 的 [[]] 语法不会被识别
// 3. 没有使用 Obsidian 的 MarkdownRenderer API
```

**解决方案**:

**步骤 1: 修改后端响应格式**
```python
# 在 obsidian_assistant.py 中
# 确保返回正确的 Obsidian 链接格式

def format_note_reference(note_path: str, note_title: str) -> str:
    """
    生成 Obsidian 内部链接格式
    
    Args:
        note_path: 笔记相对路径，如 "Obsidian_Knowledge/欢迎.md"
        note_title: 显示标题，如 "欢迎"
    
    Returns:
        格式化的内部链接，如 "[[Obsidian_Knowledge/欢迎|欢迎]]"
    """
    # 移除 .md 后缀
    clean_path = note_path.replace('.md', '')
    return f"[[{clean_path}|{note_title}]]"

# 在生成回答时使用
answer = f"根据您的笔记 {format_note_reference(path, title)} 中提到..."
```

**步骤 2: 修改前端渲染逻辑**
```typescript
// 在 chat-view.ts 中
// 使用 Obsidian 的 MarkdownRenderer

import { MarkdownRenderer } from 'obsidian';

async renderMessage(message: Message) {
    const messageDiv = this.containerEl.createDiv('message');
    
    // 不要使用 innerHTML！
    // messageDiv.innerHTML = marked.parse(message.content);
    
    // 使用 Obsidian 的 MarkdownRenderer
    await MarkdownRenderer.renderMarkdown(
        message.content,
        messageDiv,
        '', // sourcePath
        this // component
    );
}
```

**步骤 3: 测试验证**
- [ ] 后端返回包含 `[[path|title]]` 格式的回答
- [ ] 前端正确渲染为可点击的内部链接
- [ ] 点击链接能跳转到对应笔记
- [ ] 悬停显示完整路径预览

**预计时间**: 4-6 小时

**验收标准**:
- ✅ 回答中的笔记名称显示为蓝色内部链接
- ✅ 点击链接跳转到对应笔记
- ✅ Ctrl/Cmd+点击在新标签页打开
- ✅ 悬停显示笔记预览

---

#### 任务 2: 添加复制和插入功能 📋 **高优先级**

**问题描述**:
- 用户需要手动选择和复制回答
- 无法快速插入回答到当前笔记
- 降低工作流效率

**解决方案**:

**步骤 1: 设计按钮 UI**
```
┌─────────────────────────────────────┐
│ AI Assistant                    🤖  │
├─────────────────────────────────────┤
│ 🟢 Connected                        │
├─────────────────────────────────────┤
│                                      │
│ 👤 You:                             │
│ 你好，测试一下                        │
│                                      │
│ 🤖 AI:                   [📋] [📝]  │ ← 添加按钮
│ 你好！我是你的AI助手...               │
│                                      │
│ Sources:                             │
│ • [[欢迎.md|欢迎]]                   │
└─────────────────────────────────────┘

📋 = 复制按钮
📝 = 插入按钮
```

**步骤 2: 实现复制功能**
```typescript
// 在 chat-view.ts 中

private addCopyButton(messageDiv: HTMLElement, content: string) {
    const buttonContainer = messageDiv.createDiv('message-actions');
    
    // 复制按钮
    const copyBtn = buttonContainer.createEl('button', {
        text: '📋 Copy',
        cls: 'copy-btn'
    });
    
    copyBtn.addEventListener('click', async () => {
        await navigator.clipboard.writeText(content);
        
        // 显示成功提示
        copyBtn.setText('✅ Copied!');
        setTimeout(() => {
            copyBtn.setText('📋 Copy');
        }, 2000);
    });
}
```

**步骤 3: 实现插入功能**
```typescript
private addInsertButton(messageDiv: HTMLElement, content: string) {
    const insertBtn = buttonContainer.createEl('button', {
        text: '📝 Insert',
        cls: 'insert-btn'
    });
    
    insertBtn.addEventListener('click', () => {
        // 获取当前活动编辑器
        const activeView = this.app.workspace.getActiveViewOfType(MarkdownView);
        if (!activeView) {
            new Notice('No active note to insert into');
            return;
        }
        
        // 在光标位置插入
        const editor = activeView.editor;
        editor.replaceSelection(content);
        
        // 显示成功提示
        new Notice('✅ Inserted into current note');
    });
}
```

**步骤 4: 添加样式**
```css
/* 在 styles.css 中 */

.message-actions {
    position: absolute;
    top: 8px;
    right: 8px;
    display: flex;
    gap: 4px;
    opacity: 0;
    transition: opacity 0.2s;
}

.message:hover .message-actions {
    opacity: 1;
}

.copy-btn, .insert-btn {
    padding: 4px 8px;
    font-size: 12px;
    border: 1px solid var(--background-modifier-border);
    border-radius: 4px;
    background: var(--background-primary);
    cursor: pointer;
}

.copy-btn:hover, .insert-btn:hover {
    background: var(--background-modifier-hover);
}
```

**预计时间**: 2-3 小时

**验收标准**:
- ✅ 每条回答显示复制和插入按钮
- ✅ 鼠标悬停时按钮可见
- ✅ 复制功能正常，显示成功提示
- ✅ 插入功能能在光标位置插入内容
- ✅ 按钮样式符合 Obsidian 主题

---

### 第二阶段：优化体验（下周，11.18-11.22）

#### 任务 3: 修复参考来源重复显示 🐛

**问题描述**:
- "参考来源" / "Sources:" 出现两次
- 第一次下方为空
- 第二次才显示实际内容

**解决方案**:

**方案 A: 后端清理（推荐）**
```python
# 在 api_server.py 的 /query 端点

import re

def clean_answer(answer: str) -> str:
    """移除回答中的参考来源部分（由前端单独显示）"""
    # 移除中文"参考来源"及之后的内容
    answer = re.sub(r'\n+参考来源.*$', '', answer, flags=re.DOTALL)
    # 移除英文"Sources:"及之后的内容
    answer = re.sub(r'\n+Sources:.*$', '', answer, flags=re.DOTALL)
    # 移除"参考文献"等类似表述
    answer = re.sub(r'\n+参考文献.*$', '', answer, flags=re.DOTALL)
    answer = re.sub(r'\n+References:.*$', '', answer, flags=re.DOTALL)
    return answer.strip()

# 在返回前清理
answer = clean_answer(result.get("answer", ""))
```

**预计时间**: 1 小时

**验收标准**:
- ✅ 回答内容不包含"参考来源"/"Sources:"
- ✅ 来源只在底部单独显示一次
- ✅ 不影响其他内容

---

#### 任务 4: 添加多语言界面支持 🌐

**问题描述**:
- 助理开场白固定英文
- UI 文本不支持中文
- 中文用户体验不佳

**解决方案**:

**步骤 1: 添加语言设置**
```typescript
// 在 settings.ts 中

interface AIAssistantSettings {
    apiUrl: string;
    apiKey: string;
    model: string;
    language: 'en' | 'zh-CN' | 'auto'; // 新增
    enableCache: boolean;
    enableSmartRouting: boolean;
}

DEFAULT_SETTINGS: AIAssistantSettings = {
    apiUrl: 'http://localhost:8000',
    apiKey: '',
    model: 'qwen-turbo',
    language: 'auto', // 默认跟随系统
    enableCache: true,
    enableSmartRouting: true
}
```

**步骤 2: 创建多语言文本**
```typescript
// 创建 src/i18n.ts

export const i18n = {
    en: {
        welcome: "Hello! I'm your AI assistant. Ask me anything about your notes or general questions.",
        connected: "Connected",
        disconnected: "Disconnected",
        send: "Send",
        copy: "Copy",
        copied: "Copied!",
        insert: "Insert",
        sources: "Sources:",
        // ...
    },
    'zh-CN': {
        welcome: "你好！我是你的AI助手。您可以问我关于笔记或任何问题。",
        connected: "已连接",
        disconnected: "未连接",
        send: "发送",
        copy: "复制",
        copied: "已复制！",
        insert: "插入",
        sources: "参考来源：",
        // ...
    }
};

export function t(key: string, lang: string = 'en'): string {
    return i18n[lang]?.[key] || i18n['en'][key] || key;
}
```

**步骤 3: 使用多语言文本**
```typescript
// 在 chat-view.ts 中

import { t } from './i18n';

private renderWelcomeMessage() {
    const lang = this.plugin.settings.language === 'auto' 
        ? navigator.language 
        : this.plugin.settings.language;
    
    const welcomeMsg = t('welcome', lang);
    // 使用翻译后的文本
}
```

**预计时间**: 2-3 小时

**验收标准**:
- ✅ 设置中有语言选项（English / 中文 / Auto）
- ✅ 切换语言后界面文本更新
- ✅ 开场白使用所选语言
- ✅ Auto 模式跟随系统语言

---

### 第三阶段：增强功能（两周内，11.23-12.06）

#### 任务 5: 添加 Token 统计显示 📊

**当前问题**:
- 后端返回了 Token 数据
- 前端未显示

**解决方案**:
```typescript
// 在回答底部显示
// Tokens: 156 input + 89 output = 245 total (¥0.0003)
```

**预计时间**: 1-2 小时

---

#### 任务 6: 添加缓存指示 ⚡

**功能说明**:
- 缓存命中时显示 ⚡ 标记
- 提示用户响应来自缓存

**预计时间**: 1 小时

---

#### 任务 7: 错误处理优化 🛡️

**改进点**:
- 超时提示更友好
- 网络错误重试机制
- 后端错误详细提示

**预计时间**: 2-3 小时

---

## 📅 时间计划

### 本周（11.15-11.17，3天）
- [ ] **Day 1 (周五)**: 修复内部链接跳转（4-6h）
- [ ] **Day 2 (周六)**: 实现复制/插入功能（2-3h）
- [ ] **Day 3 (周日)**: 修复来源重复 + 测试（2h）

**本周目标**: 完成 P0 和 P1 问题修复

### 下周（11.18-11.22，5天）
- [ ] **Day 1-2**: 多语言支持（2-3h）
- [ ] **Day 3-5**: Token 统计、缓存指示、错误处理（4-6h）

**下周目标**: 完成 P2 和 P3 优化

### 第三周（11.23-11.29）
- [ ] 内部 Beta 测试
- [ ] 收集反馈
- [ ] Bug 修复

---

## 🎯 里程碑

### v0.1.1 (本周末，11.17)
**目标**: 修复核心功能缺陷
- ✅ 内部链接可以跳转
- ✅ 支持复制和插入
- ✅ 来源显示优化

**发布状态**: 内部测试版

---

### v0.2.0 (下周末，11.22)
**目标**: 完善用户体验
- ✅ 多语言界面
- ✅ Token 统计显示
- ✅ 缓存指示
- ✅ 错误处理优化

**发布状态**: Beta 测试版

---

### v0.3.0 (一个月后，12.14)
**目标**: 公开发布准备
- ✅ Beta 反馈修复
- ✅ 性能优化
- ✅ 文档完善
- ✅ 演示视频

**发布状态**: 候选发布版

---

## 📊 成功指标

### 功能完整性
- [ ] 所有 P0 和 P1 问题已修复
- [ ] 核心功能测试通过率 100%
- [ ] 无阻塞性 bug

### 用户体验
- [ ] 响应时间 < 3 秒
- [ ] UI 流畅不卡顿
- [ ] 错误提示友好明确

### 代码质量
- [ ] TypeScript 无编译错误
- [ ] ESLint 检查通过
- [ ] 代码注释完善

---

## 🚀 下一步行动

### 立即开始（今天）

**任务**: 修复内部链接跳转功能

**步骤**:
1. [ ] 检查当前后端响应格式
2. [ ] 修改链接生成逻辑
3. [ ] 更新前端渲染方式
4. [ ] 测试验证

**预计完成时间**: 今晚或明天

---

## ❓ 待确认问题

### 需要用户确认

1. **是否继续其他测试？**
   - 网页搜索测试（需要 TAVILY_API_KEY）
   - 设置修改测试
   - 错误处理测试
   - 性能压力测试

2. **优化优先级是否同意？**
   - P0: 内部链接 > P1: 复制/插入 > P2: 其他

3. **发布时间线是否合理？**
   - 本周修复核心问题
   - 下周完善体验
   - 一个月后公开发布

4. **是否需要添加其他功能？**
   - 对话历史保存？
   - 导出对话记录？
   - 快捷键支持？

---

**文档创建时间**: 2025-11-14 17:35  
**负责人**: YF  
**状态**: 等待确认开始执行
