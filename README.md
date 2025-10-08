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

## AArchitecture (short)

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

## TDD‑Workflow (recommended)

**Backend (pytest)**

* First write a unit test in `backend/tests/unit/` → `docker compose run --rm backend pytest -q`.
* Implement minimal code in `backend/` until the test is green.
* Add integration tests in `backend/tests/integration/` that run against the `db` service.

**Frontend (vitest + RTL)**

* Component tests in `frontend/__tests__` → `docker compose run --rm frontend npm run test`

**E2E (Playwright)**

* Start Compose Services (`docker compose up -d`) → Run Playwright scripts in `e2e/`; Edge Simulator replays deterministic event logs.

Example commands:

    ```bash
        # Backend Unit
        docker compose run --rm backend pytest tests/unit
        # Integration
        docker compose up -d db backend
        docker compose run --rm backend pytest tests/integration
        # E2E (lokal)
        docker compose up -d
        npx playwright test e2e
    ```

---

## API (Kurzreferenz)

### POST /api/events

Ingest eines Karten‑Events (Edge benutzt `x-edge-secret` Header zur Authentifizierung).

**Payload**

```json
{
  "card_id": "CARD-1234",
  "reader_id": "desk-1",
  "timestamp": "2025-10-07T08:15:00Z",
  "type": "checkin"
}
```

**Header**: `x-edge-secret: <EDGE_SECRET>`

### GET /api/events

Lists all events (MVP — paging & filtering later)

---

## Edge Simulator — Usage

* **Manual trigger**: `POST /simulate` with `{ card_id, reader_id, type }` sends an event to the backend.
* **Replay Mode**: Provide a file `events.json/csv`; the simulator sends the events deterministically — useful for E2E tests.

---

## Security & Data Protection
* Timestamps are stored in UTC; UI converts to `Europe/Berlin`.
* Minimal PII footprint: only `card_id` and optionally `name` (if explicitly required) are stored.
* Secrets are managed via environment variables. Use Docker Secrets or a vault solution for production.
* Automatic image scans (Trivy / Snyk) in CI recommended.

---

## CI / Quality Gates

Recommended GitHub Actions jobs:

1. `lint` (frontend + backend)
2. `unit-tests` (parallel)
3. `integration-tests` (Docker Compose Services)
4. `e2e-tests` (Playwright)
5. `security-scan` (Trivy/Snyk)

---

## Ordnerstruktur 

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

## Lizenz
MIT © Lazar Iliev

---

## Author
**Lazar Iliev** — Junior Developer  
[LinkedIn](https://www.linkedin.com/in/lazar-iliev-dev) • [Portfolio](https://github.com/lazar-iliev-dev)
