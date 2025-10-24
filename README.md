# TaskWeave MVP

**A weekend-shippable multi-agent productivity assistant**

TaskWeave lets users type natural language requests like *"Plan my Stanford CS midterms week"* and coordinates multiple AI agents to:
- Parse intent with Claude (Anthropic)
- Spawn and coordinate sub-agents via Fetch AI Agentverse / ASI:One
- Remember preferences and context using Letta Cloud
- Execute real actions through Composio Toolrouter (Google Calendar, Notion)
- Display everything in a beautiful Warp-style React terminal + dashboard

## 🚀 Quick Start

### Prerequisites
- Docker & docker-compose
- Node.js 18+ (for local frontend dev)
- Python 3.11+ (for local backend dev)

### Run with Docker (Recommended)
```bash
# 1. Clone and enter the repo
cd TaskWeave

# 2. Copy environment template
cp .env.example .env

# 3. Launch everything
docker-compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Health: http://localhost:8000/health

### Run Locally (Development)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Run Tests

**Backend:**
```bash
cd backend
pytest -q
```

**Frontend:**
```bash
cd frontend
npm run test
```

## 🎯 Demo Script

1. Open http://localhost:5173
2. Type in the terminal: `Plan my Stanford CS midterms week`
3. Watch Claude break down the request into 3 subtasks
4. See agents propose study blocks, meals, and calendar events
5. Review the merged timeline respecting your sleep schedule
6. Click **Apply to Calendar** (dry-run mode is ON by default)
7. Open the **Memory** tab to edit preferences (sleep hours, study block length, breaks)
8. Re-run the command and see the timeline adjust automatically

## 🏗️ Architecture

```
User Input → Claude (parse intent) → Fetch AI Agents (study, meal, calendar)
                                    ↓
                           Letta (memory & prefs)
                                    ↓
                    Composio (execute on Google Calendar)
                                    ↓
                      WebSocket → React UI (live updates)
```

## 📋 Environment Variables

Copy `.env.example` to `.env` and configure:

### Required for Full Functionality
- `ANTHROPIC_API_KEY` - Claude API key (falls back to mock)
- `FETCH_API_KEY` - Fetch AI key (falls back to mock)
- `LETTA_API_KEY` - Letta Cloud key (falls back to in-memory)
- `COMPOSIO_API_KEY` - Composio key (falls back to dry-run)

### Optional
- `ELASTIC_URL` - Elasticsearch for centralized logging
- `PORT` - Backend port (default: 8000)
- `ALLOWED_ORIGINS` - CORS origins (default: http://localhost:5173)

**Note:** The system works fully in mock mode without any API keys for demo purposes.

## 🧪 Features

- ✅ Natural language task planning with Claude
- ✅ Multi-agent orchestration (study, meal, calendar agents)
- ✅ Stateful memory with user preferences
- ✅ Conflict-free timeline merging (respects sleep, breaks, overlaps)
- ✅ Real-time WebSocket event streaming
- ✅ Dry-run mode for safe calendar operations
- ✅ Beautiful terminal UI with live logs
- ✅ Memory panel for editing preferences
- ✅ Full mock mode (no API keys required)
- ✅ Docker deployment
- ✅ Comprehensive tests

## 🎨 Tech Stack

**Frontend:**
- React + TypeScript + Vite
- TailwindCSS for styling
- WebSocket for real-time updates
- Vitest + React Testing Library

**Backend:**
- Python FastAPI (async)
- Pydantic for validation
- WebSocket support
- Pytest for testing

**AI & Tools:**
- Anthropic Claude (intent parsing)
- Fetch AI Agentverse / ASI:One (agent orchestration)
- Letta Cloud (stateful memory)
- Composio Toolrouter (calendar integration)

## 📁 Project Structure

```
taskweave/
├── README.md
├── .env.example
├── docker-compose.yml
├── backend/               # Python FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── router/       # API endpoints
│   │   ├── services/     # Business logic
│   │   ├── adapters/     # External API clients
│   │   ├── models/       # DTOs, domain models
│   │   ├── util/         # Logging, errors, IDs
│   │   └── tests/
│   ├── requirements.txt
│   └── pyproject.toml
└── frontend/             # React + TypeScript
    ├── src/
    │   ├── main.tsx
    │   ├── App.tsx
    │   ├── components/   # Terminal, Timeline, etc.
    │   ├── hooks/        # WebSocket hook
    │   ├── lib/          # API client, types
    │   └── styles/
    ├── package.json
    ├── vite.config.ts
    └── tailwind.config.js
```

## 🔐 Security & Privacy

- ✅ Secrets never logged
- ✅ Input validation on all endpoints
- ✅ CORS restricted to localhost:5173
- ✅ Request tracing with trace_id
- ✅ Error boundaries in React

## 🚧 Future Enhancements

- [ ] Notion export
- [ ] Real Google Calendar writes
- [ ] LiveKit for collaborative planning
- [ ] Dark/light theme toggle
- [ ] Multi-user support
- [ ] Mobile responsive design

## 📝 API Endpoints

- `POST /api/plan` - Parse user query into subtasks
- `POST /api/agents/spawn` - Create agent tasks
- `POST /api/agents/run` - Execute agents and merge timeline
- `GET /api/memory` - Fetch user preferences
- `POST /api/memory/upsert` - Save user preferences
- `POST /api/tools/calendar/apply` - Apply timeline to calendar
- `GET /health` - Health check
- `WS /ws/events` - Real-time event stream

## 📄 License

MIT

## 🙏 Acknowledgments

Built with:
- [Anthropic Claude](https://www.anthropic.com/)
- [Fetch.ai](https://fetch.ai/)
- [Letta](https://www.letta.com/)
- [Composio](https://composio.dev/)

---

**Built for the weekend. Ship it!** 🚀

