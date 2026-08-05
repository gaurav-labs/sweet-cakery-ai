# SPEC-003

## High-Level Architecture

### Purpose

Define the major building blocks of the platform and the responsibilities of each component.

---

## Architecture

                    Entry Points
         (UI / Python CLI / REST API)
                      │
                      ▼
               Workflow Layer
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
     Agent Layer             Tool Layer
          │                       │
          ▼                       ▼
     AI Gateway          Connectors / Storage
                                  │
                                  ▼
                           External Systems

Supporting services:

- Memory
- Security
- Configuration
- Observability

---

## Components

### Entry Points

Receive requests from users or external systems.

Examples:

- Web UI
- Python CLI
- REST API

---

### Workflow

Responsible for orchestration.

Responsibilities:

- Validate requests
- Manage workflow state
- Retrieve and store memory
- Invoke agents
- Handle human approvals
- Handle retries
- Return the final response
- Orchestrate agents, tools and human approvals.

---

### Agent

Responsible for reasoning.

Responsibilities:

- Invoke the AI Gateway when required
- Apply business reasoning
- Produce structured outputs
- Invoke tools

Agents remain stateless.

---

### Tool

Responsible for deterministic execution.

Responsibilities:

- Execute business logic
- Read or write data
- Invoke connectors
- Return results

Tools never invoke LLMs.

---

### Connector

Responsible for communication with external systems.

Examples:

- WooCommerce
- OpenAI
- WhatsApp
- Email

---

### Data Models

Carry information between components.

Examples:

- PublishProductRequest
- ProductDraft
- ChatRequest
- OrderRequest

---

## Platform Services

### AI Gateway

Provides access to LLM providers.

Used by:

- Agents

---

### Memory

Stores conversation and workflow state.

Used by:

- Workflow

---

### Storage

Provides persistent storage.

Used by:

- Tools

---

### Configuration

Provides application and business configuration.

Used by:

- Workflow
- Agents
- Tools

---

### Security

Provides authentication, authorisation and security controls.

Applies to:

- Every component

---

### Observability

Provides logging, tracing and metrics.

Applies to:

- Every component

---

## Design Principles

- Workflow orchestrates.
- Agents think.
- Tools execute.
- Connectors communicate.
- Data Models carry information.
- Shared services provide common capabilities.

Refer to ADR-001 and ADR-002 for architectural decisions.