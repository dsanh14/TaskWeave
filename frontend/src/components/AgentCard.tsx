/**
 * Agent card component showing agent status
 */

import type { AgentInfo } from '../lib/types'

interface AgentCardProps {
  agent: AgentInfo
}

export function AgentCard({ agent }: AgentCardProps) {
  const statusColors = {
    idle: 'status-idle',
    running: 'status-running',
    complete: 'status-complete',
  }

  const agentIcons = {
    study_agent: '📚',
    meal_agent: '🍽️',
    calendar_agent: '📅',
  }

  const icon = agentIcons[agent.name as keyof typeof agentIcons] || '🤖'

  return (
    <div className="agent-card">
      <div className="text-3xl">{icon}</div>
      <div className="flex-1">
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-semibold text-gray-900 capitalize">
            {agent.name.replace('_', ' ')}
          </h3>
          <span className={statusColors[agent.status]}>{agent.status}</span>
        </div>
        {agent.lastAction && (
          <p className="text-sm text-gray-600 mb-1">{agent.lastAction}</p>
        )}
        {agent.tokens !== undefined && (
          <p className="text-xs text-gray-500">Tokens: {agent.tokens}</p>
        )}
      </div>
    </div>
  )
}

