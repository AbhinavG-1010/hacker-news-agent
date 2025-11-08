# HackerNews AI Agent - API Guide

## Overview

The HackerNews AI Agent provides a conversational interface to HackerNews stories using natural language processing.

**Version**: 2.0  
**Base URL**: `https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com`

---

## 🔥 Conversational Endpoint (Recommended)

### `/api/agent/chat`

**Purpose**: Natural language input → Natural language output

**Method**: `GET`

**Parameters**:
- `q` (required): Your natural language query

**Response Format**:
```json
{
  "response": "Natural language response from the agent...",
  "query": "your original query"
}
```

### Examples

#### Example 1: Topic Search
**Request**:
```bash
curl "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent/chat?q=find%20latest%203%20news%20about%20AI"
```

**Response**:
```json
{
  "response": "I've found some recent stories related to AI for you! Here are the latest highlights:\n\n1. **Story Title**\n   - Score: 150 points\n   - Comments: 45\n   - Posted: November 8, 2025\n   - Link: [URL]\n   - Brief description of the story...\n\n2. **Another Story**\n   ...",
  "query": "find latest 3 news about AI"
}
```

#### Example 2: Summarization
**Request**:
```bash
curl "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent/chat?q=summarize%20top%205%20headlines"
```

**Response**:
```json
{
  "response": "Here's a summary of the top five headlines today from HackerNews:\n\n1. **Marko – A declarative language** (149 points, 60 comments)\n   Marko is gaining attention as a new HTML-based language...\n\n2. **Study on AI evaluation** (265 points, 144 comments)\n   Research reveals critical issues in AI assessment metrics...\n\n...",
  "query": "summarize top 5 headlines"
}
```

#### Example 3: General Query
**Request**:
```bash
curl "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent/chat?q=what%27s%20trending"
```

**Response**:
```json
{
  "response": "Here's what's trending on Hacker News right now! Check out these stories:\n\n1. **Top Story Title** - 265 points with 144 comments\n   This story discusses...\n\n2. **Second Story** - 149 points with 60 comments\n   An interesting development in...\n\n...",
  "query": "what's trending"
}
```

---

## 📊 Structured Endpoint (Optional)

### `/api/agent/query`

**Purpose**: Natural language input → Structured JSON output

**Method**: `GET`

**Parameters**:
- `q` (required): Your natural language query

**Response Format**:
```json
{
  "query": "original query",
  "intent": "search|summarize|latest",
  "topic": "topic name or null",
  "stories_count": 5,
  "stories": [
    {
      "id": 12345,
      "title": "Story Title",
      "url": "https://example.com",
      "score": 150,
      "by": "username",
      "time": 1699459200,
      "comments": 45
    }
  ],
  "summary": "AI-generated summary (only for summarize intent)"
}
```

### Example

**Request**:
```bash
curl "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent/query?q=top%205%20stories"
```

**Response**:
```json
{
  "query": "top 5 stories",
  "intent": "latest",
  "topic": null,
  "stories_count": 5,
  "stories": [
    {
      "id": 45858905,
      "title": "Marko – A declarative, HTML‑based language",
      "url": "https://markojs.com/",
      "score": 149,
      "by": "ulrischa",
      "time": 1762627435,
      "comments": 60
    },
    ...
  ]
}
```

---

## 🎯 Query Patterns

The agent understands various natural language patterns:

### Search Queries
- "find latest 3 news about AI"
- "what's new about python"
- "search for stories about startups"
- "show me articles on machine learning"

### Summarization Queries
- "summarize top 10 headlines"
- "give me an overview of today's stories"
- "what are the biggest headlines"
- "summarize what's happening on HN"

### Latest/Trending Queries
- "top 5 stories"
- "what's trending"
- "latest news"
- "show me popular stories"

### Custom Queries
- "tell me about the most discussed topics"
- "what's everyone talking about"
- "interesting stories today"

---

## 🔍 Story Types

The agent automatically determines which story collection to use:

- **Top Stories**: Most upvoted stories (default)
- **New Stories**: Recently posted stories
- **Best Stories**: Best-rated stories over time

Queries with keywords like "latest", "new", "recent" will fetch from new stories.
General queries will fetch from top stories.

---

## 💡 Tips for Best Results

1. **Be Specific**: "find 3 news about AI" works better than just "AI"
2. **Use Natural Language**: The agent understands conversational queries
3. **Specify Count**: Include the number of stories you want (e.g., "top 5")
4. **Topic Keywords**: Use clear topic keywords for better filtering
5. **Ask for Summaries**: Use "summarize" for overview-style responses

---

## 🚨 Error Handling

### 400 Bad Request
```json
{
  "detail": "Query parameter 'q' is required"
}
```
**Solution**: Ensure the `q` parameter is included in your request.

### 500 Internal Server Error
```json
{
  "detail": "Error processing query: <error details>"
}
```
**Solution**: Check your query format or try again. The error message provides details.

---

## 📈 Rate Limits

Currently, there are no rate limits on the API. However, the HackerNews API itself has no official rate limits, but please use responsibly.

---

## 🔗 Integration Examples

### Python
```python
import requests

def ask_hn_agent(query):
    url = "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent/chat"
    response = requests.get(url, params={"q": query})
    return response.json()["response"]

# Usage
response = ask_hn_agent("find latest news about AI")
print(response)
```

### JavaScript
```javascript
async function askHNAgent(query) {
  const url = `https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent/chat?q=${encodeURIComponent(query)}`;
  const response = await fetch(url);
  const data = await response.json();
  return data.response;
}

// Usage
const response = await askHNAgent("summarize top headlines");
console.log(response);
```

### cURL
```bash
# Simple query
curl "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent/chat?q=top+stories"

# With jq for formatted output
curl -s "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent/chat?q=top+stories" | jq -r '.response'
```

---

## 📝 Additional Endpoints

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
  "version": "2.0",
  "endpoints": {
    "/api/agent/chat": "Conversational agent - natural language input & output",
    "/api/agent/query": "Structured agent endpoint - returns JSON data",
    "/api/health": "Health check endpoint"
  },
  "recommended": "/api/agent/chat"
}
```

---

## 🎓 Use Cases

1. **Telegram Bots**: Integrate with Telegram for conversational HN updates
2. **Slack Bots**: Create a Slack bot for team HN digests
3. **News Aggregators**: Build custom news feeds with AI summaries
4. **Research Tools**: Gather insights on specific tech topics
5. **Monitoring**: Track mentions of specific technologies or companies

---

## 📞 Support

For issues or questions about the API, please refer to the main documentation or contact support.

**Documentation**: `/app/README.md`  
**Deployment Guide**: `/app/DEPLOYMENT.md`
