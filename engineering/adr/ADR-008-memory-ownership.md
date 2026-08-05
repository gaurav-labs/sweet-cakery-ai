# ADR-008

## Title

Memory Ownership

## Decision

The platform separates transient workflow memory, knowledge memory and application storage.

- Workflow Memory stores transient workflow state and is owned by the workflow.
- Knowledge Memory stores indexed knowledge derived from external systems.
- Application Storage stores data owned by the AI platform.
- Business entities remain in their original systems and are never duplicated as the source of truth.

## Why

- Clear ownership of data.
- Avoids duplicate business data.
- Keeps workflows independent of storage implementation.
- Supports RAG without replacing operational databases.

## Trade-offs

- Knowledge indexes must be refreshed when source data changes.
- The platform depends on external systems for business data.