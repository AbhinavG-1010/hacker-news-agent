# HackerNews AI Agent

An intelligent AI agent that can handle natural language queries about HackerNews stories.

## Features

- **Natural Language Interface**: Ask questions in plain English
- **Topic Search**: Find stories about specific topics
- **Smart Summarization**: Get AI-generated summaries of top headlines
- **Latest News**: Get the most recent stories
- **Flexible Queries**: Supports various query formats

## API Endpoints

### Main Agent Endpoint
```
GET /api/agent/query?q=<your_question>
```

### Examples

1. Search for specific topics:
```bash
curl "http://localhost:8001/api/agent/query?q=find%20latest%203%20news%20about%20AI"
```

2. Summarize headlines:
```bash
curl "http://localhost:8001/api/agent/query?q=summarize%20biggest%20headlines%20today"
```

3. Get latest stories:
```bash
curl "http://localhost:8001/api/agent/query?q=top%2010%20stories"
```

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
