# Time-Recording-System

> **Automated time tracking** — Modern, containerized project demonstrating full-stack and integration capabilities (Next.js, TypeScript, FastAPI, Python Edge Simulator). Developed using a TDD approach, fully executable in Docker.

---

![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![Tests](https://img.shields.io/badge/tests-✔️-blue) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Brief description

This project is a lean, professionally documented showcase of a **time recording/time tracking solution** with card reader integration (simulated here). The goal is to demonstrate end-to-end skills in a single, reproducible repository: frontend (Next.js + TypeScript), backend (FastAPI, Python), edge/device simulator (Python), and a CI-enabled TDD workflow (unit → integration → E2E).

The entire system is designed so that it can be run in Docker without physical hardware and tested in CI.

---

## Highlights 

* Complete end-to-end demo (simulated card reader → backend → live dashboard).
* TDD-driven development with example tests (pytest, vitest, Playwright).
* Saubere, reproduzierbare Dev‑Umgebung via `docker compose up --build`.
* Focus on security (TLS/secrets handling, least privilege Dockerfile pattern) and data protection (minimal personal data stored).

---

## Features (MVP)

* Map event simulation (Check‑in / Check‑out) through Edge Simulator
* REST API `POST /api/events` (Event‑Ingest) and `GET /api/events` (Listing)
* Realtime‑Updates (WebSocket / SSE — optional in MVP per Polling)
* CSV export for reports
* Demo‑UI (Next.js) mit Event‑Timeline & Filter
* Full containerization + example CI pipelines

---

## Tech Stack

* **Frontend:** Next.js, React, TypeScript, React Query / SWR, Vitest, Playwright
* **Backend:** FastAPI, Python, Pydantic, SQLModel/SQLAlchemy (expandable), pytest, httpx
* **Edge Simulator:** FastAPI (smaller HTTP‑Service) or CLI‑Skript (Python)
* **DB:** PostgreSQL (Postgres service in Docker Compose)
* **Container / Orchestration:** Docker, Docker Compose
* **CI:** GitHub Actions (Test, Build, Security Scan)

---

## Architecture (short)

```
[Edge-Sim] --HTTP--> [Backend API (FastAPI)] <-----> [Postgres DB]
                                       |
                                       `--> [Frontend (Next.js) - WebSocket/SSE polling]
```

* **Edge Simulator** simulates card readers and sends signed events to the backend.
* **Backend** validates/normalizes events, stores them, and distributes live updates to clients.
* **Frontend** displays dashboard, live timeline, user management, and exports.

---

## Quickstart — local (Docker)

1. Requirements: Docker & Docker Compose installed.
2. Repository clonen:

    ```bash
        git clone [text](https://github.com/lazar-iliev-dev/Time-Recording-System.git)
        cd Time-Recording-System
        cp .env.example .env   # anpassen falls nötig
    ```

3. Build & Start (development):

    ```bash
        docker compose up --build
    ```

4. Services:

* Frontend: [http://localhost:3000](http://localhost:3000)
* Backend API: [http://localhost:8000](http://localhost:8000) (OpenAPI: [http://localhost:8000/docs](http://localhost:8000/docs))
* Edge Simulator (manuell): [http://localhost:9000](http://localhost:9000) (POST /simulate)

5. Stop & clean:

    ```bash
        docker compose down -v
    ```

---

## Environment

Copy `.env.example` to `.env` and adjust values.

Important variables:

* `EDGE_SECRET` — Shared secret für Edge → Backend (test mode only)
* `DATABASE_URL` —Postgres connection string
* `NEXT_PUBLIC_API_URL` — URL for the frontend

---

## TDD Workflow (Recommended)

### Backend (pytest)

* Write a unit test in `backend/tests/unit/` → `docker compose run --rm backend pytest -q`
* Implement minimal code in `backend/` until the test passes.
* Add integration tests in `backend/tests/integration/` that run against the `db` service.

### Frontend (Vitest + React Testing Library)

* Component tests in `frontend/__tests__` → `docker compose run --rm frontend npm run test`

### End-to-End (Playwright)

End-to-end tests ensure all services (frontend ↔ backend ↔ database ↔ edge simulator) work together correctly.

Run locally:

```bash
# start all containers
docker compose up -d db backend frontend edge-sim

# execute Playwright tests
cd e2e
npx playwright install --with-deps
npx playwright test
```

List all available tests:

```bash
npx playwright test --list
```

---

## (Optional) Seed Demo Data

Quickly populate your local database with demo events for testing:

```bash
docker compose run --rm backend python scripts/seed.py
```

Verify the data was inserted:

```bash
docker compose exec db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT * FROM event;"
```

Or via API:

```bash
curl http://localhost:8000/api/events | jq .
```

---

## Continuous Integration (GitHub Actions)

All tests run automatically in CI using the workflow:

`.github/workflows/ci.yml`

It includes the following jobs:

1. **Lint** – frontend & backend
2. **Unit tests** – Python (pytest) + Next.js (Vitest)
3. **Integration tests** – backend ↔ database
4. **E2E tests** – Playwright (Dockerized)
5. **Security scan** – Trivy / Snyk (optional)

To simulate locally:

```bash
# run backend and frontend tests
docker compose run --rm backend pytest -q
cd frontend && npm run test

# run full E2E suite
cd ../e2e && npx playwright test
```

If you use [`act`](https://github.com/nektos/act):

```bash
act -j ci
```

This emulates the GitHub Actions pipeline locally.

---

## Project Structure

```
.
├── backend/         # FastAPI app, tests, Dockerfile
├── frontend/        # Next.js app, tests, Dockerfile
├── edge/            # Edge simulator, Dockerfile
├── docker-compose.yml
├── .github/workflows/
├── e2e/             # Playwright tests + fixtures
├── docs/            # Architecture diagrams, GDPR notes
└── README.md
```

---

## License
MIT © Lazar Iliev

---

## Author / Maintainer
**Lazar Iliev** — Junior Developer  
[LinkedIn](https://www.linkedin.com/in/lazar-iliev-dev) • [Portfolio](https://github.com/lazar-iliev-dev)
