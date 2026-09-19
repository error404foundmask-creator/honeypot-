# Database

SQLite is the default development store; SQLAlchemy keeps the model PostgreSQL-compatible. Events and alerts are indexed by identifiers, timestamp, source IP, service, event type, severity, and risk score. A future migration tool should be used for production schema changes.
