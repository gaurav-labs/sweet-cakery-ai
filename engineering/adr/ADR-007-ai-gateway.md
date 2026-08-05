# ADR-007

## Title

AI Gateway

## Decision

All LLM interactions must go through the AI Gateway.

Agents may recommend a provider and model.

The AI Gateway is responsible for executing the request, enforcing platform policies, handling authentication, retries, timeouts, structured output, logging, token usage and cost tracking.

The AI Gateway may reject or override unsupported provider/model combinations based on platform policy.

## Why

- Isolates LLM providers from the application.
- Centralises operational concerns.
- Gives developers control over AI behaviour.
- Gives platform owners control over execution and policy.

## Trade-offs

- Adds one abstraction layer between agents and LLM providers.