import ModulePage from '../components/ModulePage'

export default function PracticePage() {
  return (
    <ModulePage
      title="Practice"
      purpose="Build retention with guided and adaptive data science practice questions."
      status="planned"
      nextActionLabel="Continue Practical Analysis"
      nextActionTo="/data-explorer"
    >
      <section className="card">
        <p>Practice engine with real progress tracking is scheduled in Phase 9.</p>
      </section>
    </ModulePage>
  )
}
