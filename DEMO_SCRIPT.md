# TaskWeave Demo Script

## 🎬 5-Minute Demo Walkthrough

### Setup (30 seconds)
```bash
docker-compose up --build
# Wait for services to start
# Open http://localhost:5173
```

---

### Act 1: The Magic (2 minutes)

**Narrator:** "TaskWeave is a multi-agent productivity assistant. Watch what happens when I ask it to plan my week."

**Action:**
1. Type in terminal: `Plan my Stanford CS midterms week`
2. Press Enter

**Observe:**
- Terminal streams logs in real-time
- "Processing request..."
- "Parsing intent with Claude..."
- Claude returns rationale: "Breaking down exam preparation into study sessions, meal planning..."
- "Coordinating agents..."
- Three agents light up: Study 📚, Meal 🍽️, Calendar 📅
- Each agent proposes blocks
- "Generated 27 event blocks"
- Timeline tab fills with color-coded events

**Narrator:** "In seconds, three AI agents coordinated to create a complete study schedule with meals, breaks, and calendar blocks."

---

### Act 2: The Intelligence (1.5 minutes)

**Narrator:** "The system respects my personal preferences. Let me show you."

**Action:**
1. Click **Memory** tab
2. Show current preferences:
   - Sleep: 23:00 - 07:00
   - Study blocks: 90 minutes
   - Breaks: 15 minutes
   - Dietary: (empty)

**Narrator:** "Let's say I'm a night owl and vegetarian."

**Action:**
3. Change sleep to: 01:00 - 09:00
4. Add dietary: "vegetarian"
5. Click "Save Preferences"
6. See toast: "Preferences saved!"

**Narrator:** "Now watch what happens when I re-run the same request."

**Action:**
7. Click back to Terminal
8. Type: `Plan my Stanford CS midterms week`
9. Press Enter

**Observe:**
- Timeline adjusts
- No events before 09:00 AM
- Meal blocks say "(vegetarian)"
- Study blocks respect new schedule

**Narrator:** "The agents learned my preferences and adapted the entire schedule automatically."

---

### Act 3: The Integration (1 minute)

**Narrator:** "Now let's apply this to my actual calendar."

**Action:**
1. Go to **Timeline** tab
2. Show the organized schedule:
   - Monday: 3 study blocks, lunch, dinner, breaks
   - Tuesday: Similar structure
   - Wednesday: Full day planned
3. Point to "Dry-run mode" checkbox (checked)
4. Click **Apply to Calendar**

**Observe:**
- Terminal logs: "Applying 27 events to calendar..."
- "DRY-RUN: Would apply 27 blocks to calendar"
- Toast: "DRY-RUN: 27 events processed"

**Narrator:** "In dry-run mode, it simulates the integration. With a real Composio API key, these would go straight to Google Calendar."

---

### Act 4: The Architecture (30 seconds)

**Narrator:** "Under the hood:"

**Points to Terminal logs:**
- "See Claude parsing my intent"
- "Fetch AI agents coordinating in parallel"
- "Letta remembering my preferences"
- "Composio ready to execute on real tools"

**Show Agents tab:**
- Study Agent: Complete ✅
- Meal Agent: Complete ✅
- Calendar Agent: Complete ✅

**Narrator:** "All orchestrated through WebSockets for real-time updates."

---

### Finale (10 seconds)

**Narrator:** "TaskWeave: From natural language to actionable schedule in seconds. Built for the weekend. Ready to ship."

**Type one more:**
```
Help me schedule a 3-day coding sprint
```

**Watch it work again instantly.**

**End screen:**
```
TaskWeave MVP
✅ Multi-agent coordination
✅ Stateful memory
✅ Real-time streaming
✅ Calendar integration
✅ Full mock mode - no API keys needed

github.com/youruser/taskweave
```

---

## 🎯 Key Talking Points

1. **Natural Language In**: Just type what you want
2. **AI Agents Out**: Specialized agents handle different aspects
3. **Learns Preferences**: Remembers and adapts to your schedule
4. **Real Integrations**: Ready for Google Calendar, Notion, etc.
5. **Weekend Project**: Full stack, production-ready architecture
6. **Mock Mode**: Works perfectly without any API keys

## 💡 Demo Tips

- Keep terminal logs visible - they tell the story
- Emphasize real-time WebSocket updates
- Show both the problem (complex scheduling) and solution (natural language)
- Highlight the preference learning - it's the "wow" moment
- End with dry-run mode to show safety and real integration readiness

## 🎤 Q&A Prep

**Q: Does it need API keys?**
A: No! Full mock mode for demo. Add keys for production.

**Q: Can it integrate with my calendar?**
A: Yes, via Composio. Currently in dry-run mode.

**Q: How do agents coordinate?**
A: FastAPI backend with WebSocket streaming, event bus pattern.

**Q: Is memory persistent?**
A: In-memory for demo. Add Letta API key for cloud persistence.

**Q: Can I add more agents?**
A: Absolutely! Architecture is extensible.

