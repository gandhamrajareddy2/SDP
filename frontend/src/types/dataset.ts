export type DatasetId =
  | 'student_performance'
  | 'house_prices'
  | 'customer_churn'
  | 'movie_success'
  | 'retail_sales'
  | 'environmental_data'

export type Difficulty = 'beginner' | 'intermediate' | 'advanced'

export type ProjectMeta = {
  id: DatasetId
  title: string
  description: string
  domain: 'education' | 'real-estate' | 'business' | 'media' | 'retail' | 'environment'
  difficulty: Difficulty
}
