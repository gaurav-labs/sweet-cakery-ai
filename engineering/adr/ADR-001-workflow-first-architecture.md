# ADR-001

## Title

Workflow-first architecture

## Status

Accepted

## Decision

The workflow is responsible for orchestrating the complete request.

Workflows may invoke AI through the AI Gateway, execute tools or request human approval.

Tools are deterministic and must never invoke LLMs directly.

The same workflow can be started from the Web UI, Python CLI or REST API.

## Why

- Single business workflow
- No duplicated logic
- Easier testing
- Easier maintenance
- Multiple entry points
