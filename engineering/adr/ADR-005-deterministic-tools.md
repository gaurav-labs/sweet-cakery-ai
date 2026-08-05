# ADR-005

## Title

Deterministic Tools

## Decision

Tools perform a single deterministic responsibility.

Tools may execute business logic, access storage, invoke connectors and read configuration.

Tools return structured output.

Tools must never invoke LLMs, access workflow memory, invoke other tools or invoke agents.

## Why

- Clear separation of responsibilities.
- Tools remain reusable and easy to test.
- Business workflows remain predictable.
- AI is isolated from deterministic execution.

## Trade-offs

- Larger workflows may require more tools.