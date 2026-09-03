import axios from 'axios'
import { API_BASE } from './api'

export type DatasetRecord = {
  dataset_id: string
  dataset_name: string
  rows_count: number
  columns_count: number
  difficulty: string
  include_missing_values: boolean
  include_outliers: boolean
  created_at: string
}

export async function fetchRecentDatasets(limit = 20): Promise<DatasetRecord[]> {
  const response = await axios.get<DatasetRecord[]>(`${API_BASE}/datasets`, {
    params: { limit },
  })
  return response.data
}
