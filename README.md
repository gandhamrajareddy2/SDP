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
