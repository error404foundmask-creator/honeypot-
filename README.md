# Enterprise Honeypot & Deception Security Platform

A defensive, detection-only honeypot platform for authorized isolated labs. It includes safe Rust decoys, a FastAPI analysis API, persistent telemetry, WebSocket streaming, and a React SOC dashboard.

## Safety
Decoys never authenticate users, execute input, access real credentials/files, scan networks, exploit targets, or retaliate. Use only on localhost or explicitly authorized lab networks. Demo mode creates synthetic events through the normal API pipeline.

## Run
```bash
docker compose up --build
```
Open http://localhost:3000. API docs: http://localhost:8000/docs.

For local development, see `python-backend/README.md` and `frontend/README.md`. The Rust sensor posts events to `EVENT_INGEST_URL` and can listen on unprivileged configurable ports.

## Components
- `rust-sensor`: Tokio TCP decoys for SSH, HTTP, FTP, and database-like protocols.
- `python-backend`: validation, heuristic risk scoring, synthetic/local TI, SQLite/PostgreSQL-compatible persistence, REST and WebSockets.
- `frontend`: TypeScript React SOC view with live stream, attack graph, alerts, and demo controls.
- `docs/`: architecture, API, database, security, and viva material.

Risk scoring is an academic heuristic, not a definitive threat classification. No benchmark values are fabricated; use `python-backend/scripts/benchmark.py` against your machine.
