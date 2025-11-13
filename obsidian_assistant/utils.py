# DeepAgents 结果展示函数
import json
from typing import Dict, Any

def display_agent_execution(result: Dict[str, Any]) -> None:
    """
    展示 DeepAgents 执行的完整流程,包括:
    - 用户输入
    - Agent 思考过程
    - 工具调用(如果有)
    - 最终回复
    """
    messages = result.get("messages") if isinstance(result, dict) else getattr(result, "messages", None)
    
    if not messages:
        print("⚠️  未找到消息内容")
        return
    
    print("=" * 80)
    print("🤖 DeepAgents 执行流程")
    print("=" * 80)
    
    step_count = 0
    
    for idx, msg in enumerate(messages):
        # 获取消息类型和内容
        if isinstance(msg, dict):
            msg_type = msg.get("type", "unknown")
            content = msg.get("content", "")
            tool_calls = msg.get("tool_calls", [])
        else:
            msg_type = type(msg).__name__
            content = getattr(msg, "content", "")
            tool_calls = getattr(msg, "tool_calls", [])
        
        # 用户消息
        if "human" in msg_type.lower() or msg_type == "user":
            step_count += 1
            print(f"\n📝 步骤 {step_count}: 用户输入")
            print(f"{'─' * 80}")
            print(f"💬 {content}")
        
        # AI 响应
        elif "ai" in msg_type.lower() or msg_type == "assistant":
            step_count += 1
            print(f"\n🤔 步骤 {step_count}: Agent 响应")
            print(f"{'─' * 80}")
            
            if tool_calls:
                print("🛠️  Agent 决定调用工具:")
                for i, tool_call in enumerate(tool_calls, 1):
                    if isinstance(tool_call, dict):
                        tool_name = tool_call.get("name", "unknown")
                        tool_args = tool_call.get("args", {})
                    else:
                        tool_name = getattr(tool_call, "name", "unknown")
                        tool_args = getattr(tool_call, "args", {})
                    
                    print(f"  {i}. 工具名称: {tool_name}")
                    print(f"     参数: {json.dumps(tool_args, ensure_ascii=False, indent=6)}")
            
            if content and str(content).strip():
                print(f"💡 Agent 回复:")
                print(f"  {content}")
        
        # 工具执行结果
        elif "tool" in msg_type.lower():
            step_count += 1
            print(f"\n⚙️  步骤 {step_count}: 工具执行结果")
            print(f"{'─' * 80}")
            
            tool_name = None
            if isinstance(msg, dict):
                tool_name = msg.get("name") or msg.get("tool_name")
            else:
                tool_name = getattr(msg, "name", None) or getattr(msg, "tool_name", None)
            
            if tool_name:
                print(f"🔧 工具: {tool_name}")
            
            print(f"📊 返回结果:")
            if content:
                try:
                    parsed = json.loads(content) if isinstance(content, str) else content
                    print(json.dumps(parsed, ensure_ascii=False, indent=2))
                except:
                    print(f"  {content}")
    
    print(f"\n{'=' * 80}")
    print("✅ 执行完成")
    print(f"{'=' * 80}\n")


def extract_final_answer(result: Dict[str, Any]) -> str:
    """
    仅提取最终的 AI 回复内容
    """
    messages = result.get("messages") if isinstance(result, dict) else getattr(result, "messages", None)
    
    if not messages:
        return None
    
    # 从后往前找最后一个 AI 消息
    for msg in reversed(messages):
        if isinstance(msg, dict):
            msg_type = msg.get("type", "")
            content = msg.get("content", "")
        else:
            msg_type = type(msg).__name__
            content = getattr(msg, "content", "")
        
        if ("ai" in msg_type.lower() or msg_type == "assistant") and content:
            return content
    
    return None
