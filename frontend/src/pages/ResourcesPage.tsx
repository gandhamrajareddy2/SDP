import ModulePage from '../components/ModulePage'

export default function ResourcesPage() {
  return (
    <ModulePage
      title="Resources"
      purpose="Provide references, reading support, and practical guidance for lab activities."
      status="planned"
      nextActionLabel="Continue with Learn"
      nextActionTo="/learn"
    >
      <section className="card">
        <p>Resource packs and reference links will be structured in Phase 10 as metadata-driven content.</p>
      </section>
    </ModulePage>
  )
}
