"""
Token 计数器工具 v2.0 - 实时监控 LLM Token 消耗
- 支持多模型价格管理
- 自动价格过期检测
- 价格数据版本控制
"""
import time
import warnings
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class TokenUsage:
    timestamp: str
    question: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    response_time: float
    model: str = "qwen-turbo"
    cost: float = 0.0

# ============================================================================
# 价格数据库 (更新日期: 2025-11-14, 来源: 阿里云百炼官方文档)
# 官方文档: https://help.aliyun.com/zh/model-studio/models
# ============================================================================

MODEL_PRICING = {
    # === Qwen 系列 (通义千问) ===
    "qwen-turbo": {
        "input": 0.0003,   # ¥0.3/百万Token (实际价格)
        "output": 0.0006,  # ¥0.6/百万Token (非思考模式)
        "description": "极速版，速度快成本低",
        "context": "1M tokens",
        "updated": "2025-11-14"
    },
    "qwen-plus": {
        "input": 0.0008,   # ¥0.8/百万Token (0-128K)
        "output": 0.002,   # ¥2/百万Token (非思考模式)
        "description": "平衡版，效果速度成本均衡",
        "context": "1M tokens",
        "updated": "2025-11-14"
    },
    "qwen-max": {
        "input": 0.0032,   # ¥3.2/百万Token (0-32K) ⚡ 已降价!
        "output": 0.0128,  # ¥12.8/百万Token
        "description": "旗舰版，能力最强 (价格已降低47%)",
        "context": "262K tokens",
        "updated": "2025-11-14",
        "note": "2025年11月降价: 从¥6/¥24降至¥3.2/¥12.8"
    },
    "qwen3-max": {
        "input": 0.0032,   # 与 qwen-max 相同
        "output": 0.0128,
        "description": "最新旗舰版",
        "context": "262K tokens",
        "updated": "2025-11-14"
    },
    "qwen-long": {
        "input": 0.0005,   # ¥0.5/百万Token
        "output": 0.002,   # ¥2/百万Token
        "description": "超长文档版，10M上下文",
        "context": "10M tokens",
        "updated": "2025-11-14"
    },
    
    # === 开源版本 ===
    "qwen2.5-72b-instruct": {
        "input": 0.004,
        "output": 0.012,
        "description": "开源72B模型",
        "updated": "2025-11-14"
    },
    "qwen2.5-32b-instruct": {
        "input": 0.002,
        "output": 0.006,
        "description": "开源32B模型",
        "updated": "2025-11-14"
    },
    
    # === 其他厂商模型 (供参考) ===
    "deepseek-v3": {
        "input": 0.002,
        "output": 0.008,
        "description": "DeepSeek V3",
        "updated": "2025-11-14"
    },
    "kimi-k2": {
        "input": 0.004,
        "output": 0.016,
        "description": "Kimi K2",
        "updated": "2025-11-14"
    },
    "glm-4.5": {
        "input": 0.003,
        "output": 0.014,
        "description": "智谱 GLM-4.5",
        "updated": "2025-11-14"
    },
}

# 价格数据版本信息
PRICING_VERSION = "2.0"
PRICING_LAST_UPDATE = "2025-11-14"
PRICING_SOURCE = "阿里云百炼官方文档"
PRICING_WARNING_DAYS = 30  # 超过30天未更新会警告

# ============================================================================
# 价格管理函数
# ============================================================================

def check_pricing_freshness() -> Tuple[bool, int]:
    """检查价格数据是否过期"""
    from datetime import datetime
    last_update = datetime.strptime(PRICING_LAST_UPDATE, "%Y-%m-%d")
    days_old = (datetime.now() - last_update).days
    is_fresh = days_old <= PRICING_WARNING_DAYS
    return is_fresh, days_old

def get_pricing_info(model: str = "qwen-turbo") -> Dict:
    """获取模型价格信息（含元数据）"""
    if model not in MODEL_PRICING:
        warnings.warn(
            f"⚠️  模型 '{model}' 未在价格库中，使用 qwen-turbo 价格作为fallback",
            UserWarning
        )
        model = "qwen-turbo"
    return MODEL_PRICING[model]

