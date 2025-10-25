# TaskWeave 🧵

**Turn Natural Language into Actionable Plans with Multi-Agent AI**

> **TL;DR**: Type "Plan my Stanford CS midterms week" → Get a complete, conflict-free schedule in seconds. Three AI agents (Study, Meal, Calendar) coordinate in real-time, respect your preferences (sleep, breaks, dietary), and can apply directly to Google Calendar. Works perfectly in demo mode without any API keys.

TaskWeave is an intelligent productivity assistant that transforms your natural language requests into complete, personalized schedules. Simply describe what you need—like *"Plan my Stanford CS midterms week"* or *"Help me schedule a 3-day coding sprint"*—and watch as specialized AI agents coordinate to create a conflict-free timeline tailored to your preferences.

---

## 📖 Table of Contents

- [🎯 What Does TaskWeave Do?](#-what-does-taskweave-do)
- [✨ Real-World Examples](#-real-world-examples)
- [🎓 Why TaskWeave?](#-why-taskweave)
- [🚀 Quick Start](#-quick-start)
- [🎯 Demo Script](#-demo-script)
- [🏗️ How TaskWeave Works](#️-how-taskweave-works)
  - [High-Level Workflow](#high-level-workflow)
  - [Detailed Component Interaction](#detailed-component-interaction)
  - [Data Flow Diagram](#data-flow-diagram)
  - [Timeline Merge Rules](#timeline-merge-rules-the-intelligence)
  - [WebSocket Event Flow](#websocket-event-flow)
  - [Workflow Summary](#-workflow-summary)
  - [System Architecture](#️-system-architecture)
- [📋 Environment Variables](#-environment-variables)
- [✨ Key Features](#-key-features)
- [🎨 Tech Stack](#-tech-stack)
- [💡 Common Use Cases](#-common-use-cases)
- [📝 API Endpoints](#-api-endpoints)
- [🔐 Security & Privacy](#-security--privacy)
- [🚧 Future Enhancements](#-future-enhancements)

---

## 🎯 What Does TaskWeave Do?

TaskWeave solves the problem of **complex scheduling and planning** by:

### The Problem
You have a complex task (exam prep, project planning, weekly schedule) that requires:
- Breaking it down into actionable subtasks
- Coordinating different aspects (study time, meals, breaks, meetings)
- Respecting your personal constraints (sleep schedule, work hours, preferences)
- Avoiding conflicts and optimizing time allocation
- Integrating with your actual calendar

**Traditional approach:** Hours of manual planning, spreadsheet juggling, and calendar tetris.

### The TaskWeave Solution
1. **Type your request** in plain English (30 seconds)
2. **AI agents coordinate** to propose a complete schedule (5 seconds)
3. **Review and apply** your personalized timeline (30 seconds)

**Result:** A complete, optimized schedule in under a minute.

## ✨ Real-World Examples

### Example 1: Exam Preparation
```
You: "Plan my Stanford CS midterms week"

TaskWeave:
  📚 Study Agent → Creates 9 focused study blocks (3 per day, 90min each)
  🍽️ Meal Agent → Schedules healthy meals around study sessions
  📅 Calendar Agent → Blocks focused time and inserts 15min breaks
  
  Result: 27 events, zero conflicts, respects your sleep schedule
```

### Example 2: Project Sprint
```
You: "Help me schedule a 3-day coding sprint for my ML project"

TaskWeave:
  📚 Study Agent → Allocates deep work blocks for coding
  🍽️ Meal Agent → Plans meals to sustain energy
  📅 Calendar Agent → Protects your focus time from interruptions
  
  Result: Structured sprint schedule with built-in breaks
```

### Example 3: Adaptive Scheduling
```
You: Update preferences → Change sleep to 01:00-09:00 (night owl)
You: "Plan my Stanford CS midterms week"

TaskWeave:
  ✅ No events before 9 AM
  ✅ Study blocks shifted to afternoon/evening
  ✅ All preferences automatically applied
  
  Result: Personalized schedule that matches YOUR rhythm
```

## 🎓 Why TaskWeave?

Traditional productivity tools require you to:
- ❌ Manually break down complex tasks
- ❌ Juggle multiple calendars and tools
- ❌ Constantly check for scheduling conflicts
- ❌ Re-plan everything when one thing changes
- ❌ Remember your own preferences and constraints

TaskWeave flips this model:
- ✅ **Tell it what you want** (one sentence)
- ✅ **AI agents plan everything** (parallel processing)
- ✅ **Get a complete schedule** (conflict-free, personalized)
- ✅ **Adapt instantly** (change preferences, re-run)
- ✅ **Apply to real tools** (Google Calendar, Notion)

**It's like having a personal assistant who knows your schedule inside out.**

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

## 🏗️ How TaskWeave Works

TaskWeave uses a **multi-agent architecture** where specialized AI agents coordinate to solve complex scheduling tasks. Here's the complete workflow:

### High-Level Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  1️⃣  USER INPUT                                                         │
│      "Plan my Stanford CS midterms week"                               │
│                                                                         │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  2️⃣  PLANNING (Claude AI)                                               │
│      • Analyzes intent                                                 │
│      • Generates rationale                                             │
│      • Creates 3 subtasks (study, meal, calendar)                      │
│                                                                         │
│      Output:                                                           │
│      ✓ Subtask 1: "Create 3 focused study blocks per day..."          │
│      ✓ Subtask 2: "Schedule healthy meals and snacks..."              │
│      ✓ Subtask 3: "Block study time in calendar..."                   │
│                                                                         │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  3️⃣  ORCHESTRATION (Multi-Agent Coordination)                           │
│                                                                         │
│      ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│      │ 📚 Study     │  │ 🍽️  Meal      │  │ 📅 Calendar  │            │
│      │    Agent     │  │    Agent     │  │    Agent     │            │
│      └──────┬───────┘  └──────┬───────┘  └──────┬───────┘            │
│             │                  │                  │                    │
│             │  Fetch Memory    │                  │                    │
│             └──────────┬───────┴──────────────────┘                    │
│                        │                                               │
│                        ▼                                               │
│              ┌──────────────────┐                                      │
│              │  💾 Letta Memory │                                      │
│              │  (Preferences)   │                                      │
│              │                  │                                      │
│              │  • Sleep: 23-07  │                                      │
│              │  • Study: 90min  │                                      │
│              │  • Break: 15min  │                                      │
│              └──────────────────┘                                      │
│                                                                         │
│      Each agent proposes event blocks:                                │
│      • Study Agent: 9 study sessions (3/day × 3 days)                 │
│      • Meal Agent: 6 meals (lunch + dinner × 3 days)                  │
│      • Calendar Agent: 9 break blocks                                 │
│                                                                         │
│      Total: 24 raw event proposals                                    │
│                                                                         │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  4️⃣  TIMELINE MERGE (Conflict Resolution)                               │
│                                                                         │
│      Rules Applied:                                                    │
│      ✓ Remove events in sleep window (23:00 - 07:00)                  │
│      ✓ Keep events within work hours (08:00 - 22:00)                  │
│      ✓ Resolve overlaps by shifting forward                           │
│      ✓ Sort by start time, then agent name                            │
│                                                                         │
│      24 raw proposals → 21 conflict-free events                       │
│                                                                         │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  5️⃣  REAL-TIME STREAMING (WebSocket)                                    │
│                                                                         │
│      Events pushed to UI:                                             │
│      • AGENT_LOG: "Study agent starting..."                           │
│      • AGENT_LOG: "Meal agent proposed 6 blocks"                      │
│      • TIMELINE_UPDATE: [21 event blocks]                             │
│      • AGENTS_COMPLETE: "All agents finished"                         │
│                                                                         │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  6️⃣  VISUALIZATION (React UI)                                           │
│                                                                         │
│      ┌─────────────────────────────────────────────────────────┐      │
│      │  Terminal           │  Dashboard                        │      │
│      │  ─────────          │  ──────────                       │      │
│      │  [Logs streaming]   │  📅 Timeline (21 events)          │      │
│      │  • Parsing...       │  🤖 Agents (3 complete)           │      │
│      │  • Study agent...   │  💾 Memory (editable prefs)       │      │
│      │  • Timeline ready   │                                   │      │
│      └─────────────────────────────────────────────────────────┘      │
│                                                                         │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  7️⃣  CALENDAR INTEGRATION (Optional)                                    │
│                                                                         │
│      User clicks "Apply to Calendar"                                  │
│      → Composio Toolrouter → Google Calendar API                      │
│      → 21 events created in actual calendar                           │
│                                                                         │
│      (Dry-run mode: simulates without writing)                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Detailed Component Interaction

```
┌──────────────┐
│   Browser    │
│  (React UI)  │
└───────┬──────┘
        │ HTTP POST /api/plan
        │ { query: "Plan my midterms" }
        ▼
┌────────────────────────────────────────────┐
│         FastAPI Backend                    │
│                                            │
│  ┌──────────────────────────────────┐     │
│  │  Planning Router                  │     │
│  │  • Receives query                │     │
│  │  • Generates trace_id            │     │
│  └───────┬──────────────────────────┘     │
│          │                                 │
│          ▼                                 │
│  ┌──────────────────────────────────┐     │
│  │  Planner Service                  │     │
│  │  • Calls Anthropic client        │     │
│  │  • Returns 3 subtasks            │     │
│  └───────┬──────────────────────────┘     │
│          │                                 │
│          ▼                                 │
│  ┌──────────────────────────────────┐     │
│  │  Anthropic Adapter                │     │
│  │  • API call or mock response     │     │
│  │  • Returns JSON with subtasks    │     │
│  └───────┬──────────────────────────┘     │
│          │                                 │
└──────────┼─────────────────────────────────┘
           │
           │ Response: { subtasks: [...], rationale: "..." }
           ▼
┌──────────────┐
│   Browser    │ Now has 3 subtasks
└───────┬──────┘
        │ HTTP POST /api/agents/run
        │ { subtasks: [...] }
        ▼
┌────────────────────────────────────────────┐
│         FastAPI Backend                    │
│                                            │
│  ┌──────────────────────────────────┐     │
│  │  Orchestrator Service             │     │
│  │                                   │     │
│  │  For each subtask:               │     │
│  │    1. Get memory from Letta      │     │
│  │    2. Call Fetch agent           │     │
│  │    3. Emit AGENT_LOG events      │     │
│  │    4. Collect event blocks       │     │
│  └───────┬──────────────────────────┘     │
│          │                                 │
│          ▼                                 │
│  ┌──────────────────────────────────┐     │
│  │  Timeline Service                 │     │
│  │  • Merge all blocks              │     │
│  │  • Apply conflict resolution     │     │
│  │  • Return sorted timeline        │     │
│  └───────┬──────────────────────────┘     │
│          │                                 │
│          │ Throughout process:            │
│          │ WebSocket.send(AGENT_LOG)      │
│          │ WebSocket.send(TIMELINE_UPDATE)│
│          │                                 │
└──────────┼─────────────────────────────────┘
           │
           │ Response: { timeline: [21 events] }
           ▼
┌──────────────┐
│   Browser    │ Timeline displayed!
└──────────────┘
```

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      DATA TRANSFORMATIONS                   │
└─────────────────────────────────────────────────────────────┘

Natural Language Query
    "Plan my Stanford CS midterms week"
                    │
                    ▼
┌────────────────────────────────────────────────────────────┐
│ Claude API Response                                        │
│                                                            │
│ {                                                          │
│   "rationale": "Breaking down exam prep into study...",   │
│   "subtasks": [                                            │
│     {                                                      │
│       "id": "abc123",                                      │
│       "agent": "study_agent",                              │
│       "description": "Create 3 focused study blocks..."    │
│     },                                                     │
│     { ... meal_agent ... },                                │
│     { ... calendar_agent ... }                             │
│   ]                                                        │
│ }                                                          │
└────────────┬───────────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────────────┐
│ Agent Proposals (from Fetch AI / Mock)                     │
│                                                            │
│ Study Agent → [                                            │
│   { title: "Study Session 1", start: "2024-11-01T08:00",  │
│     end: "2024-11-01T09:30", source: "study_agent" },     │
│   { title: "Study Session 2", start: "2024-11-01T10:00",  │
│     ... },                                                 │
│   ... 7 more study blocks ...                             │
│ ]                                                          │
│                                                            │
│ Meal Agent → [                                             │
│   { title: "Lunch", start: "2024-11-01T12:00", ... },     │
│   ... 5 more meals ...                                    │
│ ]                                                          │
│                                                            │
│ Calendar Agent → [                                         │
│   { title: "Break", start: "2024-11-01T09:30", ... },     │
│   ... 8 more breaks ...                                   │
│ ]                                                          │
│                                                            │
│ Total: 24 raw event blocks                                │
└────────────┬───────────────────────────────────────────────┘
             │
             ▼ Timeline Service
             │ (applies merge rules)
             │
┌────────────┴───────────────────────────────────────────────┐
│ Merged Timeline (conflict-free)                            │
│                                                            │
│ [                                                          │
│   {                                                        │
│     "id": "evt_xyz",                                       │
│     "title": "Study Session 1 - Day 1",                    │
│     "start_iso": "2024-11-01T08:00:00",                    │
│     "end_iso": "2024-11-01T09:30:00",                      │
│     "source_agent": "study_agent",                         │
│     "status": "proposed"                                   │
│   },                                                       │
│   {                                                        │
│     "title": "Break",                                      │
│     "start_iso": "2024-11-01T09:30:00",                    │
│     "end_iso": "2024-11-01T09:45:00",                      │
│     "source_agent": "calendar_agent",                      │
│     "status": "proposed"                                   │
│   },                                                       │
│   ... 19 more events (sorted, no conflicts) ...           │
│ ]                                                          │
│                                                            │
│ Result: 21 optimized events                               │
└────────────┬───────────────────────────────────────────────┘
             │
             ▼ WebSocket
             │
┌────────────┴───────────────────────────────────────────────┐
│ React UI State                                             │
│                                                            │
│ {                                                          │
│   logs: [                                                  │
│     { timestamp: "10:30:15", agent: "System",             │
│       message: "Processing request..." },                 │
│     { agent: "study_agent", message: "Starting..." },     │
│     ...                                                    │
│   ],                                                       │
│   timeline: [ ... 21 events ... ],                        │
│   agents: [                                                │
│     { name: "study_agent", status: "complete" },          │
│     { name: "meal_agent", status: "complete" },           │
│     { name: "calendar_agent", status: "complete" }        │
│   ]                                                        │
│ }                                                          │
└────────────────────────────────────────────────────────────┘
```

### Timeline Merge Rules (The Intelligence)

TaskWeave's timeline service ensures conflict-free scheduling by applying these rules:

```
Input: 24 raw event proposals from agents
         │
         ▼
┌────────────────────────────────────────┐
│ Rule 1: Filter Sleep Window            │
│                                        │
│ User Memory: sleep 23:00 - 07:00      │
│ Remove any events in this window      │
│                                        │
│ 24 events → 23 events                 │
└────────┬───────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│ Rule 2: Enforce Work Hours             │
│                                        │
│ Keep only events 08:00 - 22:00        │
│                                        │
│ 23 events → 22 events                 │
└────────┬───────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│ Rule 3: Sort Chronologically           │
│                                        │
│ Sort by: (start_time, agent_name)     │
│                                        │
│ 22 events → 22 events (reordered)     │
└────────┬───────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│ Rule 4: Resolve Overlaps               │
│                                        │
│ For each event:                        │
│   if start < previous_end:             │
│     shift start = previous_end         │
│     adjust end accordingly             │
│                                        │
│ 22 events → 21 events (some shifted)  │
└────────┬───────────────────────────────┘
         │
         ▼
Output: 21 conflict-free events
```

### WebSocket Event Flow

Real-time updates keep the UI synchronized with backend processing:

```
Backend Processing              WebSocket Events           React UI Updates
─────────────────────          ─────────────────          ─────────────────

Plan endpoint called
        │
        ├──────────────────→ PLAN_COMPLETE ──────────→ Show subtasks
        │                    { subtasks: [...] }        Add log entry
        │
Orchestrator starts
        │
Study agent begins
        │
        ├──────────────────→ AGENT_LOG ──────────────→ Terminal: "Study
        │                    { agent: "study_agent",     agent starting..."
        │                      message: "Starting..." }
        │
Study agent proposes
        │
        ├──────────────────→ AGENT_LOG ──────────────→ Terminal: "Proposed
        │                    { message: "Proposed       9 blocks"
        │                      9 blocks" }
        │
Meal agent begins...
        │
        ├──────────────────→ AGENT_LOG ──────────────→ Terminal updates
        │
All agents complete
        │
Timeline merged
        │
        ├──────────────────→ TIMELINE_UPDATE ────────→ Timeline tab
        │                    { blocks: [...] }          populated with
        │                                               21 events
        │
        └──────────────────→ AGENTS_COMPLETE ────────→ Agent cards show
                             { block_count: 21 }        "complete" status
                                                        Toast notification
```

### 📊 Workflow Summary

Here's the complete process in simple terms:

1. **You type a request** → "Plan my Stanford CS midterms week"
2. **Claude breaks it down** → 3 specific subtasks for each agent type
3. **Agents work in parallel** → Each proposes event blocks based on their specialty
4. **Memory is consulted** → Your sleep schedule, study preferences are applied
5. **Timeline merges everything** → Resolves conflicts, sorts chronologically
6. **UI updates in real-time** → WebSocket streams progress logs and events
7. **You review and apply** → See the complete schedule, apply to calendar

**Total time:** Under 10 seconds from request to complete timeline.

### 🏛️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         TASKWEAVE SYSTEM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐     │
│  │                   FRONTEND LAYER                      │     │
│  │              (React + TypeScript + Vite)              │     │
│  │                                                       │     │
│  │  Components:                                          │     │
│  │  • Terminal (input + logs)                            │     │
│  │  • Timeline (event visualization)                     │     │
│  │  • AgentCard (status display)                         │     │
│  │  • MemoryPanel (preferences editor)                   │     │
│  │                                                       │     │
│  │  Libraries:                                           │     │
│  │  • API Client (REST calls)                            │     │
│  │  • WebSocket Hook (real-time events)                  │     │
│  │  • Type Definitions (full type safety)                │     │
│  └───────────────┬───────────────────────────────────────┘     │
│                  │                                             │
│         HTTP/REST │ WebSocket                                  │
│                  │                                             │
│  ┌───────────────┴───────────────────────────────────────┐     │
│  │                   BACKEND LAYER                       │     │
│  │               (Python FastAPI + Uvicorn)              │     │
│  │                                                       │     │
│  │  API Routers:                                         │     │
│  │  • /api/plan         (planning endpoint)              │     │
│  │  • /api/agents/run   (agent execution)                │     │
│  │  • /api/memory/*     (preferences)                    │     │
│  │  • /api/tools/*      (calendar integration)           │     │
│  │  • /ws/events        (WebSocket stream)               │     │
│  │                                                       │     │
│  │  Services:                                            │     │
│  │  • Planner        (intent → subtasks)                 │     │
│  │  • Orchestrator   (multi-agent coordination)          │     │
│  │  • Timeline       (conflict resolution)               │     │
│  │  • EventBus       (pub/sub for WebSocket)             │     │
│  │                                                       │     │
│  │  Adapters (with Mock Fallbacks):                      │     │
│  │  • Anthropic      (Claude API)                        │     │
│  │  • Fetch AI       (Agent orchestration)               │     │
│  │  • Letta          (Memory storage)                    │     │
│  │  • Composio       (Tool execution)                    │     │
│  └───────────────┬───────────────────────────────────────┘     │
│                  │                                             │
│         Optional │ API Calls                                   │
│                  │                                             │
│  ┌───────────────┴───────────────────────────────────────┐     │
│  │              EXTERNAL SERVICES LAYER                  │     │
│  │            (All Optional - Mock Fallbacks)            │     │
│  │                                                       │     │
│  │  • Anthropic Claude    (Intent parsing)               │     │
│  │  • Fetch AI Agentverse (Agent coordination)           │     │
│  │  • Letta Cloud         (Persistent memory)            │     │
│  │  • Composio Toolrouter (Calendar/Notion integration)  │     │
│  │  • Elasticsearch       (Optional: centralized logs)   │     │
│  └───────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Key Design Principles:
─────────────────────
✓ Separation of Concerns: Frontend ↔ Backend ↔ External Services
✓ Mock-First: Works without external APIs for demos
✓ Event-Driven: WebSocket streaming for real-time updates
✓ Type-Safe: TypeScript + Pydantic for end-to-end safety
✓ Testable: Comprehensive tests at every layer
✓ Extensible: Easy to add new agents, tools, and services
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

## ✨ Key Features

### 🧠 Intelligent Planning
- **Natural Language Understanding**: Type requests in plain English—no commands to memorize
- **Context-Aware**: Claude analyzes your intent and creates a strategic breakdown
- **Explainable AI**: Every decision comes with a rationale explaining the approach

### 🤖 Multi-Agent Coordination
- **Specialized Agents**: Three dedicated agents (Study 📚, Meal 🍽️, Calendar 📅) work in parallel
- **Autonomous Proposals**: Each agent independently suggests optimal event blocks
- **Collaborative Intelligence**: Agents share access to your preferences for coordinated planning

### 💾 Stateful Memory
- **Persistent Preferences**: Your sleep schedule, study block length, and dietary needs are remembered
- **Adaptive Scheduling**: Timeline automatically adjusts when you update preferences
- **Privacy-First**: Memory stored locally (in-memory) or optionally in Letta Cloud

### 🔀 Smart Timeline Merging
- **Zero Conflicts**: Automatically resolves overlapping events
- **Respects Boundaries**: No events during sleep hours (23:00-07:00 by default)
- **Enforces Breaks**: Inserts 15-minute breaks between study blocks
- **Work Hour Optimization**: Keeps schedule within productive hours (8 AM - 10 PM)

### ⚡ Real-Time Experience
- **WebSocket Streaming**: See agents working in real-time as logs stream to the terminal
- **Live Updates**: Timeline populates dynamically as agents complete their work
- **Instant Feedback**: Toast notifications for successful operations

### 🎨 Beautiful Interface
- **Terminal-Inspired UI**: Warp-style command interface with syntax highlighting
- **Color-Coded Timeline**: Visual distinction between study (blue), meal (green), and calendar (purple) blocks
- **Tabbed Dashboard**: Seamlessly switch between Timeline, Agents, and Memory views
- **Responsive Design**: Clean, modern UI built with Tailwind CSS

### 🔌 External Integrations
- **Google Calendar** (via Composio): Apply your timeline to actual calendar events
- **Dry-Run Mode**: Test integrations safely without making changes
- **Mock Fallbacks**: Fully functional demo mode without any API keys
- **Extensible Architecture**: Easy to add Notion, Slack, or other tools

### 🛡️ Production Ready
- **Docker Deployment**: One-command setup with docker-compose
- **Comprehensive Testing**: pytest (backend) + vitest (frontend)
- **Error Handling**: Graceful fallbacks and informative error messages
- **Request Tracing**: Every request gets a unique trace_id for debugging
- **Security**: CORS protection, input validation, no secrets logged

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

## 💡 Common Use Cases

### 📚 Students
```
"Plan my finals week with 3 exams"
"Schedule study time for CS, Math, and Physics"
"Help me balance study and social time this week"
```

### 👨‍💻 Developers
```
"Schedule a 3-day coding sprint for my ML project"
"Plan my week with 4 feature implementations"
"Organize hackathon prep with team meetings"
```

### 📊 Project Managers
```
"Plan sprint planning week with daily standups"
"Schedule project review meetings and prep time"
"Organize quarterly planning with executive sessions"
```

### 🏃 Fitness Enthusiasts
```
"Plan training schedule for marathon prep"
"Schedule gym sessions around work meetings"
"Balance workout, recovery, and nutrition this week"
```

### 🎨 Creative Professionals
```
"Schedule client work with creative brainstorming time"
"Plan content creation week with posting schedule"
"Organize portfolio work around client deadlines"
```

**The Pattern**: Describe your goal → Agents create the structure → You review and apply

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

