#!/bin/bash

# HackerNews AI Agent - POST Request Test Script

API_URL="http://localhost:8001/api/agent"
PUBLIC_URL="https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     HackerNews AI Agent - POST Request Tests              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Test 1: Topic Search
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 1: Topic Search"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X POST "$PUBLIC_URL" \
  -H "Content-Type: application/json" \
  -d '{"input": "find latest 3 news about AI"}' | jq -r '.response'
echo ""
echo ""

# Test 2: Summarization
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 2: Summarization"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X POST "$PUBLIC_URL" \
  -H "Content-Type: application/json" \
  -d '{"input": "summarize top 5 headlines"}' | jq -r '.response'
echo ""
echo ""

# Test 3: General Query
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 3: General Query"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X POST "$PUBLIC_URL" \
  -H "Content-Type: application/json" \
  -d '{"input": "what is trending on hacker news"}' | jq -r '.response'
echo ""
echo ""

# Test 4: Top Stories
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 4: Top Stories"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X POST "$PUBLIC_URL" \
  -H "Content-Type: application/json" \
  -d '{"input": "top 3 stories"}' | jq -r '.response'
echo ""
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    Tests Complete!                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Public API URL: $PUBLIC_URL"
echo ""
echo "Usage Examples:"
echo '  curl -X POST "$PUBLIC_URL" -H "Content-Type: application/json" -d '"'"'{"input": "find news about AI"}'"'"
echo '  curl -X POST "$PUBLIC_URL" -H "Content-Type: application/json" -d '"'"'{"input": "summarize top headlines"}'"'"
echo '  curl -X POST "$PUBLIC_URL" -H "Content-Type: application/json" -d '"'"'{"input": "what is trending"}'"'"
echo ""
