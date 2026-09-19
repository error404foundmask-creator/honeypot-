# Architecture

Rust accepts bounded TCP connections on four safe decoys and emits one structured event per connection. FastAPI validates and enriches events, applies transparent heuristic scoring, persists telemetry, creates alerts, and broadcasts JSON over WebSockets. React consumes REST/WebSocket data. Components communicate only through the backend event API.

All services are detection-only and should run on an isolated network.
