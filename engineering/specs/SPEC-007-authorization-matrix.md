# SPEC-007: Authorization Matrix

**Status:** Proposed
**Scope:** API, workflows, MCP tools and business services.

## 1. Objective

Define access permissions for guests, authenticated customers and administrators. All permissions must be enforced by application code, independently of LLM instructions.

## 2. Principal classes

- **Guest:** Unauthenticated user with limited public access.
- **Customer:** Authenticated user accessing their own resources.
- **Administrator:** Authenticated user with explicitly granted administrative permissions.

A role must come from a trusted server-side identity, never from a prompt, request body or model-generated argument.

## 3. API authorization matrix

| Operation | Guest | Customer | Admin |
|---|---|---|---|
| Search published products | Allow | Allow | Allow |
| View published product details | Allow | Allow | Allow |
| Create guest order | Allow | Allow | Allow |
| View own authenticated orders | Deny | Allow | Allow |
| View guest order status | Verified guest flow | Verified guest flow | Authorized support access |
| View another customer's order | Deny | Deny | Explicit support permission |
| Start product publishing | Deny | Deny | Allow |
| View product draft | Deny | Deny | Authorized workflow owner |
| Approve product draft | Deny | Deny | Authorized approver |
| Publish product | Deny | Deny | Controlled publishing workflow |
| Manage users and permissions | Deny | Deny | Explicit permission required |

Admin access does not automatically grant every privileged action. Separate permissions may be required for support, approval and publishing.

## 4. MCP tool authorization matrix

| Tool | Guest | Customer | Admin |
|---|---|---|---|
| search_products | Allow | Allow | Allow |
| get_product_details | Allow | Allow | Allow |
| create_guest_order | Allow | Allow | Allow |
| get_my_orders | Deny | Own orders only | Separate admin workflow |
| get_order_status | Verified guest flow | Own orders only | Explicit support permission |
| create_product_draft | Deny | Deny | Allow |
| request_product_approval | Deny | Deny | Allow if authorized |
| approve_product | Deny | Deny | Authorized approver only |
| publish_product | Deny | Deny | Controlled workflow only |

Tool visibility is not authorization. Every tool must enforce its permissions when executed.

## 5. Resource ownership rules

- Customer order queries must be scoped to the authenticated customer identity.
- Never trust a customer ID supplied by the model or request body to establish ownership.
- Guest order lookup requires verification through a trusted contact channel, expiry and rate limits.
- Product drafts and workflow state must be accessible only to authorized principals.
- Approval must reference the intended draft, version and workflow.
- Publishing must verify approval and allowed workflow state before execution.

## 6. Authorization enforcement points

1. **API:** Authenticate callers and enforce endpoint permissions.
2. **Workflow dispatcher:** Permit only authorized workflow initiation.
3. **MCP server:** Validate caller identity and tool permissions.
4. **Business service:** Enforce resource ownership and business rules.
5. **Connector boundary:** Restrict external operations to approved capabilities.
6. **Approval transition:** Verify approver permissions, draft/version integrity and workflow state.

No layer may assume that an earlier layer has fully authorized a sensitive operation without validating the required context.

## 7. Failure behavior

- Missing or invalid identity: reject protected operations.
- Insufficient permissions: deny the action.
- Ownership mismatch: do not disclose protected resource data.
- Missing guest verification: deny order lookup.
- Invalid or stale approval: reject publishing.
- Policy or identity service failure: fail closed for sensitive operations.

Use consistent error responses without leaking whether another customer's private resource exists.

## 8. Audit requirements

Record, where applicable:

- Request and correlation IDs.
- Authenticated principal and effective permission.
- Action and resource reference.
- Allow or deny decision and reason code.
- Workflow and tool identifiers.
- Execution outcome and latency.

Never log passwords, tokens, payment secrets or unnecessary personal data.

## 9. Acceptance criteria

- Guests cannot access customer history or administrative operations.
- Customers cannot access other customers' orders.
- Model-generated arguments cannot change the caller's identity or permissions.
- Unauthorized MCP calls are denied even if the model attempts them.
- Publishing requires a valid, authorized approval.
- Authorization decisions are testable and auditable.
- New tools and workflows require an explicit permission definition.

## 10. Related documents

- SPEC-005: Extensible AI Platform Architecture.
- SPEC-006: Threat Model.
- ADR-001: Workflow-first architecture.
- ADR-002: Component dependency rules.
- ADR-007: AI Gateway.
