import ModulePage from '../components/ModulePage'

export default function LearningPathPage() {
  const levels = [
    'Level 1: Data Literacy',
    'Level 2: Data Exploration',
    'Level 3: Data Cleaning',
    'Level 4: Visualization',
    'Level 5: Statistics',
    'Level 6: Interpretation',
    'Level 7: Decision Making',
    'Level 8: Applied Data Science',
  ]

  return (
    <ModulePage
      title="Learning Path"
      purpose="Track progression from fundamentals to applied data science practice."
      status="planned"
      nextActionLabel="Begin with Learn Module"
      nextActionTo="/learn"
    >
      <section className="card">
        <ul className="simple-list">
          {levels.map((level) => (
            <li key={level}>{level}</li>
          ))}
        </ul>
      </section>
    </ModulePage>
  )
}