def list_available_models() -> None:
    """列出所有支持的模型及价格"""
    print("\n" + "=" * 100)
    print(f"📋 支持的模型价格表 (版本: {PRICING_VERSION}, 更新: {PRICING_LAST_UPDATE})")
    print("=" * 100)
    
    categories = {
        "Qwen 商用系列": ["qwen-turbo", "qwen-plus", "qwen-max", "qwen3-max", "qwen-long"],
        "Qwen 开源系列": ["qwen2.5-72b-instruct", "qwen2.5-32b-instruct"],
        "其他厂商": ["deepseek-v3", "kimi-k2", "glm-4.5"]
    }
    
    for category, models in categories.items():
        print(f"\n🏷️  {category}")
        print("-" * 100)
        for model in models:
            if model in MODEL_PRICING:
                info = MODEL_PRICING[model]
                print(f"  {model:25s} | 输入: ¥{info['input']:.4f}/k | 输出: ¥{info['output']:.4f}/k | {info['description']}")
    
    # 检查价格新鲜度
    is_fresh, days_old = check_pricing_freshness()
    if not is_fresh:
        print(f"\n⚠️  警告: 价格数据已 {days_old} 天未更新，建议核实最新价格！")
    print("=" * 100 + "\n")

def calculate_cost(prompt_tokens: int, completion_tokens: int, model: str = "qwen-turbo") -> float:
    """计算成本（元）"""
    pricing_info = get_pricing_info(model)
    return (prompt_tokens / 1000) * pricing_info["input"] + (completion_tokens / 1000) * pricing_info["output"]

def estimate_tokens(text: str) -> int:
    """估算文本的 Token 数量（中文和英文混合）"""
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    english_words = len([w for w in text.split() if any(c.isalpha() for c in w)])
    return int(chinese_chars * 1.8 + english_words * 1.3) or len(text) // 4

def compare_model_costs(prompt_tokens: int, completion_tokens: int, models: list = None) -> None:
    """比较不同模型的成本"""
    if models is None:
        models = ["qwen-turbo", "qwen-plus", "qwen-max", "qwen3-max"]
    
    print("\n" + "=" * 80)
    print(f"💰 成本对比 (输入: {prompt_tokens:,} tokens, 输出: {completion_tokens:,} tokens)")
    print("=" * 80)
    
    results = []
    for model in models:
        if model in MODEL_PRICING:
            cost = calculate_cost(prompt_tokens, completion_tokens, model)
            info = MODEL_PRICING[model]
            results.append((model, cost, info['description']))
    
    # 按成本排序
    results.sort(key=lambda x: x[1])
    
    for i, (model, cost, desc) in enumerate(results):
        icon = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "  "
        print(f"{icon} {model:20s} | ¥{cost:.4f} | {desc}")
    
    print("=" * 80 + "\n")

# ============================================================================
# TokenCounter 类
# ============================================================================

