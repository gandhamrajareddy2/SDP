import ModulePage from '../components/ModulePage'
import { getLastDatasetTitle, getLastModule } from '../services/studentState'

export default function ProgressPage() {
  const lastDataset = getLastDatasetTitle()
  const lastModule = getLastModule() ?? 'No recorded module yet'

  return (
    <ModulePage
      title="Progress"
      purpose="Track verifiable learning activity and performance signals from saved work."
      status="in-progress"
      nextActionLabel="Continue Learning"
      nextActionTo="/dashboard"
    >
      <section className="card">
        <p>Last dataset used: {lastDataset}</p>
        <p>Last module visited: {lastModule}</p>
        <p>Backend persistence for full progress analytics is planned in Phase 11.</p>
      </section>
    </ModulePage>
  )
}
