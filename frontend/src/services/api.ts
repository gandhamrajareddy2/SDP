const configuredApiBase = (import.meta.env.VITE_API_BASE_URL as string | undefined)?.trim()
const inferredApiBase =
  window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000/api'
    : '/api'

export const API_BASE = (configuredApiBase && configuredApiBase.length > 0 ? configuredApiBase : inferredApiBase).replace(
  /\/$/,
  '',
)
