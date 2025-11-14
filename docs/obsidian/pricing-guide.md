# Token 计数器价格管理指南 v2.0

## 📋 概述

Token 计数器已升级到 v2.0 版本，提供智能价格管理和多模型支持。

## 🎯 核心功能

### 1. 自动价格跟踪

- ✅ **版本控制**: 每次更新都有版本号和时间戳
- ⚠️ **过期提醒**: 超过30天未更新自动警告
- 📋 **多模型支持**: Qwen 全系列 + 主流厂商
- 🔄 **便捷更新**: 修改字典即可

### 2. 价格数据库

**当前版本**: v2.0  
**更新日期**: 2025-11-14  
**数据来源**: [阿里云百炼官方文档](https://help.aliyun.com/zh/model-studio/models)

**支持的模型** (10个):

#### Qwen 商用系列
- `qwen-turbo`: ¥0.3/¥0.6 (百万Token) - 极速版
- `qwen-plus`: ¥0.8/¥2.0 - 平衡版  
- `qwen-max`: ¥3.2/¥12.8 - 旗舰版 ⚡ **已降价47%**
- `qwen3-max`: ¥3.2/¥12.8 - 最新旗舰版
- `qwen-long`: ¥0.5/¥2.0 - 超长文档版 (10M上下文)

#### Qwen 开源系列
- `qwen2.5-72b-instruct`: ¥4.0/¥12.0
- `qwen2.5-32b-instruct`: ¥2.0/¥6.0

#### 其他厂商
- `deepseek-v3`: ¥2.0/¥8.0
- `kimi-k2`: ¥4.0/¥16.0  
- `glm-4.5`: ¥3.0/¥14.0

## 🔧 使用方法

### 基础使用

```python
from obsidian_assistant.token_counter import TokenCounter

# 创建计数器（会自动检查价格新鲜度）
counter = TokenCounter(model="qwen-turbo")
```

### 查看所有模型

```python
from obsidian_assistant.token_counter import list_available_models

list_available_models()
```

### 对比模型成本

```python
from obsidian_assistant.token_counter import compare_model_costs

# 对比不同模型在同样任务下的成本
compare_model_costs(
    prompt_tokens=500,
    completion_tokens=300,
    models=["qwen-turbo", "qwen-plus", "qwen-max"]
)
```

### 获取价格详情

```python
from obsidian_assistant.token_counter import get_pricing_info

info = get_pricing_info("qwen-max")
print(info)
# 输出: {
#   "input": 0.0032,
#   "output": 0.0128,
#   "description": "旗舰版，能力最强 (价格已降低47%)",
#   "context": "262K tokens",
#   "updated": "2025-11-14",
#   "note": "2025年11月降价: 从¥6/¥24降至¥3.2/¥12.8"
# }
```

## 📊 价格更新流程

### 方案一：手动更新（推荐）

1. **查看官方文档**  
   访问: https://help.aliyun.com/zh/model-studio/models

2. **更新价格数据**  
   编辑 `token_counter.py` 中的 `MODEL_PRICING` 字典:
   
   ```python
   MODEL_PRICING = {
       "model-name": {
           "input": 0.001,     # 输入价格 (元/千Token)
           "output": 0.002,    # 输出价格 (元/千Token)
           "description": "模型描述",
           "context": "上下文长度",
           "updated": "2025-11-14"  # ⚠️ 必须更新此字段
       }
   }
   ```

3. **更新版本信息**
   
   ```python
   PRICING_LAST_UPDATE = "2025-11-14"  # 更新日期
   ```

4. **验证更新**
   
   ```python
   from obsidian_assistant.token_counter import list_available_models
   list_available_models()  # 检查是否显示"✅ 价格数据新鲜"
   ```

### 方案二：自动化脚本（待实现）

未来可以开发自动爬取官网价格的脚本：

```python
# 伪代码
def fetch_latest_pricing():
    """从官网 API 或页面获取最新价格"""
    # 1. 调用官方 API 或爬取定价页面
    # 2. 解析价格数据
    # 3. 更新 MODEL_PRICING 字典
    # 4. 自动更新 PRICING_LAST_UPDATE
    pass
```

**限制**: 阿里云目前没有公开的价格查询 API，需要定期手动核实。

## 🎯 实际应用案例

### 案例1: Obsidian 助手成本优化

**场景**: 100次/天的查询量

| 策略 | 模型 | 月成本 | 适用场景 |
|------|------|--------|---------|
| 经济模式 | qwen-turbo | ¥0.9 | 日常查询 |
| 平衡模式 | qwen-plus | ¥2.5 | 复杂问答 |
| 专业模式 | qwen-max | ¥9.0 | 深度分析 |

**推荐**: 
- 默认使用 `qwen-turbo` (节省 90% 成本)
- 复杂任务临时切换到 `qwen-max`

### 案例2: qwen-max 降价影响分析

**2025年11月降价前后对比**:

| Token消耗 | 降价前 | 降价后 | 节省 |
|----------|--------|--------|------|
| 1万 input + 1万 output | ¥0.30 | ¥0.16 | 47% |
| 10万 input + 10万 output | ¥3.00 | ¥1.60 | 47% |

**结论**: qwen-max 现在更具性价比，适合需要高质量输出的场景。

## 📝 常见问题

### Q1: 为什么我的成本计算不准确？

**A**: 可能原因：
1. 价格数据过期 → 运行 `list_available_models()` 检查
2. Token 估算偏差 → 使用实际 API 返回的 token 数
3. 模型名称错误 → 参考支持列表

### Q2: 如何获取最准确的价格？

**A**: 
1. 官方文档: https://help.aliyun.com/zh/model-studio/models
2. 咨询阿里云客服
3. 使用小额度测试实际扣费

### Q3: 支持添加自定义模型吗？

**A**: 完全支持！在 `MODEL_PRICING` 中添加新条目即可：

```python
MODEL_PRICING["my-custom-model"] = {
    "input": 0.001,
    "output": 0.002,
    "description": "自定义模型",
    "updated": "2025-11-14"
}
```

### Q4: 价格库会自动更新吗？

**A**: 目前是手动更新机制，因为：
- 阿里云没有公开的价格 API
- 手动更新更可控，避免误差
- 添加了过期检测，超过30天会提醒

## 🔮 未来规划

- [ ] 开发价格爬虫脚本（定期自动更新）
- [ ] 集成更多模型厂商（OpenAI, Anthropic 等）
- [ ] 添加价格趋势分析
- [ ] 成本预警功能（超过预算自动提醒）
- [ ] 支持批量调用折扣计算

## 📞 技术支持

- **文档**: 本文件
- **示例**: `examples/notebooks/obsidian_V2.0_test_with_tokens.ipynb`
- **源码**: `obsidian_assistant/token_counter.py`

---

**更新日志**:
- v2.0 (2025-11-14): 多模型支持、价格版本控制、过期检测
- v1.0 (2025-11-13): 基础 token 计数功能
