# WF-001

## Title

Product Publishing

## Purpose

Publish a new WooCommerce product from minimal user input.

---

## Entry Points

- Python CLI
- Web UI
- REST API

---

## Workflow State

- request
- product_draft
- approval
- result
- error

---

## Workflow Steps

Validate Request
        │
        ▼
Product Generation Agent
        │
        ▼
Create Product Draft Tool
        │
        ▼
Human Approval
        │
        ▼
Publish Product Tool
        │
        ▼
Trigger Knowledge Indexing Workflow
        │
        ▼
Complete

---

## Agent

### Product Generation Agent

Responsibilities:

- Generate product content.
- Generate SEO metadata.
- Generate image metadata.
- Generate product categories.
- Generate product draft.

---

## Tools

- Create Product Draft
- Publish Product

---

## Connectors

- WooCommerce Connector

---

## Data Models

- PublishProductRequest
- ProductDraft
- PublishProductResult

---

## Success Result

- Product ID
- Product URL
- Status

---

## Failure Handling

- Request validation failure
- AI generation failure
- Draft creation failure
- Approval rejected
- Product publishing failure

---

## Future Enhancements

- Bulk product publishing
- Product update workflow
- Automatic image optimisation
- Automatic knowledge indexing after approval