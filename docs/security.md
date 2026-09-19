# Security

No command execution, authentication backend, credential collection, filesystem browsing, scanning, exploitation, retaliation, or external TI dependency is implemented. Inputs have Pydantic bounds, sockets have timeouts, the Rust sensor uses bounded reads, and secrets are environment variables. Deploy behind TLS/authentication and a reverse proxy for production; the sample CORS policy is intentionally suitable only for a local lab.

The included mock TI record is synthetic. Scores are heuristics for education and must not be treated as an incident verdict.
