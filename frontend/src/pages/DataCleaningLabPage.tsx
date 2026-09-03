import ModulePage from '../components/ModulePage'

export default function DataCleaningLabPage() {
  return (
    <ModulePage
      title="Data Cleaning Lab"
      purpose="Learn missing values, duplicates, outliers, and transformations with reversible operations."
      status="planned"
      nextActionLabel="Use Current Dataset in Data Explorer"
      nextActionTo="/data-explorer"
    >
      <section className="card">
        <p>
          This lab will be implemented in Phase 4 with original vs cleaned snapshots, action history, and undo support.
        </p>
      </section>
    </ModulePage>
  )
}
