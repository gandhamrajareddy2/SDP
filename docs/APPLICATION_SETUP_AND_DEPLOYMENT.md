# DataScience Lab: Current Setup and Deployment Guide

This document is tailored to the current repository setup and deployment flow.

## 1. Application Architecture

This project runs as two services:

- Backend: FastAPI on port 8000.
- Frontend: React + Vite build served by NGINX on port 80 inside container.

Traffic model in Kubernetes:

1. Browser requests frontend route `/`.
2. Frontend static files are served by NGINX.
3. API requests to `/api/*` are routed to backend service.
4. Backend responds from FastAPI endpoints.

## 2. File-by-File Reference (Current Repo)

- [backend/Dockerfile](backend/Dockerfile): Backend container build and runtime command.
- [backend/.dockerignore](backend/.dockerignore): Backend build context exclusions.
- [frontend/Dockerfile](frontend/Dockerfile): Frontend multi-stage build (Node build + NGINX runtime).
- [frontend/nginx.conf](frontend/nginx.conf): SPA routing and `/api` reverse proxy to backend service inside Kubernetes.
- [frontend/.dockerignore](frontend/.dockerignore): Frontend build context exclusions.
- [docker-compose.yml](docker-compose.yml): Local two-container stack on ports 5173 and 8000.
- [k8s/namespace.yaml](k8s/namespace.yaml): Namespace `data-visualization-tool`.
- [k8s/backend.yaml](k8s/backend.yaml): Backend Deployment + Service.
- [k8s/frontend.yaml](k8s/frontend.yaml): Frontend Deployment + Service.
- [k8s/ingress.yaml](k8s/ingress.yaml): Host-based ingress routing.
- [k8s/kustomization.yaml](k8s/kustomization.yaml): Aggregates Kubernetes manifests.
- [.github/workflows/ci-cd-k8s.yml](.github/workflows/ci-cd-k8s.yml): CI/CD workflow for test, image build/push, and Kubernetes rollout.

## 3. Local Docker Compose Workflow

Run from repository root:

```powershell
docker compose up --build
```

Access:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api
- Backend docs: http://localhost:8000/docs

Stop:

```powershell
docker compose down
```

## 4. Local Kubernetes Workflow (Docker Desktop)

### 4.1 Prerequisites

1. Docker Desktop Kubernetes is enabled and running.
2. kubectl context is `docker-desktop`.
3. ingress-nginx is installed.

### 4.2 Deploy

```powershell
kubectl apply -k k8s
```

Check status:

```powershell
kubectl -n data-visualization-tool get deploy,pods,svc,ingress
```

### 4.3 Current Ingress Hosts

Configured hosts in [k8s/ingress.yaml](k8s/ingress.yaml):

- `datascience-lab.local`
- `datascience-lab.127.0.0.1.nip.io`

Recommended local URL (works without editing hosts file):

- http://datascience-lab.127.0.0.1.nip.io/

API check:

- http://datascience-lab.127.0.0.1.nip.io/api/health

If using `datascience-lab.local`, add Windows hosts entry:

```text
127.0.0.1 datascience-lab.local
```

## 5. Why localhost Should Not Be Used for Multi-App Routing

For multiple local apps behind one ingress controller, host-based routing is safer than catch-all localhost routing.

Current setup intentionally avoids binding app routes directly to `localhost` ingress host. This prevents collisions when other applications are added.

## 6. GitHub Actions CI/CD (Current Workflow)

Workflow file: [.github/workflows/ci-cd-k8s.yml](.github/workflows/ci-cd-k8s.yml)

Jobs:

1. `test-and-build-app`
2. `build-and-push-images`
3. `deploy-to-kubernetes`

### 6.1 What each job does

`test-and-build-app`:

- Installs backend dependencies.
- Runs backend tests (`pytest backend/tests -q`).
- Builds frontend (`npm ci && npm run build`).

`build-and-push-images`:

- Logs into Docker Hub.
- Builds and pushes backend image tags:
  - `<dockerhub_user>/datascience-lab-backend:${github.sha}`
  - `<dockerhub_user>/datascience-lab-backend:latest`
- Builds and pushes frontend image tags:
  - `<dockerhub_user>/datascience-lab-frontend:${github.sha}`
  - `<dockerhub_user>/datascience-lab-frontend:latest`

`deploy-to-kubernetes`:

- Decodes kubeconfig from secret.
- Applies `k8s` manifests.
- Updates deployment images to SHA-tagged images.
- Waits for rollout status.

### 6.2 Required GitHub secrets

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `KUBE_CONFIG_B64`

### 6.3 Important Local Cluster Limitation

GitHub-hosted runners cannot directly deploy to your local Docker Desktop Kubernetes.

Use one of these:

1. Self-hosted runner on the same machine as Docker Desktop.
2. Remote cluster (AKS/EKS/GKE) with reachable API endpoint.

## 7. Troubleshooting

### 7.1 DNS_PROBE_FINISHED_NXDOMAIN

Cause:

- `datascience-lab.local` is not resolvable by system DNS.

Fix options:

1. Use `http://datascience-lab.127.0.0.1.nip.io/`.
2. Add hosts entry for `datascience-lab.local`.

### 7.2 404 on http://localhost/

Expected when host-based ingress is used and `localhost` host rule is intentionally not configured.

### 7.3 Verify ingress routing from terminal

```powershell
Invoke-WebRequest -UseBasicParsing -Headers @{ Host = 'datascience-lab.local' } http://localhost/api/health
```

### 7.4 Verify deployment health

```powershell
kubectl -n data-visualization-tool get deploy,pods,svc,ingress
kubectl -n data-visualization-tool logs deploy/datascience-lab-backend
kubectl -n data-visualization-tool logs deploy/datascience-lab-frontend
```

## 8. Recommended Day-to-Day Commands

Deploy latest manifests:

```powershell
kubectl apply -k k8s
```

Check rollout quickly:

```powershell
kubectl -n data-visualization-tool rollout status deploy/datascience-lab-backend
kubectl -n data-visualization-tool rollout status deploy/datascience-lab-frontend
```

Delete app resources:

```powershell
kubectl delete -k k8s
```
