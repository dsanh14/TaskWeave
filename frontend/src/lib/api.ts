/**
 * API client for TaskWeave backend
 */

import type {
  PlanRequest,
  PlanResponse,
  AgentRunRequest,
  AgentRunResponse,
  MemoryGetResponse,
  MemoryUpsertRequest,
  MemoryUpsertResponse,
  ApplyCalendarRequest,
  ApplyCalendarResponse,
} from './types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

class APIClient {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      })

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // Planning
  async plan(request: PlanRequest): Promise<PlanResponse> {
    return this.request<PlanResponse>('/api/plan', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }

  // Agents
  async runAgents(request: AgentRunRequest): Promise<AgentRunResponse> {
    return this.request<AgentRunResponse>('/api/agents/run', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }

  // Memory
  async getMemory(userId: string): Promise<MemoryGetResponse> {
    return this.request<MemoryGetResponse>(
      `/api/memory?user_id=${encodeURIComponent(userId)}`
    )
  }

  async upsertMemory(
    request: MemoryUpsertRequest
  ): Promise<MemoryUpsertResponse> {
    return this.request<MemoryUpsertResponse>('/api/memory/upsert', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }

  // Tools
  async applyCalendar(
    request: ApplyCalendarRequest
  ): Promise<ApplyCalendarResponse> {
    return this.request<ApplyCalendarResponse>('/api/tools/calendar/apply', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }

  // Health
  async health(): Promise<{ status: string; version: string }> {
    return this.request('/health')
  }
}

export const apiClient = new APIClient()

