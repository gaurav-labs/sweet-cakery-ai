# SPEC-006: Sweet Cakery AI Threat Model

**Status:** Proposed
**Scope:** Product publishing, customer assistant, MCP tools and future workflows.

## 1. Objective

Identify security threats, trust boundaries and mitigations before implementing new capabilities. Security controls must be enforced by deterministic application code, not delegated to the LLM.

## 2. Assets

- Customer identities, sessions and personal information.
- WooCommerce products, orders, prices and customer records.
- Product images, generated drafts and publishing approvals.
- LLM credentials, WooCommerce credentials and WordPress credentials.
- Workflow state, tool permissions and application configuration.
- Audit records, AI traces and security evaluation results.

## 3. Trust boundaries

1. **User → API:** All user input, uploaded files and requests are untrusted.
2. **API → workflow:** Only validated, authorized requests may initiate workflows.
3. **Workflow → LLM:** Prompts, retrieved content and model outputs may be manipulated or incorrect.
4. **Agent → MCP/tools:** Tool arguments and requested actions require independent validation.
5. **Business service → WooCommerce:** External API responses and failures must be handled safely.
6. **Application → storage/telemetry:** Sensitive information must be protected from unauthorized access and disclosure.
7. **Approval → publishing:** Approval must be authenticated, authorized and bound to the exact draft/version.

## 4. Threat actors

- Anonymous users attempting unauthorized access or resource exhaustion.
- Authenticated customers attempting to access other customers' data.
- Compromised or malicious administrator accounts.
- Attackers manipulating prompts, uploaded content or retrieved product descriptions.
- Compromised integrations, credentials or dependencies.

## 5. Threat scenarios and mitigations

| ID | Threat | Required mitigation |
|---|---|---|
| T01 | Unauthenticated administrative API access | Require authentication and deny by default. |
| T02 | Customer accesses another customer's orders | Enforce resource ownership in the business service on every request. |
| T03 | Guest guesses an order reference | Require secure contact verification, expiry and rate limits. |
| T04 | Prompt injection requests privileged actions | Treat model output as untrusted; enforce tool authorization independently. |
| T05 | Malicious retrieved content manipulates the agent | Treat retrieved content as data, not trusted instructions; restrict tool capabilities. |
| T06 | Unauthorized or replayed publishing approval | Authenticate approvers; bind approval to draft ID, version and workflow state. |
| T07 | Malicious or oversized image upload | Validate file type and size, generate server-side filenames and isolate uploaded files. |
| T08 | Duplicate orders or repeated tool execution | Use idempotency keys and deterministic order-state validation. |
| T09 | Excessive requests or expensive model calls | Apply IP/user rate limits, token budgets, timeouts and concurrency limits. |
| T10 | Secrets or personal information leak through logs | Redact sensitive data, restrict log access and define retention. |
| T11 | Compromised connector or excessive service permissions | Use least-privilege credentials, protected secrets and explicit connector permissions. |
| T12 | Workflow state tampering or unauthorized resume | Validate workflow ownership, allowed state transitions and approval identity. |
| T13 | Model invents prices or order status | Retrieve authoritative data and calculate prices in deterministic business services. |
| T14 | Tool failure or external API timeout creates inconsistent state | Use bounded retries, idempotency, explicit failure states and reconciliation. |

## 6. Existing implementation observations

Based on the reviewed source files:

- The current publishing API exposes product-generation and approval endpoints without visible authentication or authorization checks.
- The approval endpoint accepts a workflow ID and resumes the workflow with an approval value. Authorization and approval integrity must be enforced before publishing.
- Uploaded images are written to temporary storage using a filename derived from the upload. File validation, size limits and safe filename handling need review.
- The AI Gateway centralizes LLM access, but security policy enforcement and telemetry need further implementation and testing.
- WooCommerce and WordPress credentials are loaded through configuration. Secret handling and deployment permissions require verification.

These are observations from the reviewed files, not a complete security audit.

## 7. Security principles

- Deny by default and enforce least privilege.
- Separate authentication, authorization and business validation.
- Never treat prompts, model outputs or tool arguments as trusted.
- Enforce authorization at the point of execution.
- Keep approval and payment decisions outside autonomous model authority.
- Keep WooCommerce as the source of truth for products and orders.
- Correlate application, workflow, AI and tool events without logging secrets.
- Fail safely when identity, policy, approval or required verification cannot be established.

## 8. Security testing

Create repeatable tests for:

- Guest, customer and administrator access boundaries.
- Cross-customer order access and guest order verification.
- Direct and indirect prompt injection.
- Unauthorized MCP tool calls and malformed tool arguments.
- Approval replay, stale drafts and unauthorized workflow resume.
- Upload validation, rate limits and duplicate order prevention.
- Secret/PII leakage and failure handling.
- Connector errors, timeouts and inconsistent workflow state.

For defined authorization regression tests, the target is zero successful unauthorized operations.

## 9. Implementation priority

1. Authentication, authorization and administrative endpoint protection.
2. Workflow ownership and approval integrity.
3. Customer order ownership and guest verification.
4. MCP tool authorization and prompt-injection resistance.
5. Upload validation, rate limits and idempotency.
6. Audit logging, observability and security evaluation.
7. Connector hardening and future workflow-specific threat reviews.

## 10. Acceptance criteria

- Every sensitive operation has an explicit authorization rule.
- Customers cannot retrieve other customers' orders.
- Guests cannot invoke privileged administrative operations.
- Prompt injection cannot bypass tool or business-service authorization.
- Publishing requires valid approval for the intended draft/version.
- Security failures are observable without exposing secrets.
- New workflows undergo threat review before receiving permissions.

## 11. Related documents

- SPEC-001 through SPEC-005.
- ADR-001: Workflow-first architecture.
- ADR-002: Component dependency rules.
- ADR-007: AI Gateway.
- ADR-008: Memory ownership.

This threat model is a living document. Update it when trust boundaries, integrations, permissions or workflows change.
