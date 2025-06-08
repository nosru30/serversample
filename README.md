# serversample

## Environment variables

- `DATABASE_URL`: connection string for the database. Tests use a SQLite file if
  not provided.
- `CORS_ALLOW_ORIGINS`: comma-separated list of origins allowed by CORS.
  Defaults to `*` to permit any origin.

## API endpoints

The application exposes `/tasks` for CRUD operations on tasks persisted in the
configured database. Tasks may include nested `sub_tasks`, which are stored as
rows referencing their parent task. Database schema migrations are managed with
Alembic and applied automatically at startup.
