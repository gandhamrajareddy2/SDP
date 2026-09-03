import ModulePage from '../components/ModulePage'

const modules = [
  '01 Data Literacy',
  '02 Understanding Datasets',
  '03 Data Types',
  '04 Data Cleaning',
  '05 Missing Values',
  '06 Outliers',
  '07 Descriptive Statistics',
  '08 Data Visualization',
  '09 Correlation',
  '10 Interpretation',
  '11 Data-to-Decision',
  '12 Introduction to Predictive Analytics',
]

export default function LearnPage() {
  return (
    <ModulePage
      title="Learn"
      purpose="Connect concepts to practical labs using structured modules."
      status="in-progress"
      nextActionLabel="Open Data Explorer Activity"
      nextActionTo="/data-explorer"
    >
      <section className="card">
        <h2>Learning Modules</h2>
        <ul className="simple-list">
          {modules.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
        <p>Each module will include concept, example, interactive activity, reflection, practice, and key takeaway.</p>
      </section>
    </ModulePage>
  )
}
