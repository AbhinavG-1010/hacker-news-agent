# HackerNews AI Agent - Deployment Guide

## Overview
Complete full-stack application with AI-powered HackerNews agent.

## Architecture

### Backend (FastAPI)
- **Port**: 8001
- **Location**: `/app/backend/`
- **Main File**: `server.py`
- **Features**:
  - Natural language query processing
  - HackerNews API integration
  - AI-powered summarization (GPT-4o-mini)
  - RESTful API endpoints

### Frontend (React)
- **Port**: 3000
- **Location**: `/app/frontend/`
- **Features**:
  - Clean, modern UI
  - Real-time search
  - Example queries
  - Story cards with metadata
  - Responsive design

## API Endpoints

### Backend
- `GET /` - API information and examples
- `GET /api/health` - Health check
- `GET /api/agent/query?q=<query>` - Main agent endpoint

### Public URLs
- **Backend**: `https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com`
- **Frontend**: `https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com` (via nginx proxy)

## Environment Variables

### Backend (.env)
```
EMERGENT_LLM_KEY=sk-emergent-4E055C9DeB9DeE8B9E
```

### Frontend (.env)
```
REACT_APP_BACKEND_URL=https://9269b179-d7ec-4d7a-95e6-41cf0b7d4517.preview.emergentagent.com
```

## Dependencies

### Backend (Python)
- fastapi==0.115.5
- uvicorn==0.32.1
- httpx==0.27.2
- python-dotenv==1.0.1
- emergentintegrations (with special index)

### Frontend (Node.js)
- react@^18.2.0
- react-dom@^18.2.0
- react-scripts@5.0.1
- axios@^1.6.0

## Deployment Status
✅ **READY FOR DEPLOYMENT**

### Pre-Deployment Checks
- ✅ Backend running (port 8001)
- ✅ Frontend running (port 3000)
- ✅ Environment variables configured
- ✅ CORS properly configured
- ✅ Health endpoints responding
- ✅ Public URLs accessible
- ✅ All dependencies installed
- ✅ No hardcoded values
- ✅ Supervisor configured

### Service Management
```bash
# Restart all services
sudo supervisorctl restart all

# Restart backend only
sudo supervisorctl restart backend

# Restart frontend only
sudo supervisorctl restart frontend

# Check status
sudo supervisorctl status
```

## Testing

### Backend Tests
```bash
# Health check
curl http://localhost:8001/api/health

# Test query
curl "http://localhost:8001/api/agent/query?q=top%205%20stories"

# Test topic search
curl "http://localhost:8001/api/agent/query?q=find%20latest%203%20news%20about%20AI"

# Test summarization
curl "http://localhost:8001/api/agent/query?q=summarize%20top%205%20headlines"
```

### Frontend Tests
- Open `http://localhost:3000` in browser
- Try example queries
- Verify results display correctly

## Example Queries

1. **Topic Search**: "find latest 5 news about AI"
2. **Summarization**: "summarize top 10 headlines today"
3. **General**: "what's new about programming"
4. **Latest**: "top 5 stories"
5. **Specific**: "latest news about startups"

## Features

### Agent Capabilities
- ✅ Natural language understanding
- ✅ Intent detection (search, summarize, latest)
- ✅ Topic extraction and filtering
- ✅ AI-powered summarization
- ✅ Concurrent story fetching
- ✅ Story type selection (top, new, best)

### UI Features
- ✅ Modern gradient design
- ✅ Real-time search
- ✅ Loading states
- ✅ Error handling
- ✅ Example queries
- ✅ Story cards with metadata
- ✅ External link opening
- ✅ Responsive layout
- ✅ Data test IDs for testing

## Production Considerations
- Stateless design (Kubernetes-ready)
- No database required (external APIs only)
- Auto-scaling compatible
- Health checks enabled
- CORS configured for production
- Environment-based configuration

## Logs
```bash
# Backend logs
tail -f /var/log/supervisor/backend.err.log
tail -f /var/log/supervisor/backend.out.log

# Frontend logs
tail -f /var/log/supervisor/frontend.err.log
tail -f /var/log/supervisor/frontend.out.log
```

## Notes
- Backend uses Emergent Universal LLM key (no personal API key needed)
- HackerNews API has no rate limits
- Frontend communicates with backend via environment variable
- Both services managed by supervisor for automatic restarts
