# HackerNews AI Agent - POST API Guide

## Overview

The HackerNews AI Agent now uses POST requests for conversational interaction with natural language input and output.

**Version**: 2.1  
**Base URL**: `https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com`

---

## 🔥 Main Endpoint

### `POST /api/agent`

**Purpose**: Natural language input → Natural language output

**Method**: `POST`

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "input": "your natural language query"
}
```

**Response Body**:
```json
{
  "response": "natural language response from the agent"
}
```

---

## 📖 Examples

### Example 1: Find AI Stories

**Request**:
```bash
curl -X POST "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent" \
  -H "Content-Type: application/json" \
  -d '{"input": "find latest 3 news about AI"}'
```

**Response**:
```json
{
  "response": "Here are the top 3 AI-related stories...\n\n1. **Story Title** (Score: 150 points, 45 comments)\n   Description...\n\n2. **Another Story** (Score: 120 points, 30 comments)\n   More details..."
}
```

### Example 2: Summarize Headlines

**Request**:
```bash
curl -X POST "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent" \
  -H "Content-Type: application/json" \
  -d '{"input": "summarize top 5 headlines"}'
```

**Response**:
```json
{
  "response": "Here's a summary of the top five headlines today from HackerNews:\n\n1. **Marko** (149 points, 60 comments)\n   Marko is gaining attention...\n\n2. **AI Evaluation Study** (265 points, 144 comments)\n   Research reveals..."
}
```

### Example 3: What's Trending

**Request**:
```bash
curl -X POST "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent" \
  -H "Content-Type: application/json" \
  -d '{"input": "what is trending on hacker news"}'
```

**Response**:
```json
{
  "response": "Here's what's trending on Hacker News right now! Check out these stories:\n\n1. **Top Story Title** - 265 points with 144 comments\n   This story discusses..."
}
```

### Example 4: Top Stories

**Request**:
```bash
curl -X POST "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent" \
  -H "Content-Type: application/json" \
  -d '{"input": "top 3 stories"}'
```

**Response**:
```json
{
  "response": "Here are the top 3 stories currently trending on HackerNews:\n\n1. **Ironclad OS** (38 points, 5 comments)\n   Ironclad discusses..."
}
```

---

## 🎯 Query Patterns

The agent understands various natural language patterns:

### Search Queries
```json
{"input": "find latest 3 news about AI"}
{"input": "what's new about python"}
{"input": "search for stories about startups"}
{"input": "show me articles on machine learning"}
```

### Summarization Queries
```json
{"input": "summarize top 10 headlines"}
{"input": "give me an overview of today's stories"}
{"input": "what are the biggest headlines"}
{"input": "summarize what's happening on HN"}
```

### Latest/Trending Queries
```json
{"input": "top 5 stories"}
{"input": "what's trending"}
{"input": "latest news"}
{"input": "show me popular stories"}
```

### Custom Queries
```json
{"input": "tell me about the most discussed topics"}
{"input": "what's everyone talking about"}
{"input": "interesting stories today"}
```

---

## 💻 Code Examples

### Python
```python
import requests

def ask_hn_agent(query):
    url = "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent"
    headers = {"Content-Type": "application/json"}
    data = {"input": query}
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()["response"]

# Usage
response = ask_hn_agent("find latest news about AI")
print(response)
```

### JavaScript (Node.js)
```javascript
async function askHNAgent(query) {
  const url = "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent";
  
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ input: query })
  });
  
  const data = await response.json();
  return data.response;
}

// Usage
const response = await askHNAgent("summarize top headlines");
console.log(response);
```

### JavaScript (Browser)
```javascript
async function askHNAgent(query) {
  const response = await fetch(
    "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input: query })
    }
  );
  
  const data = await response.json();
  return data.response;
}

// Usage
askHNAgent("top stories").then(response => {
  console.log(response);
});
```

### cURL
```bash
# Basic query
curl -X POST "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent" \
  -H "Content-Type: application/json" \
  -d '{"input": "top stories"}'

