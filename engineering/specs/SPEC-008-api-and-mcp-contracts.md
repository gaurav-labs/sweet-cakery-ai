# SPEC-008: API and MCP Contracts

**Status:** Proposed
**Depends on:** SPEC-005, SPEC-006, SPEC-007

## 1. Objective

Define API endpoints, MCP tool contracts, trusted identity propagation, authorization enforcement, and standard errors for the Sweet Cakery AI platform.

## 2. API Contracts

| Method | Endpoint | Access | Purpose |
|---|---|---|---|
| GET | `/api/v1/products` | Public | Search products |
| GET | `/api/v1/products/{product_id}` | Public | Get product details |
| POST | `/api/v1/orders/guest` | Guest | Create a guest order |
| GET | `/api/v1/orders/me` | Customer | List own orders |
| GET | `/api/v1/orders/{order_id}` | Customer or verified guest | Retrieve an authorized order |
| POST | `/api/v1/admin/product-publishing` | Admin | Start product draft workflow |
| GET | `/api/v1/admin/workflows/{workflow_id}` | Authorized admin | Get workflow status |
| POST | `/api/v1/admin/workflows/{workflow_id}/approval` | Authorized approver | Approve or reject a specific draft version |

These are proposed target contracts. Existing routes may differ and must be mapped before implementation.

## 3. Identity Context

The API security layer creates a trusted identity context after validating the session or token.

Required fields:
- `principal_id`
- `principal_type`
- `roles` and effective `permissions`
- `auth_method`
- `request_id` and `trace_id`

Rules:
- Never derive identity or permissions from prompts, model output, or request-body fields.
- Customer IDs for personal order queries come from the trusted identity context.
- Propagate identity through workflows and tools using trusted internal context.
- For remote MCP, validate transport credentials, token audience, expiry, and scopes.
- Never trust arbitrary forwarded identity headers.
- Every sensitive operation rechecks authorization at execution time.

## 4. MCP Tool Contracts

| Tool | Required inputs | Authorization |
|---|---|---|
| `search_products` | Query, optional filters, limit/cursor | Public |
| `get_product_details` | `product_id` | Public |
| `create_guest_order` | Items, contact, delivery details, idempotency key | Guest-order policy |
| `get_my_orders` | Optional status, limit/cursor | Customer; derive customer ID from identity |
| `get_order_status` | `order_id`, guest verification when applicable | Order owner or verified guest |
| `create_product_draft` | Validated upload reference, product metadata, starting price | `product:draft:create` |
| `request_product_approval` | Workflow ID, draft ID, draft version | Authorized requester |
| `approve_product` | Workflow ID, draft ID, version, decision, optional reason | `product:approve` |
| `publish_product` | Workflow ID, draft ID, version | Internal workflow only |

### Tool rules

- The model may propose tool arguments but cannot grant itself permissions.
- MCP tool visibility is not an authorization boundary.
- Enforce authorization in the MCP adapter and underlying business service.
- Validate all inputs against explicit schemas, bounds, and allowed values.
- Resolve product prices, variations, availability, and totals from trusted WooCommerce data; never trust client-supplied totals.
- Require idempotency for order creation.
- Publishing must verify an authorized approval for the exact draft version.
- Approval and publication are separate operations. Reject stale or replayed approvals.
- `publish_product` must not be directly exposed as an unrestricted model-callable tool.

## 5. Approval Contract

An approval decision must include:
- Workflow ID
- Draft ID and exact draft version
- Decision: `approve` or `reject`
- Optional reason

The server supplies the approver identity. The workflow verifies the approver's permission, draft ownership/context, current version, and pending state.

Reject stale versions, duplicate decisions, unauthorized approvers, and attempts to publish unapproved drafts.

## 6. Standard Error Contract

Return a consistent structure:

    {
      "error": {
        "code": "RESOURCE_FORBIDDEN",
        "message": "The requested operation is not permitted.",
        "request_id": "server-generated-id",
        "retryable": false
      }
    }

| Status | Meaning |
|---|---|
| 400 | Invalid input |
| 401 | Missing or invalid authentication |
| 403 | Authenticated but unauthorized |
| 404 | Resource missing; use generic responses where needed to prevent enumeration |
| 409 | Duplicate request or stale workflow/draft version |
| 413 | Upload exceeds configured limits |
| 429 | Rate limit exceeded |
| 502/503 | External provider or connector unavailable |

Do not expose stack traces, credentials, internal prompts, or sensitive resource details in errors.

## 7. Observability

Propagate `request_id` and `trace_id` across API, workflow, AI Gateway, MCP tools, and connectors.

Record structured security events with:
- Principal ID where available
- Action, resource, authorization decision, and outcome
- Workflow/request correlation IDs
- Latency and error category

Never log secrets, authentication tokens, or unnecessary customer PII. Keep security audit records access-controlled and tamper-resistant.

## 8. Validation and Acceptance Criteria

- Cross-customer order access is denied.
- Guest order lookup requires verification that cannot be bypassed by guessing IDs.
- Model-supplied identity fields never override trusted identity.
- Authorization is enforced independently of tool visibility.
- Unauthorized users cannot create, approve, or publish product drafts.
- Approval is bound to an exact draft version and authorized approver.
- Duplicate order requests do not create duplicate orders.
- Inputs, uploads, rate limits, timeouts, and external failures are handled safely.
- Security events are correlated without leaking secrets or unnecessary PII.

## 9. Implementation Order

1. Map current routes and MCP/tool interfaces against this target contract.
2. Add trusted identity context and centralized authorization.
3. Secure existing product-publishing and approval endpoints.
4. Define and validate tool schemas and error responses.
5. Add authorization, ownership, replay, and idempotency tests.
6. Implement customer/order workflows only after these controls pass.
