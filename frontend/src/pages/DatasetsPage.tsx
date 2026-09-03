import { useMemo, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import ModulePage from '../components/ModulePage'
import { fetchRecentDatasets } from '../services/datasets'
import { PROJECTS } from '../services/projects'

export default function DatasetsPage() {
  const [searchText, setSearchText] = useState('')
  const recentDatasetsQuery = useQuery({
    queryKey: ['recent-datasets', 'hub'],
    queryFn: () => fetchRecentDatasets(100),
  })

  const filteredProjects = useMemo(() => {
    const query = searchText.trim().toLowerCase()
    if (!query) {
      return PROJECTS
    }
    return PROJECTS.filter(
      (project) =>
        project.title.toLowerCase().includes(query) ||
        project.description.toLowerCase().includes(query) ||
        project.domain.toLowerCase().includes(query),
    )
  }, [searchText])

  const byName = useMemo(() => {
    const map = new Map<string, { rows: number; columns: number; count: number }>()
    for (const item of recentDatasetsQuery.data ?? []) {
      const key = item.dataset_name
      const existing = map.get(key)
      if (!existing) {
        map.set(key, { rows: item.rows_count, columns: item.columns_count, count: 1 })
      } else {
        existing.rows = item.rows_count
        existing.columns = item.columns_count
        existing.count += 1
      }
    }
    return map
  }, [recentDatasetsQuery.data])

  return (
    <ModulePage
      title="Dataset Hub"
      purpose="Choose project datasets with context and learning objective alignment."
      status="in-progress"
      nextActionLabel="Generate and Explore Dataset"
      nextActionTo="/data-explorer"
    >
      <section className="card">
        <label className="search-field">
          Search datasets
          <input
            type="text"
            value={searchText}
            onChange={(event) => setSearchText(event.target.value)}
            placeholder="Search by name, description, or domain"
          />
        </label>
        {recentDatasetsQuery.isLoading && <p>Loading recent dataset activity...</p>}
        {recentDatasetsQuery.isError && <p>Could not load recent generated dataset stats.</p>}
      </section>

      <section className="card dataset-grid">
        {filteredProjects.map((project) => (
          <article key={project.id} className="dataset-card">
            <h2>{project.title}</h2>
            <p>{project.description}</p>
            <p>Domain: {project.domain}</p>
            <p>Difficulty: {project.difficulty}</p>
            <p>Recent generated versions: {byName.get(project.id)?.count ?? 0}</p>
            <p>Latest rows: {byName.get(project.id)?.rows ?? 0}</p>
            <p>Latest columns: {byName.get(project.id)?.columns ?? 0}</p>
            <Link className="text-link" to="/data-explorer">
              Open in Data Explorer
            </Link>
          </article>
        ))}
      </section>
    </ModulePage>
  )
}
