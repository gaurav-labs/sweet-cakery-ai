# SPEC-005: Extensible AI Platform Architecture

**Status:** Proposed
**Scope:** Sweet Cakery AI platform evolution

## 1. Objective

Evolve Sweet Cakery AI from a product-publishing workflow into a secure, extensible AI platform supporting customer assistance, marketing, analytics and external integrations.

WooCommerce remains the source of truth for products and orders.

## 2. Architecture

flowchart TD
    E["Web UI / CLI / REST API / Scheduler"] --> S["Security API"]
    S --> D["Workflow Dispatcher"]
    D --> W1["Product Publishing"]
    D --> W2["Customer Assistant"]
    D --> W3["Marketing"]
    D --> W4["Analytics"]
    D --> W5["Integrations"]
    W1 & W2 & W3 & W4 & W5 --> SH["Shared Platform Services"]
    SH --> AI["AI Gateway"]
    SH --> MCP["MCP Tools & Policies"]
    SH --> OBS["Observability"]
    SH --> ST["Application Storage"]
    W1 & W2 --> WC["WooCommerce Connector"]
    W3 & W4 & W5 --> EXT["External Connectors"]


The diagram represents the target architecture, not the current implementation.

## 3. Component responsibilities

| Component | Responsibility |
|---|---|
| Security API | Authentication, request validation and API-level authorization |
| Workflow Dispatcher | Route authorized requests to explicit workflow implementations |
| Workflows | Own business orchestration, workflow state and human approval |
| Agents | Interpret context and use the AI Gateway when reasoning is needed |
| AI Gateway | Centralize LLM access, provider/model policies, timeouts, retries, structured output, token usage and cost tracking |
| MCP tools | Expose explicitly permitted capabilities to AI clients |
| Business services | Enforce deterministic business rules and execute operations |
| Connectors | Communicate with WooCommerce and other external systems |
| Observability | Collect correlated logs, traces, metrics and security events |
| Application storage | Store platform-owned state without replacing external business systems |

## 4. Dependency rules

- Entry points invoke workflows through the application boundary.
- Workflows orchestrate agents, tools and approval steps.
- Agents access LLMs only through the AI Gateway.
- Tools execute deterministic operations and never invoke LLMs directly.
- Business services enforce authorization and business rules independently of the model.
- Connectors isolate external-system APIs and credentials.
- Shared services must not depend on individual workflow implementations.
- Workflow-specific state must not leak into unrelated workflows.
- All sensitive operations must be authorized at execution time.

## 5. Security architecture

### Identity and authorization

Support three principal classes:

- **Guest:** public catalogue search and permitted guest-order operations.
- **Customer:** guest capabilities plus access to their own authenticated orders.
- **Administrator:** explicitly authorized administrative and publishing operations.

Every sensitive operation must enforce identity, permissions, resource ownership and business rules server-side.

Guest order lookup requires a secure verification mechanism; an order number alone is insufficient.

### AI security

- Treat user input, retrieved content and model output as untrusted.
- Validate tool arguments and outputs against defined schemas.
- Enforce authorization independently of model instructions and tool visibility.
- Apply rate limits, token budgets and execution timeouts.
- Prevent unauthorized data access and tool execution.
- Require authenticated human approval for privileged publishing actions.
- Bind approvals to the specific draft/version being approved.

### MCP security

MCP is a controlled tool interface, not an authorization boundary by itself.

Tool execution must enforce the caller's identity, allowed actions and resource permissions. Administrative tools must not be accessible to guests or ordinary customers.

## 6. Workflow extensibility

New workflows should be introduced as independent modules with explicit inputs, outputs, state and dependencies.

Initial workflows:

1. Product publishing.
2. Customer assistant and order management.
3. Marketing operations.
4. Business analytics.
5. External platform integrations.

Use an explicit workflow dispatcher initially. Introduce dynamic registration or plugin discovery only when justified by actual requirements.

New workflows should reuse shared security, AI, observability and connector capabilities without modifying unrelated workflows.

## 7. Data ownership

- WooCommerce owns operational product and order records.
- Each workflow owns its execution state.
- Application storage owns platform-specific records such as audit metadata and workflow references.
- Knowledge indexes are derived from authoritative sources and must not become the source of truth.
- Secrets must be managed outside source code and excluded from logs.

## 8. Observability and evaluation

Correlate each request across the API, workflow, AI Gateway, MCP tools and external connectors.

Measure:

- Request and workflow latency, error rate and completion rate.
- Model latency, token consumption and cost.
- Tool selection, execution results and authorization denials.
- Prompt-injection and unauthorized-access regression results.
- Order accuracy, duplicate prevention and publishing success.
- Rate-limit enforcement and resource-budget violations.

Keep security audit events protected against unauthorized modification. Never log credentials or unnecessary sensitive data.

Maintain repeatable functional, security and AI-quality evaluations.

## 9. Implementation phases

1. Review existing architecture, code and security gaps.
2. Establish the application security boundary and authorization policies.
3. Introduce the customer assistant and controlled MCP tools.
4. Integrate customer ordering and authenticated order history.
5. Extend the existing product-publishing workflow with secure administrative approval.
6. Add security evaluations, observability and resource controls.
7. Add marketing, analytics and external integrations incrementally.

## 10. Acceptance criteria

- Existing product publishing continues to work.
- Guest, customer and administrator permissions are independently enforced.
- Customers cannot access other customers' orders.
- Model manipulation cannot bypass tool authorization.
- Privileged publishing requires authenticated, authorized approval.
- New workflows can reuse platform capabilities without duplicating core security logic.
- AI and business operations are observable and testable.
- WooCommerce remains the source of truth for products and orders.

## 11. Related decisions

- ADR-001: Workflow-first architecture.
- ADR-002: Component dependency rules.
- ADR-007: AI Gateway.
- ADR-008: Memory ownership.

This specification defines the target architecture. Existing implementations must be inspected before implementation plans are finalized.
