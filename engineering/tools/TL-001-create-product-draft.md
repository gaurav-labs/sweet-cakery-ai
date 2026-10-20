# TL-001

## Title

Create Product Draft Tool

---

## Purpose

Create a WooCommerce draft product from a ProductDraft using predefined business rules.

---

## Input

- CreateProductDraftRequest

---

## Responsibilities

- Apply pricing rules.
- Apply weight options.
- Apply flavour options.
- Create a WooCommerce draft product.
- Return the created draft information.

---

## Output

- WooCommerceDraft

---

## Uses

- WooCommerce Connector
- Configuration

---

## Never

- Invoke AI.
- Access workflow memory.
- Make business decisions.
- Publish the product.
- Invoke other tools.

---

## Failure

Return a structured error to the Workflow.