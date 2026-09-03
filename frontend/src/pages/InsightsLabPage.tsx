import ModulePage from '../components/ModulePage'

export default function InsightsLabPage() {
  return (
    <ModulePage
      title="Insights Lab"
      purpose="Practice DIKW reasoning and convert observations into decisions."
      status="in-progress"
      nextActionLabel="Open Current Insights Flow"
      nextActionTo="/data-explorer"
    >
      <section className="card">
        <p>
          Existing DIKW and interpretation feedback are preserved in the current explorer flow and will be expanded in
          Phase 8.
        </p>
      </section>
    </ModulePage>
  )
}
