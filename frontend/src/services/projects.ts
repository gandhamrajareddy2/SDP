import type { ProjectMeta } from '../types/dataset'

export const PROJECTS: ProjectMeta[] = [
  {
    id: 'student_performance',
    title: 'Student Performance',
    description: 'Predict student final performance and interpret key factors.',
    domain: 'education',
    difficulty: 'beginner',
  },
  {
    id: 'house_prices',
    title: 'House Prices',
    description: 'Model pricing behavior from property characteristics.',
    domain: 'real-estate',
    difficulty: 'intermediate',
  },
  {
    id: 'customer_churn',
    title: 'Customer Churn',
    description: 'Analyze retention signals and identify churn risks.',
    domain: 'business',
    difficulty: 'intermediate',
  },
  {
    id: 'movie_success',
    title: 'Movie Success',
    description: 'Explore factors associated with box-office outcomes.',
    domain: 'media',
    difficulty: 'advanced',
  },
  {
    id: 'retail_sales',
    title: 'Retail Sales',
    description: 'Track demand patterns and support inventory decisions.',
    domain: 'retail',
    difficulty: 'intermediate',
  },
  {
    id: 'environmental_data',
    title: 'Environmental Data',
    description: 'Investigate pollution and weather-related indicators.',
    domain: 'environment',
    difficulty: 'advanced',
  },
]
