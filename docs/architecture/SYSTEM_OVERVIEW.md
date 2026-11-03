# System overview

## Current foundation

```text
React + Vite
    |
    | HTTP (Socket.IO boundary added in a later batch)
    v
Fastify API
    |
    +-- validated environment
    |
    +-- database package
            |
            +-- Drizzle ORM
            |
            +-- PostgreSQL 17
```

The application is a modular monolith. PostgreSQL is the durable data store. The API owns application lifecycle and exposes liveness and readiness separately.

## Dependency direction

- `apps/web` depends on shared contracts.
- `apps/server` depends on shared contracts and the database package.
- `packages/database` owns database connectivity, Drizzle schema and migrations.
- The future game engine remains a pure domain package and must not depend on Fastify, Socket.IO, React or PostgreSQL.

## Health semantics

`/health/live` indicates that the HTTP process is responsive. It must not fail solely because PostgreSQL is unavailable.

`/health/ready` checks the database dependency and returns 503 when it cannot be reached.

## Deferred

Socket.IO room transport, game domain tables, room repositories, game engine, Redis, distributed coordination and custom variants are deliberately outside this infrastructure batch.
