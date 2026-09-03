import { Link } from 'react-router-dom'

export default function LandingPage() {
  return (
    <section className="module-page landing-page">
      <header className="card hero-card">
        <p className="eyebrow">DataScience Lab</p>
        <h1>Learn Data Science by working with data.</h1>
        <p>
          Explore datasets, clean data, build visualizations, interpret patterns, and develop evidence-based insights
          through hands-on practice.
        </p>
        <div className="hero-actions">
          <Link className="button-link" to="/learn">
            Start Learning
          </Link>
          <Link className="button-link secondary" to="/datasets">
            Explore Datasets
          </Link>
        </div>
      </header>

      <section className="card capability-grid">
        <h2>How You Learn Here</h2>
        <div className="pillars">
          <span>Explore Data</span>
          <span>Clean Data</span>
          <span>Visualize</span>
          <span>Analyze</span>
          <span>Interpret</span>
          <span>Apply</span>
        </div>
      </section>
    </section>
  )
}
