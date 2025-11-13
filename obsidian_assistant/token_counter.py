"""
Token 计数器工具 v1.0 - 实时监控 LLM Token 消耗
"""
import time
from typing import Dict, Optional
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

MODEL_PRICING = {
    "qwen-turbo": {"input": 0.002, "output": 0.006},
    "qwen-plus": {"input": 0.004, "output": 0.012},
}

def calculate_cost(prompt_tokens: int, completion_tokens: int, model: str = "qwen-turbo") -> float:
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["qwen-turbo"])
    return (prompt_tokens / 1000) * pricing["input"] + (completion_tokens / 1000) * pricing["output"]

def estimate_tokens(text: str) -> int:
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    english_words = len([w for w in text.split() if any(c.isalpha() for c in w)])
    return int(chinese_chars * 1.8 + english_words * 1.3) or len(text) // 4

class TokenCounter:
    def __init__(self, model: str = "qwen-turbo"):
        self.model = model
        self.records = []
        self.current_start_time = None
    
    def start_counting(self):
        self.current_start_time = time.time()
    
    def record_usage(self, question: str, prompt_tokens: int, completion_tokens: int, model: Optional[str] = None) -> TokenUsage:
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
        print("\n" + "=" * 80)
        print("📊 Token 使用统计")
        print("=" * 80)
        print(f"🕐 时间: {record.timestamp}")
        print(f"❓ 问题: {record.question}")
        print(f"⏱️  响应时间: {record.response_time:.2f} 秒")
        print(f"\n💬 Token 详情:")
        print(f"  - 输入:  {record.prompt_tokens:>6,}")
        print(f"  - 输出:  {record.completion_tokens:>6,}")
        print(f"  - 总计:  {record.total_tokens:>6,}")
        print(f"\n💰 预估成本: ¥{record.cost:.4f} 元")
        print("=" * 80 + "\n")
    
    def print_statistics(self):
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
        print("=" * 80 + "\n")

def count_tokens_for_result(question: str, result: dict, counter: TokenCounter) -> TokenUsage:
    total_input = estimate_tokens(question)
    total_output = 0
    
    messages = result.get("messages", [])
    for msg in messages:
        content = getattr(msg, 'content', None) or (msg.get('content', '') if isinstance(msg, dict) else str(msg))
        if content:
            total_output += estimate_tokens(str(content))
    
    return counter.record_usage(question, total_input, total_output)

print("✅ Token 计数器模块加载完成")
