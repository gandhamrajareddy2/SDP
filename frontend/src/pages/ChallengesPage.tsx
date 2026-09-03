import ModulePage from '../components/ModulePage'

export default function ChallengesPage() {
  return (
    <ModulePage
      title="Challenges"
      purpose="Solve end-to-end scenario-based analytics tasks with rubric scoring."
      status="planned"
      nextActionLabel="Start with Existing Project Dataset"
      nextActionTo="/data-explorer"
    >
      <section className="card">
        <p>Challenge mode with scoring dimensions will be implemented in Phase 9.</p>
      </section>
    </ModulePage>
  )
}
