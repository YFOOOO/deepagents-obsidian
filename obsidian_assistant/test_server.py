#!/usr/bin/env python
"""简化版 API 服务器测试脚本"""

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))

# 加载环境变量
from dotenv import load_dotenv
load_dotenv(project_root / ".env")

print("✅ 环境变量已加载")
print(f"📁 Obsidian路径: /Users/yf/Documents/obsidian agent")
print(f"🔑 DASHSCOPE_API_KEY: {'已设置' if os.getenv('DASHSCOPE_API_KEY') else '未设置'}")
print(f"🔑 TAVILY_API_KEY: {'已设置' if os.getenv('TAVILY_API_KEY') else '未设置'}")

# 启动服务器
if __name__ == "__main__":
    import uvicorn
    from api_server import app
    
    print("\n🚀 启动 API 服务器...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
