#!/usr/bin/env python3
"""Simple API test script"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_models():
    """Test models endpoint"""
    print("\n🔍 Testing /models endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/models", timeout=5)
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Available models: {len(data.get('models', []))}")
        print(f"   Primary model: {data.get('primary_model')}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_query():
    """Test query endpoint"""
    print("\n🔍 Testing /query endpoint...")
    try:
        payload = {
            "query": "什么是Obsidian？",
            "include_sources": True
        }
        response = requests.post(
            f"{BASE_URL}/query",
            json=payload,
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Answer length: {len(data.get('answer', ''))}")
        print(f"   Sources count: {len(data.get('sources', []))}")
        print(f"   Token usage: {data.get('metadata', {}).get('token_stats')}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🧪 Obsidian AI Assistant API Tests")
    print("="*60)
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Models List", test_models()))
    results.append(("Query", test_query()))
    
    print("\n" + "="*60)
    print("📊 Test Results:")
    print("="*60)
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status}: {name}")
    
    all_passed = all(r[1] for r in results)
    print("\n" + "="*60)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed")
    print("="*60)
