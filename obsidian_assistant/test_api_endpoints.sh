#!/bin/bash
# API 端点测试脚本

echo "=================================="
echo "🧪 API 端点测试"
echo "=================================="
echo ""

API_URL="http://localhost:8000"

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试函数
test_endpoint() {
    local name=$1
    local endpoint=$2
    local method=${3:-GET}
    local data=$4
    
    echo -e "${YELLOW}测试: $name${NC}"
    echo "端点: $endpoint"
    
    if [ "$method" = "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data" 2>&1)
    else
        response=$(curl -s -w "\n%{http_code}" "$API_URL$endpoint" 2>&1)
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ 成功 (HTTP $http_code)${NC}"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    else
        echo -e "${RED}❌ 失败 (HTTP $http_code)${NC}"
        echo "$body"
    fi
    
    echo ""
    echo "----------------------------------"
    echo ""
}

# 等待服务器启动
echo "⏳ 等待服务器启动..."
sleep 2

# 测试 1: 健康检查
test_endpoint "健康检查" "/health" "GET"

# 测试 2: 模型列表
test_endpoint "获取模型列表" "/models" "GET"

# 测试 3: 简单查询
test_endpoint "简单查询测试" "/query" "POST" \
    '{"query":"什么是 Obsidian?","model":"qwen-turbo"}'

echo "=================================="
echo "✅ 测试完成"
echo "=================================="
