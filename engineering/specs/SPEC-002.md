# SPEC-002

## Non-Functional Requirements

### Security

**NFR-001** Guest users can interact with AI without authentication.

**NFR-002** Authentication is required for protected operations.

**NFR-003** Every protected action must be authorised.

**NFR-004** Secrets must never be stored in source code.

---

### Reliability

**NFR-005** The system should fail gracefully when an AI provider is unavailable.

**NFR-006** Business rules must continue to work without AI.

---

### Observability

**NFR-007** Every AI request must be logged.

**NFR-008** Every tool invocation must be traceable.

**NFR-009** Errors must be logged with enough information for troubleshooting.

---

### Performance

**NFR-010** Customer interactions should feel responsive.

**NFR-011** Long-running tasks should execute in the background.

---

### Maintainability

**NFR-012** Business logic must remain separate from platform logic.

**NFR-013** AI providers should be replaceable with minimal code changes.

**NFR-014** Configuration should come from environment variables.

---

### Quality

**NFR-015** Every major feature must have documentation.

**NFR-016** Every major feature must have automated tests.
