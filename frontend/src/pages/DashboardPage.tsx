import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import ModulePage from '../components/ModulePage'
import { fetchRecentDatasets } from '../services/datasets'
import { getLastDatasetTitle, getLastModule } from '../services/studentState'

function humanizeModule(pathname: string | null): string {
  if (!pathname) {
    return 'No activity yet'
  }
  const cleaned = pathname.replace(/^\//, '')
  if (!cleaned) {
    return 'Home'
  }
  return cleaned
    .split('-')
    .map((token) => token.charAt(0).toUpperCase() + token.slice(1))
    .join(' ')
}

export default function DashboardPage() {
  const lastDataset = getLastDatasetTitle()
  const lastModule = humanizeModule(getLastModule())
  const recentDatasetsQuery = useQuery({
    queryKey: ['recent-datasets', 'dashboard'],
    queryFn: () => fetchRecentDatasets(6),
  })

  return (
    <ModulePage
      title="Dashboard"
      purpose="Continue your real learning flow using current dataset and recent activity state."
      status="in-progress"
      nextActionLabel="Continue in Data Explorer"
      nextActionTo="/data-explorer"
    >
      <section className="card dashboard-grid">
        <div>
          <h2>Continue Learning</h2>
          <p>Current dataset: {lastDataset}</p>
          <p>Current learning activity: {lastModule}</p>
          <p>Progress tracking backend is scheduled in Phase 11. Current state combines local session + persisted datasets.</p>
          <div className="dashboard-recent">
            <h3>Recent datasets</h3>
            {recentDatasetsQuery.isLoading && <p>Loading recent dataset history...</p>}
            {recentDatasetsQuery.isError && <p>Could not load recent datasets right now.</p>}
            {!recentDatasetsQuery.isLoading && !recentDatasetsQuery.isError && recentDatasetsQuery.data?.length === 0 && (
              <p>No generated datasets yet. Create your first one in Data Explorer.</p>
            )}
            {recentDatasetsQuery.data && recentDatasetsQuery.data.length > 0 && (
              <ul className="simple-list">
                {recentDatasetsQuery.data.map((item) => (
                  <li key={item.dataset_id}>
                    {item.dataset_name} | {item.rows_count} rows | {item.columns_count} cols | {item.difficulty}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
        <div className="quick-actions">
          <Link className="button-link" to="/data-explorer">
            Explore Dataset
          </Link>
          <Link className="button-link secondary" to="/visualization-lab">
            Create Visualization
          </Link>
          <Link className="button-link secondary" to="/practice">
            Practice Questions
          </Link>
          <Link className="button-link secondary" to="/challenges">
            Start Challenge
          </Link>
        </div>
      </section>
    </ModulePage>
  )
}
