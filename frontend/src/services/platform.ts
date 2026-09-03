import axios from 'axios'
import { API_BASE } from './api'

export type DatasetVersion = {
  dataset_name: string
  version_number: number
  dataset_id: string
  config_json: string
  metrics_json: string
  created_at: string
}

export type SessionRecord = {
  session_id: string
  name: string
  dataset_id: string | null
  state_json: string
  created_at: string
  updated_at: string
}

export type ProgressSummary = {
  total_events: number
  by_module: Record<string, number>
}

export type ProgressEventPayload = {
  module: string
  event_type: string
  score?: number
  metadata_json?: string
}

export async function fetchVersions(datasetName: string, limit = 20): Promise<DatasetVersion[]> {
  const response = await axios.get<DatasetVersion[]>(`${API_BASE}/datasets/${datasetName}/versions`, {
    params: { limit },
  })
  return response.data
}

export async function listSessions(limit = 50): Promise<SessionRecord[]> {
  const response = await axios.get<SessionRecord[]>(`${API_BASE}/sessions`, { params: { limit } })
  return response.data
}

export async function createSession(payload: {
  name: string
  dataset_id?: string
  state_json?: string
}): Promise<SessionRecord> {
  const response = await axios.post<SessionRecord>(`${API_BASE}/sessions`, {
    name: payload.name,
    dataset_id: payload.dataset_id ?? null,
    state_json: payload.state_json ?? '{}',
  })
  return response.data
}

export async function updateSession(
  sessionId: string,
  payload: { name: string; dataset_id?: string; state_json?: string },
): Promise<SessionRecord> {
  const response = await axios.put<SessionRecord>(`${API_BASE}/sessions/${sessionId}`, {
    name: payload.name,
    dataset_id: payload.dataset_id ?? null,
    state_json: payload.state_json ?? '{}',
  })
  return response.data
}

export async function duplicateSession(sessionId: string): Promise<SessionRecord> {
  const response = await axios.post<SessionRecord>(`${API_BASE}/sessions/${sessionId}/duplicate`)
  return response.data
}

export async function deleteSession(sessionId: string): Promise<void> {
  await axios.delete(`${API_BASE}/sessions/${sessionId}`)
}

export async function fetchProgressSummary(): Promise<ProgressSummary> {
  const response = await axios.get<ProgressSummary>(`${API_BASE}/progress/summary`)
  return response.data
}

export async function logProgressEvent(payload: ProgressEventPayload): Promise<void> {
  await axios.post(`${API_BASE}/progress/events`, {
    module: payload.module,
    event_type: payload.event_type,
    score: payload.score,
    metadata_json: payload.metadata_json ?? '{}',
  })
}
