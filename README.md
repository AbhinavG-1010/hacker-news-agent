# HackerNews AI Agent

An intelligent AI agent that handles natural language queries about HackerNews stories and responds in natural language.

## ✨ Key Features

- **🗣️ Natural Language Input & Output**: Ask questions in plain English, get conversational responses
- **🔍 Topic Search**: Find stories about specific topics
- **📝 Smart Summarization**: Get AI-generated summaries of top headlines
- **📰 Latest News**: Get the most recent stories
- **🤖 Conversational AI**: Powered by GPT-4o-mini for intelligent responses
- **🔌 REST API**: Simple POST endpoint with JSON input/output

## 🚀 API Endpoint

### 🔥 Main Agent Endpoint
```
POST /api/agent
Content-Type: application/json
```

**Request Body:**
```json
{
  "input": "your natural language query"
}
```

**Response Body:**
```json
{
  "output": "natural language response from agent"
}
```

## 📖 Examples

### 1. Topic Search
```bash
curl -X POST "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent" \
  -H "Content-Type: application/json" \
  -d '{"input": "find latest 3 news about AI"}'
```

**Response:**
```json
{
  "output": "Here are the latest AI stories...\n\n1. **Story Title** (150 points, 45 comments)\n   Description..."
}
```

### 2. Summarization
```bash
curl -X POST "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent" \
  -H "Content-Type: application/json" \
  -d '{"input": "summarize top 5 headlines"}'
```

### 3. What's Trending
```bash
curl -X POST "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent" \
  -H "Content-Type: application/json" \
  -d '{"input": "what is trending on hacker news"}'
```

### 4. Top Stories
```bash
curl -X POST "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent" \
  -H "Content-Type: application/json" \
  -d '{"input": "top 3 stories"}'
```

## 🛠️ Setup

1. Install dependencies:
```bash
cd /app/backend
pip install -r requirements.txt --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

2. Run the server:
```bash
python server.py
```

## 🎯 Technology Stack

- **FastAPI**: Web framework
- **HackerNews API**: Data source
- **EmergentIntegrations**: LLM integration library
- **GPT-4o-mini**: Natural language processing and generation

## 🔄 How It Works

1. **Input**: User sends natural language query
2. **Parse**: Agent analyzes query to understand intent (search/summarize/latest)
3. **Fetch**: Retrieves relevant stories from HackerNews API
4. **Filter**: Applies topic filtering if specified
5. **Generate**: Creates natural language response using GPT-4o-mini
6. **Output**: Returns conversational response

## 💬 Query Types

The agent understands various query formats:

- **Search**: "find latest 3 news about AI", "what's new about python"
- **Summarize**: "summarize top 5 headlines", "give me an overview of today's stories"
- **Latest**: "top stories", "what's trending on hacker news"
- **Custom**: "tell me about the most discussed topics today"

## 📤 Response Format

### Conversational Endpoint (`/api/agent/chat`)
```json
{
  "response": "Natural language response with story details...",
  "query": "original query"
}
```

### Structured Endpoint (`/api/agent/query`)
```json
{
  "query": "original query",
  "intent": "search|summarize|latest",
  "topic": "topic name or null",
  "stories_count": 5,
  "stories": [...],
  "summary": "AI summary (if applicable)"
}
```

## 🧪 Testing

Run the test script:
```bash
./test_agent.sh
```

## 🌐 Public Access

**API URL**: `https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent/chat`

**Quick Test**:
```bash
curl "https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com/api/agent/chat?q=top+stories"
```
