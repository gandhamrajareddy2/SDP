import ModulePage from '../components/ModulePage'

export default function StatisticsLabPage() {
  return (
    <ModulePage
      title="Statistics Lab"
      purpose="Understand descriptive metrics, interpretation, and practical use cases."
      status="planned"
      nextActionLabel="Analyze Current Dataset"
      nextActionTo="/data-explorer"
    >
      <section className="card">
        <p>Phase 7 will add progressive disclosure for metrics, formulas, interpretation, and examples.</p>
      </section>
    </ModulePage>
  )
}
