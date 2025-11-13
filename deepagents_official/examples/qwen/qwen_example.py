"""示例：如何使用 Qwen（Tongyi）模型接入 deepagents

说明：本示例使用 LangChain 社区包中对 Tongyi/Qwen 的封装 `ChatTongyi`。
在运行前，请确保已安装依赖：

    pip install dashscope langchain-community

并设置环境变量 `DASHSCOPE_API_KEY`（或在构造时传入 `api_key=`）。

示例会构造一个 `ChatTongyi` 实例并将其传入 `create_deep_agent(model=...)`。
然后演示如何调用 agent（同步示例）。
"""

import os
from pprint import pprint

from deepagents import create_deep_agent

# 自动加载本地 .env（如果存在），方便在开发环境中把 API key 放在 .env 文件里
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # python-dotenv 非必需，但有时对本地开发很方便
    pass

try:
    # LangChain 社区封装中的 ChatTongyi
    from langchain_community.chat_models import ChatTongyi
    from langchain_core.messages import HumanMessage
except Exception as e:  # pragma: no cover - user environment may be missing packages
    raise ImportError(
        "需要安装 dashscope 与 langchain-community。运行: pip install dashscope langchain-community"
    ) from e


def main():
    # 优先从环境变量读取 API key
    api_key = os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("QWEN_API_KEY")
    # 诊断信息：告诉用户 env 中是否存在 key
    if api_key:
        print("已从环境读取到 Qwen API Key（将用于 ChatTongyi 构造）")
    else:
        print("未在环境中找到 DASHSCOPE_API_KEY 或 QWEN_API_KEY（将无法调用真实 API）")
    if not api_key:
        print("请先设置 DASHSCOPE_API_KEY（或 QWEN_API_KEY）环境变量以运行本示例。")
        return

    # 创建 Qwen/Tongyi 模型实例（根据需要调整 model 名称，例如 'qwen-turbo' / 'qwen-max'）
    # 构造 ChatTongyi 实例（如未提供 api_key，ChatTongyi 会尝试从环境变量中读取）
    qwen = ChatTongyi(model="qwen-turbo", api_key=api_key)

    # 创建 deep agent，并传入 qwen 模型实例
    agent = create_deep_agent(model=qwen, tools=[], system_prompt="You are an assistant powered by Qwen/Tongyi.")

    # 构造最小 state 并调用 agent（deepagents 使用 state dict，包含 messages）
    state = {"messages": [HumanMessage(content="请用中文简短介绍Qwen模型的用途。")]}  # 中文示例

    # agent.invoke 返回一个包含 messages 的结果（取决于模型封装）
    result = agent.invoke(state)

    pprint(result)


if __name__ == "__main__":
    main()
