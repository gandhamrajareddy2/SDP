# DataScience Lab Backend

FastAPI backend for DataScience Lab.

## Environment Variables

Set these at deployment level (for example, in Render service environment settings):

- `CORS_ALLOW_ORIGINS`: comma-separated allowed frontend origins
- `CORS_ALLOW_CREDENTIALS`: `true` or `false`

Example:

```env
CORS_ALLOW_ORIGINS=https://your-frontend.onrender.com,http://localhost:5173
CORS_ALLOW_CREDENTIALS=false
```

## Run

```powershell
C:/Python314/python.exe -m pip install -r requirements.txt
C:/Python314/python.exe -m uvicorn app.main:app --reload --port 8000
```

## Slice 1 Features

- Student Performance dataset generator
- Dataset metadata + preview API
- Missing value summary and data types
- CSV download and dataset reset
- SQLite dataset registry

## Render Start Command

Use this start command so Render injects its dynamic port:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
