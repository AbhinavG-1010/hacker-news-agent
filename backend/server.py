from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
import asyncio
from emergentintegrations.llm.chat import LlmChat, UserMessage
import json
import re
from datetime import datetime

load_dotenv()

app = FastAPI(title="HackerNews AI Agent")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HackerNews API base URL
HN_API_BASE = "https://hacker-news.firebaseio.com/v0"

# LLM configuration
EMERGENT_LLM_KEY = os.getenv("EMERGENT_LLM_KEY")


class HackerNewsService:
    """Service to interact with HackerNews API"""
    
    @staticmethod
    async def fetch_story(story_id: int) -> Optional[Dict]:
        """Fetch a single story by ID"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{HN_API_BASE}/item/{story_id}.json")
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f"Error fetching story {story_id}: {e}")
        return None
    
    @staticmethod
    async def fetch_top_stories(limit: int = 500) -> List[int]:
        """Fetch top story IDs"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{HN_API_BASE}/topstories.json")
                if response.status_code == 200:
                    return response.json()[:limit]
            except Exception as e:
                print(f"Error fetching top stories: {e}")
        return []
    
    @staticmethod
    async def fetch_new_stories(limit: int = 500) -> List[int]:
        """Fetch new story IDs"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{HN_API_BASE}/newstories.json")
                if response.status_code == 200:
                    return response.json()[:limit]
            except Exception as e:
                print(f"Error fetching new stories: {e}")
        return []
    
    @staticmethod
    async def fetch_best_stories(limit: int = 500) -> List[int]:
        """Fetch best story IDs"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{HN_API_BASE}/beststories.json")
                if response.status_code == 200:
                    return response.json()[:limit]
            except Exception as e:
                print(f"Error fetching best stories: {e}")
        return []
    
    @staticmethod
    async def fetch_stories_details(story_ids: List[int]) -> List[Dict]:
        """Fetch details for multiple stories concurrently"""
        tasks = [HackerNewsService.fetch_story(story_id) for story_id in story_ids]
        stories = await asyncio.gather(*tasks)
        # Filter out None values and stories without titles
        return [s for s in stories if s and s.get('title')]