# Get just the response text
curl -s -X POST "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent" \
  -H "Content-Type: application/json" \
  -d '{"input": "find news about AI"}' | jq -r '.response'

# Pretty print
curl -s -X POST "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent" \
  -H "Content-Type: application/json" \
  -d '{"input": "summarize top headlines"}' | jq '.'
```

---

## 🚨 Error Handling

### 400 Bad Request - Empty Input
```json
{
  "detail": "Input field is required and cannot be empty"
}
```

**Cause**: The `input` field is missing, empty, or contains only whitespace.

**Solution**: Ensure the request body includes a valid `input` field:
```json
{"input": "your query here"}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "input"],
      "msg": "Field required"
    }
  ]
}
```

**Cause**: Request body is malformed or missing the `input` field.

**Solution**: Send a valid JSON body with the `input` field.

### 500 Internal Server Error
```json
{
  "detail": "Error processing query: <error details>"
}
```

**Cause**: Server-side error during query processing.

**Solution**: Check your query format and try again. If the problem persists, contact support.

---

## 🔍 Response Format

All successful responses follow this format:

```json
{
  "response": "Natural language response with story details, including:\n- Story titles\n- Scores (upvotes)\n- Comment counts\n- Authors\n- Links\n- Descriptions and context"
}
```

The `response` field contains:
- Natural language text
- Formatted with markdown-style headers
- Links to stories
- Story metadata (score, comments, author)
- Contextual descriptions and insights

---

## 📊 Additional Endpoints

### Health Check
```bash
GET /api/health
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-08T22:45:44.432627"
}
```

### API Info
```bash
GET /
```

**Response**:
```json
{
  "message": "HackerNews AI Agent API",
  "version": "2.1",
  "endpoints": {
    "POST /api/agent": "Main conversational agent",
    "GET /api/health": "Health check"
  },
  "request_format": {
    "method": "POST",
    "url": "/api/agent",
    "body": {
      "input": "your natural language query"
    }
  },
  "response_format": {
    "response": "natural language response"
  }
}
```

---

## 🎓 Use Cases

1. **Telegram Bots**: Integrate with Telegram for conversational HN updates
2. **Slack Bots**: Create a Slack bot for team HN digests
3. **News Aggregators**: Build custom news feeds with AI summaries
4. **Research Tools**: Gather insights on specific tech topics
5. **Monitoring**: Track mentions of specific technologies or companies
6. **CLI Tools**: Create command-line interfaces for HN queries
7. **Mobile Apps**: Power mobile app backends with natural language
8. **Voice Assistants**: Enable voice-based HN queries

---

## 🔐 CORS

CORS is enabled for all origins, allowing requests from any domain.

---

## ⚡ Rate Limits

Currently, there are no rate limits on the API. However:
- The HackerNews API has no official rate limits
- Use responsibly to avoid overloading services
- Consider implementing client-side caching for repeated queries

---

## 📝 Best Practices

1. **Be Specific**: Include numbers ("3 stories") for better results
2. **Use Natural Language**: The agent understands conversational queries
3. **Handle Responses**: Parse the natural language response as needed
4. **Error Handling**: Always check for error responses
5. **Timeouts**: Set appropriate timeout values (recommended: 30s)
6. **Retries**: Implement retry logic for failed requests

---

## 🐛 Troubleshooting

### Issue: Connection Timeout
**Solution**: Increase timeout value to 30-60 seconds

### Issue: Empty Response
**Solution**: Verify the request body is properly formatted JSON

### Issue: CORS Error (Browser)
**Solution**: This shouldn't happen as CORS is enabled. Check browser console for details.

### Issue: 422 Error
**Solution**: Ensure Content-Type header is set to "application/json"

---

## 📞 Support

For issues or questions:
- Check `/app/README.md` for general documentation
- Check `/app/DEPLOYMENT.md` for deployment information
- Run test script: `./test_post_agent.sh`

**API Endpoint**: `POST /api/agent`  
**Status Endpoint**: `GET /api/health`
