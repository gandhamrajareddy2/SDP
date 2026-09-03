# DataScience Lab Transformation TODO

Status: In progress
Approach: Incremental refactor; preserve working features while migrating to modular architecture.

## Product Objective
Transform current app into a professional, university-level interactive data science learning platform based on:
Learn -> Explore -> Clean -> Visualize -> Analyze -> Interpret -> Practice -> Apply -> Reflect.

## Phase Plan

### Phase 1: Application Shell + Routing + Design System
- [x] Create route-based architecture with lazy-loaded pages.
- [x] Build responsive app shell (sidebar, top header, module indicator, mobile nav, breadcrumbs).
- [x] Introduce frontend folder architecture: pages, components, features, services, hooks, types, utils.
- [x] Keep existing Data Explorer + Generator functionality intact by wrapping existing implementation in new routing.
- [x] Add global design tokens and base UI primitives (cards, badges, buttons, status states).
- [x] Add baseline dark mode support via theme tokens.
- [x] Validate frontend build and existing flows.

### Phase 2: Dashboard + Dataset Hub
- [x] Build Dashboard with real state (selected dataset, last activity, progress signals from actual saved state).
- [x] Build Dataset Hub with cards and filter/sort/search.
- [x] Reuse backend project/template metadata where possible.
- [x] Add quick actions wired to real routes.

### Phase 3: Data Explorer + Backend Pagination/Filtering
- [x] Add backend pagination for dataset rows.
- [x] Add backend filtering and sorting parameters.
- [x] Update Data Explorer tabs: Overview, Preview, Columns, Statistics, Missing, Duplicates, Outliers.
- [x] Frontend row table with server-side pagination/filter/search.

### Phase 4: Data Cleaning Lab
- [x] Add non-destructive cleaning workflows with action history and undo.
- [x] Maintain original dataset and cleaned version snapshots.
- [x] Add educational explanation per operation.

### Phase 5: Visualization Lab 2.0
- [x] Expand chart catalog with analysis-purpose-first mapping.
- [x] Implement chart configuration controls and invalid-combination handling.
- [x] Keep performance constraints and responsive behavior.

### Phase 6: Chart Recommendation Engine
- [x] Build “Help Me Choose a Chart” guided recommender based on objective + variable types.
- [x] Include reason, required variables, what to look for, common mistakes.

### Phase 7: Statistics Lab
- [x] Add statistics definitions + formulas + interpretation with progressive disclosure.
- [x] Link directly to selected dataset and selected columns.

### Phase 8: Insights Lab + Interpretation Checker 2.0
- [x] Expand interpretation evaluation dimensions and structured feedback.
- [x] Preserve reasoning-first guidance (no answer dumping).

### Phase 9: Practice + Challenges
- [x] Add question engine and challenge flow with rubric-based scoring.
- [x] Track actual student progress events.

### Phase 10: Projects + Learning Path
- [x] Build guided and open-ended mini projects.
- [x] Visual learning path with configurable progression states.

### Phase 11: Saved Sessions + Dataset Versioning
- [x] Add save/resume/rename/duplicate/delete sessions.
- [x] Add dataset version records and compare view.

### Phase 12: Export
- [x] Add chart PNG export.
- [x] Add dataset CSV export enhancements.
- [x] Add PDF analysis report export.

### Phase 13: Accessibility + Responsive + Performance
- [ ] Accessibility audit and fixes (keyboard, ARIA, contrast, focus). Baseline improvements applied; full audit pending.
- [x] Mobile/tablet layout optimization.
- [x] Performance tuning (lazy routes, query caching, memoization, render optimization).

### Phase 14: Tests + Production Verification
- [x] Add backend automated tests (API, generator, validation, pagination/filtering, sessions).
- [ ] Add frontend tests for route navigation and key workflows.
- [ ] Validate Render production behavior end to end.

## Reuse Matrix (Keep and Integrate)
- Existing dataset generation API and controls from frontend App component.
- Existing visualization subset (scatter, line, bar, histogram).
- Existing interpretation and keyword/phrase feedback logic.
- Existing insights (DIKW), merits/demerits, and learning content sections.
- Existing backend routes for generation, summary, rows, download, delete.

## Refactor Targets
- Split large frontend app into route modules and reusable feature components.
- Centralize shared types, constants, and project metadata.
- Move API calls into typed service layer.
- Replace ad-hoc local state islands with structured page-level state + persistent session model.

## New Components/Pages Required
- App shell: sidebar, header, breadcrumbs, module status.
- Pages: Dashboard, Learn, Datasets, Data Explorer, Data Cleaning Lab, Visualization Lab, Statistics Lab, Insights Lab, Practice, Challenges, Projects, Learning Path, Resources, Progress, Landing.
- Shared UI: Card, SectionHeader, EmptyState, ErrorState, LoadingState, Badge, Tabs, DataTable.
- Services: dataset, explorer, sessions, stats, challenges, progress.

## Backend API Changes
- Add paginated rows endpoint with filtering/sorting.
- Add session CRUD endpoints.
- Add dataset version listing/comparison endpoints.
- Add readiness endpoint and improved health.
- Add request-id middleware + structured logging.
- Add validation extensions for generator advanced controls.
- Add optional rate-limiting for expensive endpoints.

## Database Schema Changes (SQLite now, PostgreSQL-ready later)
- Add dataset_versions table linked to dataset_id.
- Add sessions table and session_snapshots/config payloads.
- Add progress_events table for verifiable learning progress.
- Add indexes for dataset_id, created_at, session_id.
- Keep migrations additive and backward compatible.

## Dependency Plan (Only when required)
- Frontend now: react-router-dom already present.
- Potential frontend additions:
  - chart.js + react-chartjs-2 OR nivo for advanced charts not natively supported by Recharts.
  - html-to-image for PNG export.
  - jspdf (or pdf-lib) for PDF report generation.
- Backend potential additions:
  - slowapi for rate limiting.
  - pytest + httpx for tests.
  - structlog for structured logging.

## Risks to Existing Functionality and Mitigations
- Risk: Route refactor breaks existing Data Explorer/generator.
  - Mitigation: Keep current App implementation as wrapped module route during migration.
- Risk: New state model conflicts with current local state.
  - Mitigation: Introduce bridge layer and migrate feature-by-feature.
- Risk: Large chart additions hurt performance.
  - Mitigation: Lazy load chart-heavy modules and cap rendered points.
- Risk: Misleading fake progress.
  - Mitigation: Show only persisted/derived metrics; otherwise mark as not started.
- Risk: Deploy regressions on Render.
  - Mitigation: Preserve existing build commands and validate SPA fallback before rollout.

## Current Sprint Goal
- Close remaining verification gaps: frontend automated tests and Render production end-to-end validation.
