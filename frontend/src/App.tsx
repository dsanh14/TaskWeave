/**
 * Main App component
 */

import { useState, useEffect, useCallback } from 'react'
import { Terminal } from './components/Terminal'
import { Timeline } from './components/Timeline'
import { AgentCard } from './components/AgentCard'
import { MemoryPanel } from './components/MemoryPanel'
import { Toast } from './components/Toast'
import { useWebSocket } from './hooks/useWebSocket'
import { apiClient } from './lib/api'
import type {
  LogEntry,
  EventBlock,
  MemoryPrefs,
  AgentInfo,
  ServerEvent,
  EventType,
  AgentLogPayload,
  TimelineUpdatePayload,
  ErrorPayload,
} from './lib/types'

const USER_ID = 'demo_user_1'

export default function App() {
  // State
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [timeline, setTimeline] = useState<EventBlock[]>([])
  const [memory, setMemory] = useState<MemoryPrefs>({
    user_id: USER_ID,
    sleep_start: '23:00',
    sleep_end: '07:00',
    break_minutes: 15,
    study_block_minutes: 90,
    dietary: null,
  })
  const [agents, setAgents] = useState<AgentInfo[]>([
    {
      id: 'study_agent',
      name: 'study_agent',
      status: 'idle',
    },
    {
      id: 'meal_agent',
      name: 'meal_agent',
      status: 'idle',
    },
    {
      id: 'calendar_agent',
      name: 'calendar_agent',
      status: 'idle',
    },
  ])

  const [activeTab, setActiveTab] = useState<'timeline' | 'agents' | 'memory'>(
    'timeline'
  )
  const [isProcessing, setIsProcessing] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [isApplying, setIsApplying] = useState(false)
  const [toast, setToast] = useState<{
    message: string
    type: 'success' | 'error' | 'info'
  } | null>(null)

  // Load memory on mount
  useEffect(() => {
    loadMemory()
  }, [])

  const loadMemory = async () => {
    try {
      const response = await apiClient.getMemory(USER_ID)
      setMemory(response.prefs)
      addLog('System', 'Loaded user preferences')
    } catch (error) {
      console.error('Failed to load memory:', error)
      addLog('System', 'Using default preferences', 'warning')
    }
  }

  // WebSocket event handler
  const handleWebSocketEvent = useCallback((event: ServerEvent) => {
    switch (event.type) {
      case 'AGENT_LOG':
        const logPayload = event.payload as AgentLogPayload
        addLog(logPayload.agent, logPayload.message)
        break

      case 'TIMELINE_UPDATE':
        const timelinePayload = event.payload as TimelineUpdatePayload
        setTimeline(timelinePayload.blocks)
        addLog('System', `Timeline updated with ${timelinePayload.blocks.length} events`)
        break

      case 'ERROR':
        const errorPayload = event.payload as ErrorPayload
        addLog('System', `Error: ${errorPayload.message}`, 'error')
        showToast(errorPayload.message, 'error')
        break

      case 'PLAN_COMPLETE':
        addLog('System', 'Planning complete')
        break

      case 'AGENTS_COMPLETE':
        addLog('System', 'All agents completed')
        setAgents((prev) =>
          prev.map((agent) => ({ ...agent, status: 'complete' }))
        )
        setIsProcessing(false)
        showToast('Timeline generated successfully!', 'success')
        break

      default:
        console.log('Unknown event type:', event.type)
    }
  }, [])

  // WebSocket connection
  const { isConnected } = useWebSocket({
    onEvent: handleWebSocketEvent,
    onConnect: () => {
      addLog('System', 'Connected to server')
    },
    onDisconnect: () => {
      addLog('System', 'Disconnected from server', 'warning')
    },
  })

  // Helper functions
  const addLog = (
    agent: string,
    message: string,
    level: string = 'info'
  ) => {
    const log: LogEntry = {
      timestamp: new Date().toLocaleTimeString(),
      message,
      level,
      agent,
    }
    setLogs((prev) => [...prev, log])
  }

  const showToast = (
    message: string,
    type: 'success' | 'error' | 'info' = 'info'
  ) => {
    setToast({ message, type })
  }

  // Handler: Terminal submit
  const handleTerminalSubmit = async (query: string) => {
    setIsProcessing(true)
    addLog('User', query)
    addLog('System', 'Processing request...')

    // Reset agents to running
    setAgents((prev) =>
      prev.map((agent) => ({ ...agent, status: 'running' }))
    )

    try {
      // Step 1: Plan
      addLog('System', 'Parsing intent with Claude...')
      const planResponse = await apiClient.plan({
        user_id: USER_ID,
        query,
        dry_run: true,
      })

      addLog('Planner', planResponse.rationale)

      // Step 2: Run agents
      addLog('System', 'Coordinating agents...')
      const agentResponse = await apiClient.runAgents({
        user_id: USER_ID,
        subtasks: planResponse.subtasks,
        trace_id: planResponse.trace_id,
      })

      setTimeline(agentResponse.timeline)
      addLog('System', `Generated ${agentResponse.timeline.length} event blocks`)

      setAgents((prev) =>
        prev.map((agent) => ({ ...agent, status: 'complete' }))
      )
      setIsProcessing(false)

      showToast('Timeline generated successfully!', 'success')
    } catch (error) {
      console.error('Processing error:', error)
      addLog('System', 'Failed to process request', 'error')
      setIsProcessing(false)
      setAgents((prev) =>
        prev.map((agent) => ({ ...agent, status: 'idle' }))
      )
      showToast('Failed to process request', 'error')
    }
  }

  // Handler: Apply to calendar
  const handleApplyCalendar = async (dryRun: boolean) => {
    setIsApplying(true)
    addLog('System', `Applying ${timeline.length} events to calendar...`)

    try {
      const response = await apiClient.applyCalendar({
        user_id: USER_ID,
        blocks: timeline,
        dry_run: dryRun,
      })

      const mode = response.dry_run ? 'DRY-RUN' : 'APPLIED'
      addLog(
        'Calendar',
        `${mode}: ${response.applied_count} events processed`
      )
      showToast(
        `${mode}: ${response.applied_count} events processed`,
        'success'
      )
    } catch (error) {
      console.error('Apply calendar error:', error)
      addLog('System', 'Failed to apply to calendar', 'error')
      showToast('Failed to apply to calendar', 'error')
    } finally {
      setIsApplying(false)
    }
  }

  // Handler: Save memory
  const handleSaveMemory = async (prefs: MemoryPrefs) => {
    setIsSaving(true)
    addLog('System', 'Saving preferences...')

    try {
      const response = await apiClient.upsertMemory({ prefs })
      setMemory(response.prefs)
      addLog('System', 'Preferences saved successfully')
      showToast('Preferences saved!', 'success')
    } catch (error) {
      console.error('Save memory error:', error)
      addLog('System', 'Failed to save preferences', 'error')
      showToast('Failed to save preferences', 'error')
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                TaskWeave
              </h1>
              <p className="text-sm text-gray-500">
                Multi-Agent Productivity Assistant
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div
                className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm ${
                  isConnected
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                }`}
              >
                <span
                  className={`w-2 h-2 rounded-full ${
                    isConnected ? 'bg-green-500' : 'bg-red-500'
                  }`}
                />
                <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left: Terminal */}
          <div className="lg:col-span-1">
            <Terminal
              logs={logs}
              onSubmit={handleTerminalSubmit}
              isProcessing={isProcessing}
            />
          </div>

          {/* Right: Dashboard */}
          <div className="lg:col-span-1">
            {/* Tab navigation */}
            <div className="bg-white rounded-t-lg border-b border-gray-200 px-6 py-3">
              <nav className="flex space-x-6">
                {[
                  { id: 'timeline', label: 'Timeline' },
                  { id: 'agents', label: 'Agents' },
                  { id: 'memory', label: 'Memory' },
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={`pb-2 border-b-2 font-medium text-sm transition-colors ${
                      activeTab === tab.id
                        ? 'border-primary-600 text-primary-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700'
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </nav>
            </div>

            {/* Tab content */}
            <div className="bg-white rounded-b-lg shadow-md p-6 min-h-[500px]">
              {activeTab === 'timeline' && (
                <Timeline
                  blocks={timeline}
                  onApply={handleApplyCalendar}
                  isApplying={isApplying}
                />
              )}

              {activeTab === 'agents' && (
                <div>
                  <h2 className="text-xl font-bold text-gray-900 mb-4">
                    Agents
                  </h2>
                  <div className="space-y-4">
                    {agents.map((agent) => (
                      <AgentCard key={agent.id} agent={agent} />
                    ))}
                  </div>
                </div>
              )}

              {activeTab === 'memory' && (
                <MemoryPanel
                  prefs={memory}
                  onSave={handleSaveMemory}
                  isSaving={isSaving}
                />
              )}
            </div>
          </div>
        </div>
      </main>

      {/* Toast notifications */}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  )
}

