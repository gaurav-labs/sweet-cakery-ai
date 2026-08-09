# ADR-004

## Title

Stateless Agents

## Decision

Agents are stateless.

Agents receive all required context from the workflow and return structured output.

Agents may invoke the AI Gateway and tools but must never access memory, storage, connectors or other agents directly.

## Why

- Clear separation of responsibilities.
- Agents remain reusable and easy to test.
- Workflows own orchestration and state.
- Changes to memory or storage do not affect agents.

## Trade-offs

- Workflows are responsible for preparing the agent context.