# Task Manager API

A simple REST API for managing tasks. Built with Flask + Gunicorn.
Designed as a learning app for writing a **Helm chart**.

---

## Running Locally

```bash
pip install -r requirements.txt
APP_ENV=development python app.py
```

## Running with Docker

```bash
docker build -t task-manager:1.0.0 .
docker run -p 5000:5000 \
  -e APP_ENV=production \
  -e APP_VERSION=1.0.0 \
  task-manager:1.0.0
```

---

## API Endpoints

| Method | Path            | Description              |
|--------|-----------------|--------------------------|
| GET    | /health         | Liveness probe           |
| GET    | /ready          | Readiness probe          |
| GET    | /info           | App version & env info   |
| GET    | /tasks          | List all tasks           |
| POST   | /tasks          | Create a task            |
| GET    | /tasks/:id      | Get a single task        |
| PUT    | /tasks/:id      | Update a task            |
| DELETE | /tasks/:id      | Delete a task            |

### Example: Create a task
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Helm", "priority": "high"}'
```

### Example: List tasks by status
```bash
curl http://localhost:5000/tasks?status=pending
```

---

## Environment Variables

| Variable      | Default        | Description                        |
|---------------|----------------|------------------------------------|
| PORT          | 5000           | Port the server listens on         |
| APP_ENV       | development    | Environment label (dev/staging/prod)|
| APP_VERSION   | 1.0.0          | Version string shown in /info      |

---

## Helm Chart Checklist (what to build)

When writing your Helm chart for this app, make sure to cover:

- [ ] `Deployment` — image, replicas, env vars from values
- [ ] `Service` — ClusterIP on port 5000
- [ ] `ConfigMap` — APP_ENV, APP_VERSION as config
- [ ] `Ingress` — optional, toggled via `ingress.enabled`
- [ ] `HPA` — horizontal pod autoscaler (bonus)
- [ ] Liveness probe → `GET /health`
- [ ] Readiness probe → `GET /ready`
- [ ] Resource limits (cpu/memory) via values
- [ ] Multi-env values files: `values-dev.yaml`, `values-prod.yaml`
