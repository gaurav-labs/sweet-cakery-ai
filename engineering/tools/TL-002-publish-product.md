# TL-002

## Title

Publish Product Tool

---

## Purpose

Publish an existing WooCommerce draft product.

---

## Input

- WooCommerceDraft

---

## Responsibilities

- Publish the WooCommerce draft product.
- Return the published product information.

---

## Output

- PublishProductResult

---

## Uses

- WooCommerce Connector

---

## Never

- Invoke AI.
- Modify product content.
- Apply business rules.
- Invoke other tools.

---

## Failure

Return a structured error to the Workflow.