# HackerNews AI Agent

An intelligent AI agent that handles natural language queries about HackerNews stories and responds in natural language.

## ✨ Key Features

- **🗣️ Natural Language Input & Output**: Ask questions in plain English, get conversational responses
- **🔍 Topic Search**: Find stories about specific topics
- **📝 Smart Summarization**: Get AI-generated summaries of top headlines
- **📰 Latest News**: Get the most recent stories
- **🤖 Conversational AI**: Powered by GPT-4o-mini for intelligent responses

## 🚀 API Endpoints

### 🔥 Conversational Agent (Recommended)
```
GET /api/agent/chat?q=<your_question>
```
Returns natural language response - perfect for direct interaction!

### Structured Data (Optional)
```
GET /api/agent/query?q=<your_question>
```
Returns JSON data with structured story information.

## 📖 Examples

### 1. Topic Search (Conversational)
```bash
curl "http://localhost:8001/api/agent/chat?q=find%20latest%203%20news%20about%20AI"
```
**Response:** Natural language summary of AI-related stories with details.

### 2. Summarization
```bash
curl "http://localhost:8001/api/agent/chat?q=summarize%20top%205%20headlines%20today"
```
**Response:** Conversational overview of top headlines with key insights.

### 3. General Queries
```bash
curl "http://localhost:8001/api/agent/chat?q=what%27s%20trending%20on%20hacker%20news"
```
**Response:** Natural language description of trending stories.

## Setup

1. Install dependencies:
```bash
cd /app/backend
pip install -r requirements.txt --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

2. Run the server:
```bash
python server.py
```

## Technology Stack

- **FastAPI**: Web framework
- **HackerNews API**: Data source
- **EmergentIntegrations**: LLM integration
- **GPT-4o-mini**: Natural language processing and summarization

## How It Works

1. User sends a natural language query
2. Agent parses the query using LLM to extract intent and parameters
3. Fetches relevant stories from HackerNews API
4. Filters stories by topic if specified
5. Generates summaries or returns structured data
6. Returns formatted response

## Query Types

- **Search**: Find stories about specific topics
- **Summarize**: Get AI summaries of headlines
- **Latest**: Get most recent stories

## Response Format

The API returns JSON with:
- `query`: Original query
- `intent`: Detected intent (search/summarize/latest)
- `topic`: Extracted topic (if any)
- `stories_count`: Number of stories found
- `stories`: Array of story objects with title, url, score, comments, etc.
- `summary`: AI-generated summary (for summarize intent)
