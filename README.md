# DataScience Lab Monorepo

This repository is a monorepo with separate frontend and backend applications.

## Structure

- frontend: React + TypeScript + Vite app
- backend: FastAPI app

## Local Development

### Backend

```powershell
cd backend
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 8000
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

## Render Deployment (Monorepo)

Use the root [render.yaml](render.yaml) blueprint to deploy both services from one repository.

## One-Roof Single Service Option

If you want one backend service to host both API and frontend from the same domain:

1. Build frontend first so [frontend/dist](frontend/dist) exists.
2. Start backend from repo root using module path.

```bash
pip install -r requirements.txt
uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

Notes:

- Root `requirements.txt` forwards to [backend/requirements.txt](backend/requirements.txt).
- Backend serves frontend files automatically when `frontend/dist` exists.

### Backend service

- rootDir: backend
- buildCommand: pip install -r requirements.txt
- startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT

### Frontend service

- rootDir: frontend
- buildCommand: npm ci && npm run build
- staticPublishPath: dist
- env: VITE_API_BASE_URL points to backend /api URL

## Environment Variables

### Backend

- CORS_ALLOW_ORIGINS
- CORS_ALLOW_CREDENTIALS

### Frontend

- VITE_API_BASE_URL