class HackerNewsAgent:
    """AI Agent for processing HackerNews queries"""
    
    def __init__(self):
        self.llm_chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id="hn-agent",
            system_message="""You are a HackerNews AI assistant. Your job is to analyze user queries and extract:
1. Intent: 'search' (find specific topics), 'summarize' (summarize headlines), or 'latest' (get latest news)
2. Topic: The main topic/keyword to search for (if applicable)
3. Count: Number of stories requested (default 5 if not specified)
4. Story type: 'top', 'new', or 'best' (default 'top')

Respond ONLY with a JSON object in this exact format:
{"intent": "search|summarize|latest", "topic": "topic name or null", "count": number, "story_type": "top|new|best"}

Examples:
- "find latest 3 news about AI" -> {"intent": "search", "topic": "AI", "count": 3, "story_type": "new"}
- "summarize biggest headlines today" -> {"intent": "summarize", "topic": null, "count": 10, "story_type": "top"}
- "what's new about python" -> {"intent": "search", "topic": "python", "count": 5, "story_type": "new"}
- "top stories" -> {"intent": "latest", "topic": null, "count": 5, "story_type": "top"}"""
        ).with_model("openai", "gpt-4o-mini")
        
        self.conversational_agent = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id="hn-conversational",
            system_message="""You are a helpful HackerNews assistant that responds in natural, conversational language.
Your role is to help users discover and understand HackerNews stories.

When given stories, you should:
1. Provide a clear, conversational response
2. Highlight the most interesting or relevant stories
3. Include key details like scores, comments, and themes
4. Use a friendly, informative tone
5. Format responses clearly with proper structure

For search queries: Present the stories you found and briefly describe them.
For summarization: Provide an overview of key themes and highlights.
For general queries: Give a helpful, informative response about what you found.

Always be concise but informative. Use natural language, not JSON or technical jargon."""
        ).with_model("openai", "gpt-4o-mini")
    
    async def parse_query(self, query: str) -> Dict:
        """Parse user query to extract intent and parameters"""
        try:
            user_message = UserMessage(text=query)
            response = await self.llm_chat.send_message(user_message)
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback to default
                return {"intent": "latest", "topic": None, "count": 5, "story_type": "top"}
        except Exception as e:
            print(f"Error parsing query: {e}")
            return {"intent": "latest", "topic": None, "count": 5, "story_type": "top"}
    
    async def filter_stories_by_topic(self, stories: List[Dict], topic: str) -> List[Dict]:
        """Filter stories by topic using keyword matching"""
        if not topic:
            return stories
        
        topic_lower = topic.lower()
        filtered = []
        
        for story in stories:
            title = story.get('title', '').lower()
            text = story.get('text', '').lower() if story.get('text') else ''
            url = story.get('url', '').lower()
            
            # Check if topic appears in title, text, or url
            if topic_lower in title or topic_lower in text or topic_lower in url:
                filtered.append(story)
        
        return filtered
    
    async def generate_summary(self, stories: List[Dict], query: str) -> str:
        """Generate a summary of stories using LLM"""
        if not stories:
            return "No stories found matching your query."
        
        # Prepare stories text for summarization
        stories_text = "\n\n".join([
            f"Title: {story.get('title', 'N/A')}\n"
            f"Score: {story.get('score', 0)} points\n"
            f"Comments: {story.get('descendants', 0)}\n"
            f"URL: {story.get('url', 'N/A')}"
            for story in stories[:10]  # Limit to 10 for context
        ])
        
        prompt = f"""User query: {query}

Here are the HackerNews stories:

{stories_text}

Provide a concise summary addressing the user's query."""
        
        try:
            user_message = UserMessage(text=prompt)
            response = await self.conversational_agent.send_message(user_message)
            return response
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Error generating summary."
    
    async def generate_conversational_response(self, stories: List[Dict], query: str, intent: str, topic: Optional[str]) -> str:
        """Generate a natural language conversational response"""
        if not stories:
            if topic:
                return f"I couldn't find any HackerNews stories about '{topic}' at the moment. You might want to try a different search term or check back later."
            else:
                return "I couldn't find any stories matching your request. Please try a different query."
        
        # Prepare stories data for the LLM
        story_parts = []
        for i, story in enumerate(stories):
            story_url = story.get('url', f"https://news.ycombinator.com/item?id={story.get('id')}")
            story_time = datetime.fromtimestamp(story.get('time', 0)).strftime('%Y-%m-%d %H:%M')
            story_text = (
                f"Story {i+1}:\n"
                f"Title: {story.get('title', 'N/A')}\n"
                f"URL: {story_url}\n"
                f"Score: {story.get('score', 0)} points\n"
                f"Author: {story.get('by', 'unknown')}\n"
                f"Comments: {story.get('descendants', 0)}\n"
                f"Posted: {story_time}"
            )
            story_parts.append(story_text)
        stories_text = "\n\n".join(story_parts)
        
        # Create context-aware prompt
        context = f"User asked: '{query}'\n"
        if topic:
            context += f"They are looking for stories about: {topic}\n"
        context += f"Found {len(stories)} relevant stories.\n\n"
        
        prompt = f"""{context}Stories from HackerNews:

{stories_text}

Please provide a natural, conversational response to the user's query. 
- Be helpful and informative
- Highlight the most interesting stories
- Include relevant details (scores, comment counts)
- Keep it concise but engaging
- Use a friendly tone"""
        
        try:
            user_message = UserMessage(text=prompt)
            response = await self.conversational_agent.send_message(user_message)
            return response
        except Exception as e:
            print(f"Error generating conversational response: {e}")
            return "I found some stories but had trouble generating a response. Please try again."
    
    async def process_query(self, query: str) -> Dict:
        """Main method to process user queries - returns structured data"""
        # Parse the query
        parsed = await self.parse_query(query)
        intent = parsed.get('intent', 'latest')
        topic = parsed.get('topic')
        count = parsed.get('count', 5)
        story_type = parsed.get('story_type', 'top')
        
        # Fetch stories based on type
        if story_type == 'new':
            story_ids = await HackerNewsService.fetch_new_stories(limit=100)
        elif story_type == 'best':
            story_ids = await HackerNewsService.fetch_best_stories(limit=100)
        else:
            story_ids = await HackerNewsService.fetch_top_stories(limit=100)
        
        # Fetch story details
        stories = await HackerNewsService.fetch_stories_details(story_ids[:50])
        
        # Filter by topic if needed
        if topic:
            stories = await self.filter_stories_by_topic(stories, topic)
        
        # Limit to requested count
        stories = stories[:count]
        
        # Generate response based on intent
        if intent == 'summarize':
            summary = await self.generate_summary(stories, query)
            return {
                "query": query,
                "intent": intent,
                "summary": summary,
                "stories_count": len(stories),
                "stories": stories
            }
        else:
            # For search and latest, return structured data
            return {
                "query": query,
                "intent": intent,
                "topic": topic,
                "stories_count": len(stories),
                "stories": [
                    {
                        "id": story.get('id'),
                        "title": story.get('title'),
                        "url": story.get('url', f"https://news.ycombinator.com/item?id={story.get('id')}"),
                        "score": story.get('score', 0),
                        "by": story.get('by', 'unknown'),
                        "time": story.get('time'),
                        "comments": story.get('descendants', 0)
                    }
                    for story in stories
                ]
            }
    
    async def process_conversational_query(self, query: str) -> str:
        """Process query and return natural language response"""
        # Parse the query
        parsed = await self.parse_query(query)
        intent = parsed.get('intent', 'latest')
        topic = parsed.get('topic')
        count = parsed.get('count', 5)
        story_type = parsed.get('story_type', 'top')
        
        # Fetch stories based on type
        if story_type == 'new':
            story_ids = await HackerNewsService.fetch_new_stories(limit=100)
        elif story_type == 'best':
            story_ids = await HackerNewsService.fetch_best_stories(limit=100)
        else:
            story_ids = await HackerNewsService.fetch_top_stories(limit=100)
        
        # Fetch story details
        stories = await HackerNewsService.fetch_stories_details(story_ids[:50])
        
        # Filter by topic if needed
        if topic:
            stories = await self.filter_stories_by_topic(stories, topic)
        
        # Limit to requested count
        stories = stories[:count]
        
        # Generate conversational response
        response = await self.generate_conversational_response(stories, query, intent, topic)
        return response


