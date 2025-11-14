#!/usr/bin/env python3
"""
API 端点测试脚本
运行此脚本前请确保 API 服务器已在另一个终端启动：
  cd /Users/yf/Documents/GitHub/deepagents/obsidian_assistant
  python run_test.py
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def check_server():
    """检查服务器是否运行"""
    print("🔍 检查服务器状态...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        print("✅ 服务器正在运行")
        return True
    except:
        print("❌ 服务器未运行")
        print("\n请在另一个终端运行:")
        print("  cd /Users/yf/Documents/GitHub/deepagents/obsidian_assistant")
        print("  python run_test.py")
        return False

def test_health():
    """测试 /health 端点"""
    print("\n" + "="*70)
    print("🧪 测试 1/3: /health 端点")
    print("="*70)
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"📊 状态码: {response.status_code}")
        data = response.json()
        print(f"📄 响应数据:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # 验证响应
        assert response.status_code == 200, "状态码不是 200"
        assert data.get("status") == "healthy", "状态不是 healthy"
        assert data.get("assistant_initialized") == True, "Assistant 未初始化"
        
        print("✅ 测试通过")
        return True
    except AssertionError as e:
        print(f"❌ 断言失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_models():
    """测试 /models 端点"""
    print("\n" + "="*70)
    print("🧪 测试 2/3: /models 端点")
    print("="*70)
    try:
        response = requests.get(f"{BASE_URL}/models", timeout=5)
        print(f"📊 状态码: {response.status_code}")
        data = response.json()
        
        print(f"📄 可用模型数量: {len(data.get('models', []))}")
        print(f"📄 主模型: {data.get('primary_model')}")
        print(f"📄 模型列表:")
        for model in data.get('models', [])[:5]:  # 只显示前5个
            print(f"   - {model}")
        if len(data.get('models', [])) > 5:
            print(f"   ... 还有 {len(data.get('models', [])) - 5} 个模型")
        
        # 验证响应
        assert response.status_code == 200, "状态码不是 200"
        assert len(data.get('models', [])) > 0, "没有可用模型"
        assert data.get('primary_model'), "没有主模型"
        
        print("✅ 测试通过")
        return True
    except AssertionError as e:
        print(f"❌ 断言失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_query():
    """测试 /query 端点"""
    print("\n" + "="*70)
    print("🧪 测试 3/3: /query 端点")
    print("="*70)
    try:
        payload = {
            "query": "什么是Obsidian？简短回答。",
            "include_sources": True
        }
        print(f"📤 发送查询: {payload['query']}")
        print("⏳ 等待响应（可能需要 5-15 秒）...")
        
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/query",
            json=payload,
            timeout=30
        )
        elapsed = time.time() - start_time
        
        print(f"📊 状态码: {response.status_code}")
        print(f"⏱️  响应时间: {elapsed:.2f}秒")
        
        data = response.json()
        
        print(f"\n📄 回答 ({len(data.get('answer', ''))} 字符):")
        answer = data.get('answer', '')
        if len(answer) > 200:
            print(answer[:200] + "...")
        else:
            print(answer)
        
        print(f"\n📚 来源数量: {len(data.get('sources', []))}")
        for i, source in enumerate(data.get('sources', [])[:3], 1):
            print(f"   {i}. {source.get('path', source.get('url', '未知'))}")
        
        if 'metadata' in data and 'token_stats' in data['metadata']:
            print(f"\n💰 Token 统计:")
            stats = data['metadata']['token_stats']
            print(f"   输入: {stats.get('prompt_tokens', 0)}")
            print(f"   输出: {stats.get('completion_tokens', 0)}")
            print(f"   总计: {stats.get('total_tokens', 0)}")
            if 'total_cost_yuan' in stats:
                print(f"   成本: ¥{stats['total_cost_yuan']:.6f}")
        
        # 验证响应
        assert response.status_code == 200, "状态码不是 200"
        assert len(data.get('answer', '')) > 0, "回答为空"
        
        print("\n✅ 测试通过")
        return True
    except AssertionError as e:
        print(f"❌ 断言失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def main():
    print("="*70)
    print("🧪 Obsidian AI Assistant - API 端点测试")
    print("="*70)
    
    # 检查服务器
    if not check_server():
        sys.exit(1)
    
    # 运行测试
    results = []
    results.append(("健康检查 (/health)", test_health()))
    results.append(("模型列表 (/models)", test_models()))
    results.append(("查询功能 (/query)", test_query()))
    
    # 总结
    print("\n" + "="*70)
    print("📊 测试总结")
    print("="*70)
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status}: {name}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    print("\n" + "="*70)
    if passed_count == total_count:
        print(f"🎉 所有测试通过! ({passed_count}/{total_count})")
        print("="*70)
        sys.exit(0)
    else:
        print(f"⚠️  部分测试失败 ({passed_count}/{total_count} 通过)")
        print("="*70)
        sys.exit(1)

if __name__ == "__main__":
    main()
