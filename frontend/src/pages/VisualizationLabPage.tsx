import ModulePage from '../components/ModulePage'

export default function VisualizationLabPage() {
  return (
    <ModulePage
      title="Visualization Lab"
      purpose="Build analysis-purpose visualizations with valid chart and variable combinations."
      status="in-progress"
      nextActionLabel="Use Existing Visualization Builder"
      nextActionTo="/data-explorer"
    >
      <section className="card">
        <p>
          The current chart builder remains available and working. Advanced chart families and recommendation engine are
          scheduled in Phase 5 and Phase 6.
        </p>
      </section>
    </ModulePage>
  )
}
