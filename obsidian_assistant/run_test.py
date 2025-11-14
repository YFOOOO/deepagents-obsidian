#!/usr/bin/env python
"""极简 API 服务器测试脚本 - 仅用于验证功能"""

import os
import sys
from pathlib import Path

# 设置路径
sys.path.insert(0, str(Path(__file__).parent))
os.chdir(Path(__file__).parent)

# 加载环境变量
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

print("=" * 80)
print("🧪 API 服务器测试模式")
print("=" * 80)
print(f"📁 工作目录: {os.getcwd()}")
print(f"📂 Obsidian: /Users/yf/Documents/obsidian agent")
print(f"🔑 DASHSCOPE_API_KEY: {'✅ 已设置' if os.getenv('DASHSCOPE_API_KEY') else '❌ 未设置'}")
print(f"🔑 TAVILY_API_KEY: {'✅ 已设置' if os.getenv('TAVILY_API_KEY') else '❌ 未设置'}")
print("=" * 80)
print()

if __name__ == "__main__":
    try:
        import uvicorn
        from api_server import app
        
        print("🚀 启动测试服务器 (按 Ctrl+C 停止)...")
        print("🌐 地址: http://localhost:8000")
        print("📖 API 文档: http://localhost:8000/docs")
        print()
        print("⏳ 初始化中...")
        print()
        
        # 直接运行在前台
        uvicorn.run(
            app,
            host="127.0.0.1",  # 只监听本地
            port=8000,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