# Initialize agent
agent = HackerNewsAgent()


@app.get("/")
async def root():
    return {
        "message": "HackerNews AI Agent API",
        "version": "2.0",
        "endpoints": {
            "/agent": "🔥 Main conversational agent - natural language input & output (use query parameter)",
            "/api/agent/chat": "Legacy conversational endpoint (use q parameter)",
            "/api/agent/query": "Structured agent endpoint - returns JSON data",
            "/api/health": "Health check endpoint"
        },
        "recommended": "/agent?query=<your_question>",
        "examples": [
            "/agent?query=find latest 3 news about AI",
            "/agent?query=summarize biggest headlines today",
            "/agent?query=what's new about python",
            "/agent?query=top 10 stories"
        ]
    }


@app.get("/api/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/api/agent")
async def conversational_agent(query: str = Query(..., description="Natural language query for HackerNews")):
    """
    🔥 Main conversational agent endpoint - accepts natural language and returns natural language.
    
    This is the primary endpoint for direct interaction with the agent.
    
    Examples:
    - /api/agent?query=find latest 3 news about AI
    - /api/agent?query=summarize biggest headlines today
    - /api/agent?query=what's new about python
    - /api/agent?query=tell me about top stories today
    """
    try:
        if not query or len(query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query parameter 'query' is required")
        
        response = await agent.process_conversational_query(query)
        return {"response": response, "query": query}
        
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/api/agent/chat")
async def chat_agent(q: str = Query(..., description="Natural language query for HackerNews")):
    """
    Legacy conversational agent endpoint (kept for backward compatibility).
    Use /agent?query=... instead.
    """
    try:
        if not q or len(q.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
        
        response = await agent.process_conversational_query(q)
        return {"response": response, "query": q}
        
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/api/agent/query")
async def query_agent(q: str = Query(..., description="Natural language query for HackerNews")):
    """
    Structured agent endpoint that accepts natural language queries and returns JSON data.
    
    Use /api/agent/chat for natural language responses instead.
    
    Examples:
    - /api/agent/query?q=find latest 3 news about AI
    - /api/agent/query?q=summarize biggest headlines today
    - /api/agent/query?q=what's new about python
    """
    try:
        if not q or len(q.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
        
        result = await agent.process_query(q)
        return result
        
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)