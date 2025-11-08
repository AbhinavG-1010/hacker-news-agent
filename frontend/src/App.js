import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const exampleQueries = [
    'find latest 5 news about AI',
    'summarize top 10 headlines today',
    'what\'s new about programming',
    'top 5 stories',
    'latest news about startups'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.get(`${BACKEND_URL}/api/agent/query`, {
        params: { q: query }
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch results. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (exampleQuery) => {
    setQuery(exampleQuery);
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1 data-testid="app-title">🤖 HackerNews AI Agent</h1>
          <p data-testid="app-subtitle">Ask me anything about HackerNews stories</p>
        </header>

        <div className="search-section">
          <form onSubmit={handleSubmit} data-testid="search-form">
            <div className="search-box">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask me anything... (e.g., 'find latest news about AI')"
                className="search-input"
                disabled={loading}
                data-testid="search-input"
              />
              <button 
                type="submit" 
                className="search-button" 
                disabled={loading || !query.trim()}
                data-testid="search-button"
              >
                {loading ? '🔄 Searching...' : '🔍 Search'}
              </button>
            </div>
          </form>

          <div className="examples">
            <p className="examples-label">Try these examples:</p>
            <div className="examples-grid">
              {exampleQueries.map((example, index) => (
                <button
                  key={index}
                  onClick={() => handleExampleClick(example)}
                  className="example-button"
                  disabled={loading}
                  data-testid={`example-button-${index}`}
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </div>

        {error && (
          <div className="error-box" data-testid="error-message">
            <span className="error-icon">⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {result && (
          <div className="results" data-testid="results-container">
            <div className="results-header">
              <h2>Results</h2>
              <span className="results-count" data-testid="results-count">
                {result.stories_count} {result.stories_count === 1 ? 'story' : 'stories'} found
              </span>
            </div>

            {result.summary && (
              <div className="summary-box" data-testid="summary-box">
                <h3>📝 Summary</h3>
                <p>{result.summary}</p>
              </div>
            )}

            {result.stories && result.stories.length > 0 && (
              <div className="stories-list">
                {result.stories.map((story, index) => (
                  <div key={story.id} className="story-card" data-testid={`story-card-${index}`}>
                    <div className="story-header">
                      <h3 className="story-title">
                        <a 
                          href={story.url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          data-testid={`story-link-${index}`}
                        >
                          {story.title}
                        </a>
                      </h3>
                    </div>
                    <div className="story-meta">
                      <span className="meta-item" data-testid={`story-score-${index}`}>⬆️ {story.score} points</span>
                      <span className="meta-item">👤 {story.by}</span>
                      <span className="meta-item" data-testid={`story-comments-${index}`}>💬 {story.comments} comments</span>
                      <span className="meta-item">🕒 {new Date(story.time * 1000).toLocaleDateString()}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {result.stories_count === 0 && (
              <div className="no-results" data-testid="no-results">
                <p>😔 No stories found matching your query. Try a different search!</p>
              </div>
            )}
          </div>
        )}

        <footer className="footer">
          <p>Powered by HackerNews API & AI 🚀</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
