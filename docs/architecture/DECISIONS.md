# Architecture decisions

This is the initial decision register. Significant decisions should be expanded into dated ADRs as the implementation develops.

## ADR-0001 — Modular monolith

**Status:** Accepted

Keep the first release in a modular monolith. This minimizes operational complexity for a private playtesting POC while preserving explicit domain boundaries.

## ADR-0002 — Server-authoritative game state

**Status:** Accepted

The server validates all gameplay commands and produces role-specific views. Client-side state is presentation state only. In particular, hidden Mr X location data must never be sent to detective clients.

## ADR-0003 — Pure game engine

**Status:** Accepted; implementation deferred to Phase 4

The game engine will be framework-independent TypeScript with deterministic transitions. It will not import React, Fastify, Socket.IO or Drizzle.

## ADR-0004 — Defer distributed infrastructure

**Status:** Accepted

Do not introduce Redis or distributed room ownership for the initial POC. Revisit only when measured capacity or availability requirements justify it.

## ADR-0005 — React + Vite frontend

**Status:** Accepted

Use React + Vite. The older Next.js recommendation in the original context pack is superseded by the approved consolidated plan.
