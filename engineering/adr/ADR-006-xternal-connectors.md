# ADR-006

## Title

External Connectors

## Decision

Connectors are responsible only for communicating with external systems.

Connectors authenticate, invoke external APIs, map requests and responses, and return structured output.

Connectors must never contain business logic or AI reasoning.

## Why

- Isolates external dependencies.
- Makes external systems easy to replace.
- Keeps business logic independent of APIs.

## Trade-offs

- Adds one abstraction layer between tools and external systems.