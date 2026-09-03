import ModulePage from '../components/ModulePage'
import { PROJECTS } from '../services/projects'

export default function ProjectsPage() {
  return (
    <ModulePage
      title="Projects"
      purpose="Move from guided tasks to open-ended analysis and recommendation writing."
      status="planned"
      nextActionLabel="Explore Project Datasets"
      nextActionTo="/datasets"
    >
      <section className="card">
        <h2>Project Tracks</h2>
        <ul className="simple-list">
          {PROJECTS.map((project) => (
            <li key={project.id}>{project.title}</li>
          ))}
        </ul>
      </section>
    </ModulePage>
  )
}
