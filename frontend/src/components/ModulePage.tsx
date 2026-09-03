import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'

type ModulePageProps = {
  title: string
  purpose: string
  status: 'available' | 'in-progress' | 'planned'
  nextActionLabel?: string
  nextActionTo?: string
  children?: ReactNode
}

export default function ModulePage({
  title,
  purpose,
  status,
  nextActionLabel,
  nextActionTo,
  children,
}: ModulePageProps) {
  return (
    <section className="module-page">
      <header className="module-header card">
        <div>
          <p className="eyebrow">DataScience Lab Module</p>
          <h1>{title}</h1>
          <p className="module-purpose">{purpose}</p>
        </div>
        <span className={`status-badge ${status}`}>{status.replace('-', ' ')}</span>
      </header>

      {nextActionLabel && nextActionTo && (
        <div className="card module-cta">
          <p>This module is connected to the platform roadmap and will progressively receive full functionality.</p>
          <Link className="button-link" to={nextActionTo}>
            {nextActionLabel}
          </Link>
        </div>
      )}

      {children}
    </section>
  )
}
