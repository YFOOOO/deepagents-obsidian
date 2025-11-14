"""
DeepAgents 结果展示工具函数

用于美化展示 Agent 的执行过程和提取最终答案
"""

def display_agent_execution(result):
    """
    展示 Agent 的完整执行流程
    
    参数:
        result: agent.invoke() 返回的结果字典
    """
    print("=" * 80)
    print("🤖 Agent 执行流程")
    print("=" * 80)
    
    if 'messages' not in result:
        print("⚠️ 结果中没有 messages 字段")
        return
    
    messages = result['messages']
    step_count = 0
    
    for msg in messages:
        msg_type = type(msg).__name__
        
        # 处理 HumanMessage（用户输入）
        if msg_type == 'HumanMessage' or (hasattr(msg, 'type') and msg.type == 'human'):
            print(f"\n👤 用户:")
            content = msg.content if hasattr(msg, 'content') else str(msg)
            print(f"   {content}")
            
        # 处理 AIMessage（Agent 响应）
        elif msg_type == 'AIMessage' or (hasattr(msg, 'type') and msg.type == 'ai'):
            step_count += 1
            print(f"\n🤖 Agent (步骤 {step_count}):")
            
            # 显示文本内容
            if hasattr(msg, 'content') and msg.content:
                print(f"   💬 回复: {msg.content}")
            
            # 显示工具调用
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"   🔧 调用工具:")
                for tool_call in msg.tool_calls:
                    tool_name = tool_call.get('name', '未知工具')
                    tool_args = tool_call.get('args', {})
                    print(f"      - {tool_name}")
                    if tool_args:
                        for key, value in tool_args.items():
                            # 截断过长的参数值
                            str_value = str(value)
                            if len(str_value) > 100:
                                str_value = str_value[:100] + "..."
                            print(f"        {key}: {str_value}")
        
        # 处理 ToolMessage（工具返回结果）
        elif msg_type == 'ToolMessage' or (hasattr(msg, 'type') and msg.type == 'tool'):
            tool_name = msg.name if hasattr(msg, 'name') else '未知工具'
            print(f"\n   📦 工具返回 ({tool_name}):")
            content = msg.content if hasattr(msg, 'content') else str(msg)
            # 截断过长的返回值
            if len(content) > 200:
                content = content[:200] + "..."
            print(f"      {content}")
    
    print("\n" + "=" * 80)
    print("✅ 执行完成")
    print("=" * 80)


def extract_final_answer(result):
    """
    提取 Agent 的最终答案
    
    参数:
        result: agent.invoke() 返回的结果字典
        
    返回:
        str: 最终答案文本
    """
    if 'messages' not in result:
        return "❌ 无法提取答案：结果中没有 messages 字段"
    
    messages = result['messages']
    
    # 从后往前查找最后一条 AIMessage
    for msg in reversed(messages):
        msg_type = type(msg).__name__
        if msg_type == 'AIMessage' or (hasattr(msg, 'type') and msg.type == 'ai'):
            if hasattr(msg, 'content') and msg.content:
                return msg.content
    
    return "❌ 未找到最终答案"


def count_tokens_for_result(question, result, token_counter):
    """
    统计单次查询的 Token 使用情况
    
    参数:
        question: 问题文本
        result: agent.invoke() 返回结果
        token_counter: TokenCounter 实例
        
    返回:
        dict: Token 使用记录
    """
    # 简化版本：估算 token 数量
    # 中文按字符数，英文按单词数的 1.3 倍估算
    
    def estimate_tokens(text):
        """估算文本的 token 数量"""
        if not text:
            return 0
        # 简单估算：中文 1 字符 ≈ 1.5 tokens，英文 1 单词 ≈ 1.3 tokens
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        other_chars = len(text) - chinese_chars
        return int(chinese_chars * 1.5 + other_chars * 0.3)
    
    prompt_tokens = estimate_tokens(question)
    completion_tokens = 0
    
    if 'messages' in result:
        for msg in result['messages']:
            if hasattr(msg, 'content') and msg.content:
                completion_tokens += estimate_tokens(msg.content)
    
    # 记录到 token_counter
    if hasattr(token_counter, 'record_usage'):
        return token_counter.record_usage(question, prompt_tokens, completion_tokens)
    
    # 返回简化的记录
    return {
        'question': question,
        'prompt_tokens': prompt_tokens,
        'completion_tokens': completion_tokens,
        'total_tokens': prompt_tokens + completion_tokens,
        'estimated': True
    }


if __name__ == '__main__':
    print("✅ DeepAgents 工具函数加载成功")
    print("可用函数:")
    print("  - display_agent_execution(result)")
    print("  - extract_final_answer(result)")
    print("  - count_tokens_for_result(question, result, token_counter)")
