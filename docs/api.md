# API

- `GET /api/health`
- `GET /api/events?limit=50`
- `POST /api/events` with the documented EventIn schema
- `GET /api/events/{event_id}`
- `GET /api/statistics`
- `GET /api/alerts`
- `POST /api/demo/{ssh|http|ftp|database}`
- `WS /ws/events`

The demo endpoints are synthetic and use the same processing path as sensor events.
