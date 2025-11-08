#!/bin/bash

# HackerNews AI Agent - Conversational API Test Script

API_URL="http://localhost:8001/api/agent/chat"
PUBLIC_URL="https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent/chat"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     HackerNews AI Agent - Conversational API Tests        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Test 1: Topic Search
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 1: Topic Search - 'find latest 3 news about AI'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s "$API_URL?q=find%20latest%203%20news%20about%20AI" | jq -r '.response'
echo ""
echo ""

# Test 2: Summarization
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 2: Summarization - 'summarize top 5 headlines'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s "$API_URL?q=summarize%20top%205%20headlines" | jq -r '.response'
echo ""
echo ""

# Test 3: General Query
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 3: General Query - 'what's trending on hacker news'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s "$API_URL?q=what%27s%20trending%20on%20hacker%20news" | jq -r '.response'
echo ""
echo ""

# Test 4: Simple Query
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 4: Simple Query - 'top stories'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s "$API_URL?q=top%20stories" | jq -r '.response'
echo ""
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    Tests Complete!                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Public API URL: $PUBLIC_URL"
echo ""
echo "Usage Examples:"
echo "  curl '$PUBLIC_URL?q=find+news+about+AI'"
echo "  curl '$PUBLIC_URL?q=summarize+top+headlines'"
echo "  curl '$PUBLIC_URL?q=what+is+trending'"
echo ""