class TokenCounter:
    def __init__(self, model: str = "qwen-turbo"):
        self.model = model
        self.records = []
        self.current_start_time = None
        
        # 启动时检查价格新鲜度
        is_fresh, days_old = check_pricing_freshness()
        if not is_fresh:
            warnings.warn(
                f"⚠️  价格数据已 {days_old} 天未更新 (更新于: {PRICING_LAST_UPDATE})，建议核实最新价格！",
                UserWarning
            )
    
    def start_counting(self):
        """开始计时"""
        self.current_start_time = time.time()
    
    def record_usage(self, question: str, prompt_tokens: int, completion_tokens: int, model: Optional[str] = None) -> TokenUsage:
        """记录一次调用"""
        response_time = time.time() - self.current_start_time if self.current_start_time else 0
        model_name = model or self.model
        total = prompt_tokens + completion_tokens
        cost = calculate_cost(prompt_tokens, completion_tokens, model_name)
        
        record = TokenUsage(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            question=question[:50] + "..." if len(question) > 50 else question,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total,
            response_time=response_time,
            model=model_name,
            cost=cost
        )
        self.records.append(record)
        return record
    
    def print_current_usage(self, record: TokenUsage):
        """打印单次使用统计"""
        pricing_info = get_pricing_info(record.model)
        
        print("\n" + "=" * 80)
        print("📊 Token 使用统计")
        print("=" * 80)
        print(f"🕐 时间: {record.timestamp}")
        print(f"🤖 模型: {record.model} ({pricing_info['description']})")
        print(f"❓ 问题: {record.question}")
        print(f"⏱️  响应时间: {record.response_time:.2f} 秒")
        print(f"\n💬 Token 详情:")
        print(f"  - 输入:  {record.prompt_tokens:>6,} tokens × ¥{pricing_info['input']:.4f}/k = ¥{(record.prompt_tokens/1000)*pricing_info['input']:.4f}")
        print(f"  - 输出:  {record.completion_tokens:>6,} tokens × ¥{pricing_info['output']:.4f}/k = ¥{(record.completion_tokens/1000)*pricing_info['output']:.4f}")
        print(f"  - 总计:  {record.total_tokens:>6,} tokens")
        print(f"\n💰 本次成本: ¥{record.cost:.4f} 元")
        print("=" * 80 + "\n")
    
    def print_statistics(self):
        """打印累积统计"""
        if not self.records:
            print("⚠️  暂无统计数据")
            return
        
        total_tokens = sum(r.total_tokens for r in self.records)
        total_cost = sum(r.cost for r in self.records)
        total_time = sum(r.response_time for r in self.records)
        
        print("\n" + "=" * 80)
        print("📈 累积统计报告")
        print("=" * 80)
        print(f"📞 总调用次数: {len(self.records)}")
        print(f"⏱️  总响应时间: {total_time:.2f} 秒")
        print(f"⚡ 平均响应: {total_time/len(self.records):.2f} 秒/次")
        print(f"\n💬 Token 统计:")
        print(f"  - 累计 Token: {total_tokens:>10,}")
        print(f"  - 平均 Token: {total_tokens/len(self.records):>10,.0f}")
        print(f"\n💰 成本统计:")
        print(f"  - 累计成本: ¥{total_cost:.4f} 元")
        print(f"  - 平均成本: ¥{total_cost/len(self.records):.4f} 元/次")
        
        # 月度预估
        daily_100 = total_cost / len(self.records) * 100
        monthly = daily_100 * 30
        print(f"\n📊 用量预估 (按当前模式):")
        print(f"  - 100次/天: ¥{daily_100:.2f}/天 ≈ ¥{monthly:.2f}/月")
        print("=" * 80 + "\n")

def count_tokens_for_result(question: str, result: dict, counter: TokenCounter) -> TokenUsage:
    """从 agent 结果中计算 Token 消耗"""
    total_input = estimate_tokens(question)
    total_output = 0
    
    messages = result.get("messages", [])
    for msg in messages:
        content = getattr(msg, 'content', None) or (msg.get('content', '') if isinstance(msg, dict) else str(msg))
        if content:
            total_output += estimate_tokens(str(content))
    
    return counter.record_usage(question, total_input, total_output)

# ============================================================================
# 模块初始化
# ============================================================================

print("=" * 80)
print("✅ Token 计数器模块 v2.0 加载完成")
print("-" * 80)
print(f"📦 价格库版本: {PRICING_VERSION}")
print(f"📅 数据更新: {PRICING_LAST_UPDATE}")
print(f"📚 数据来源: {PRICING_SOURCE}")
print(f"🔧 支持模型: {len(MODEL_PRICING)} 个")

# 检查价格新鲜度
is_fresh, days_old = check_pricing_freshness()
if not is_fresh:
    print(f"⚠️  价格数据已 {days_old} 天未更新，建议核实最新价格！")
else:
    print(f"✅ 价格数据新鲜 (更新于 {days_old} 天前)")

print("=" * 80)
print("\n💡 新功能:")
print("  - list_available_models()      # 查看所有支持的模型")
print("  - compare_model_costs(...)     # 对比不同模型成本")
print("  - get_pricing_info(model)      # 获取模型价格详情")
print("\n")
