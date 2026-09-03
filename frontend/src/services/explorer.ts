import axios from 'axios'
import { API_BASE } from './api'
import type { DatasetId, Difficulty } from '../types/dataset'

export type DataRow = Record<string, string | number | null>

export type DatasetSummary = {
  dataset_id: string
  dataset_name: string
  rows: number
  columns: number
  target_suggestion: string
  difficulty: string
  column_descriptions: Record<string, string>
  data_types: Record<string, string>
  missing_summary: Record<string, number>
  preview: DataRow[]
  suggested_questions: string[]
}

export type DatasetPayload = {
  dataset: DatasetId
  num_records: number
  include_missing_values: boolean
  include_outliers: boolean
  difficulty: Difficulty
}

export type PaginatedRowsResponse = {
  dataset_id: string
  page: number
  page_size: number
  total_rows: number
  total_pages: number
  rows: DataRow[]
}

export type NumericStats = {
  count: number
  mean: number
  median: number
  min: number
  max: number
  std_dev: number
}

export type DatasetProfile = {
  dataset_id: string
  rows: number
  columns: number
  missing_cells: number
  duplicate_rows: number
  numeric_columns: string[]
  categorical_columns: string[]
  outlier_counts: Record<string, number>
  numeric_stats: Record<string, NumericStats>
}

export type RowsQueryParams = {
  page: number
  page_size: number
  search?: string
  sort_by?: string
  sort_dir?: 'asc' | 'desc'
  filter_column?: string
  filter_value?: string
  numeric_min?: number
  numeric_max?: number
  missing_only?: boolean
}

export async function generateDataset(payload: DatasetPayload): Promise<DatasetSummary> {
  const response = await axios.post<DatasetSummary>(`${API_BASE}/datasets/generate`, payload)
  return response.data
}

export async function deleteDataset(datasetId: string): Promise<void> {
  await axios.delete(`${API_BASE}/datasets/${datasetId}`)
}

export async function fetchDatasetRowsPaginated(
  datasetId: string,
  params: RowsQueryParams,
): Promise<PaginatedRowsResponse> {
  const response = await axios.get<PaginatedRowsResponse>(`${API_BASE}/datasets/${datasetId}/rows/paginated`, {
    params,
  })
  return response.data
}

export async function fetchDatasetProfile(datasetId: string): Promise<DatasetProfile> {
  const response = await axios.get<DatasetProfile>(`${API_BASE}/datasets/${datasetId}/profile`)
  return response.data
}
