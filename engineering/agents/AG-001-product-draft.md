# AG-001

## Title

Product Draft Agent

---

## Purpose

Generate a complete ProductDraft from a PublishProductRequest.

---

## Input

- PublishProductRequest
- Relevant workflow context

---

## Responsibilities

- Invoke the AI Gateway
- Generate a ProductDraft
- Return structured output

---

## Output

- ProductDraft

---

## Never

- Publish products
- Apply business rules
- Apply pricing rules
- Access workflow memory
- Access storage
- Call connectors
- Make workflow decisions

---

## Failure

Return a structured error to the Workflow.