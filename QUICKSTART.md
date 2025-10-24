# TaskWeave Quickstart Guide

## 🚀 Get Started in 60 Seconds

### Option 1: Docker (Recommended)

```bash
# 1. Clone or navigate to TaskWeave directory
cd TaskWeave

# 2. Start everything with Docker
docker-compose up --build
```

That's it! Open http://localhost:5173 in your browser.

### Option 2: Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend (in another terminal):**
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

## 📝 Try the Demo

1. **Open the app** at http://localhost:5173

2. **Type in the terminal:**
   ```
   Plan my Stanford CS midterms week
   ```

3. **Watch the magic:**
   - Claude breaks down your request
   - Three agents (Study, Meal, Calendar) propose blocks
   - Timeline merges everything respecting your preferences

4. **Explore the tabs:**
   - **Timeline**: See your schedule
   - **Agents**: View agent status
   - **Memory**: Edit preferences (sleep hours, study blocks, breaks)

5. **Apply to calendar:**
   - Click "Apply to Calendar" (dry-run mode is ON by default)
   - See simulated calendar integration

6. **Edit preferences:**
   - Go to **Memory** tab
   - Change sleep hours (e.g., 22:30 - 06:30)
   - Update study block length
   - Add dietary preferences
   - Click "Save Preferences"

7. **Re-run with new preferences:**
   - Type another request
   - See timeline adjust to your new schedule!

## 🎭 Demo Scenarios

### Scenario 1: Exam Prep
```
Plan my Stanford CS midterms week
```

### Scenario 2: Project Work
```
Help me schedule a 3-day coding sprint for my ML project
```

### Scenario 3: Balanced Schedule
```
Organize my week with study, exercise, and social time
```

## 🔧 Configuration

### No API Keys Required!
The system works fully in **mock mode** without any API keys. All AI integrations have intelligent fallbacks.

### Add Real API Keys (Optional)
Create a `.env` file in the root directory:

```bash
# Anthropic Claude (for better planning)
ANTHROPIC_API_KEY=sk-ant-...

# Fetch AI (for real agent orchestration)
FETCH_API_KEY=sk-fetch-...

# Letta Cloud (for persistent memory)
LETTA_API_KEY=sk-letta-...

# Composio (for real calendar integration)
COMPOSIO_API_KEY=sk-composio-...
```

## 🧪 Run Tests

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

## 🐛 Troubleshooting

### Port conflicts?
Edit `docker-compose.yml` or use environment variables:
```bash
PORT=8001 docker-compose up
```

### WebSocket not connecting?
Check that backend is running on port 8000 and CORS is configured correctly.

### Frontend not loading?
Make sure `VITE_API_BASE_URL=http://localhost:8000` is set (or create `.env` file in frontend directory).

## 📚 Learn More

- **API Documentation**: http://localhost:8000/docs (FastAPI auto-generated)
- **Architecture**: See [README.md](./README.md)
- **Code Structure**: Browse `/backend` and `/frontend` directories

## 🎉 Next Steps

1. **Customize agents**: Edit `/backend/app/adapters/fetch_client.py`
2. **Add new tools**: Create adapters in `/backend/app/adapters/`
3. **Enhance UI**: Modify components in `/frontend/src/components/`
4. **Real integrations**: Add API keys and implement real API calls

Happy planning! 🚀

