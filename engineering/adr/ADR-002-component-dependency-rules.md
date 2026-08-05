## Title

Component Dependency Rules

## Decision

The platform follows a layered architecture with strict dependency rules.

Entry Point
    ↓
Workflow
    ↓
Agent
    ↓
Tool
    ↓
Connector
    ↓
External System


Shared services:

- AI Gateway
- Memory
- Security
- Configuration
- Observability
- Storage

The following rules apply:

- Workflows orchestrate the execution.
- Agents perform reasoning and may invoke the AI Gateway.
- Tools execute deterministic tasks and never invoke LLMs.
- Connectors communicate with external systems only.
- Data Models carry information between components.
- Components may only depend on the layer immediately below them.

## Why

This keeps responsibilities clearly separated.

- Workflows focus only on orchestration.
- Agents focus only on reasoning.
- Tools remain deterministic and reusable.
- External integrations remain isolated inside connectors.
- Shared services are reusable across the platform.

This makes the system easier to understand, test, maintain and extend.

## Consequences

### Benefits

- Clear ownership of responsibilities.
- Reusable tools across multiple workflows.
- Easy to replace external systems.
- Easy to add new workflows without changing the architecture.
- AI remains one capability of the platform rather than the centre of the architecture.

### Trade-offs

- Slightly more components.
- Requires discipline to keep layer boundaries intact.