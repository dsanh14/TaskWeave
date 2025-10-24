/**
 * TypeScript types for TaskWeave frontend
 */

export enum AgentType {
  STUDY_AGENT = 'study_agent',
  MEAL_AGENT = 'meal_agent',
  CALENDAR_AGENT = 'calendar_agent',
}

export enum EventStatus {
  PROPOSED = 'proposed',
  APPLIED = 'applied',
}

export enum EventType {
  AGENT_LOG = 'AGENT_LOG',
  TIMELINE_UPDATE = 'TIMELINE_UPDATE',
  ERROR = 'ERROR',
  PLAN_COMPLETE = 'PLAN_COMPLETE',
  AGENTS_SPAWNED = 'AGENTS_SPAWNED',
  AGENTS_COMPLETE = 'AGENTS_COMPLETE',
}

export interface Subtask {
  id: string
  agent: AgentType
  description: string
}

export interface EventBlock {
  id: string
  title: string
  start_iso: string
  end_iso: string
  source_agent: string
  status: EventStatus
}

export interface MemoryPrefs {
  user_id: string
  sleep_start: string
  sleep_end: string
  break_minutes: number
  study_block_minutes: number
  dietary: string | null
}

export interface PlanRequest {
  user_id: string
  query: string
  dry_run: boolean
}

export interface PlanResponse {
  subtasks: Subtask[]
  rationale: string
  trace_id: string
}

export interface AgentRunRequest {
  user_id: string
  subtasks: Subtask[]
  trace_id: string
}

export interface AgentRunResponse {
  timeline: EventBlock[]
  trace_id: string
}

export interface MemoryGetResponse {
  prefs: MemoryPrefs
  trace_id: string
}

export interface MemoryUpsertRequest {
  prefs: MemoryPrefs
}

export interface MemoryUpsertResponse {
  prefs: MemoryPrefs
  trace_id: string
}

export interface ApplyCalendarRequest {
  user_id: string
  blocks: EventBlock[]
  dry_run: boolean
}

export interface ApplyCalendarResponse {
  applied_count: number
  dry_run: boolean
  trace_id: string
}

export interface ServerEvent {
  type: EventType
  payload: any
  trace_id?: string
}

export interface AgentLogPayload {
  agent: string
  message: string
  level: string
}

export interface TimelineUpdatePayload {
  user_id: string
  blocks: EventBlock[]
}

export interface ErrorPayload {
  message: string
  details?: string
}

export interface LogEntry {
  timestamp: string
  message: string
  level: string
  agent?: string
}

export interface AgentInfo {
  id: string
  name: string
  status: 'idle' | 'running' | 'complete'
  lastAction?: string
  tokens?: number
}

