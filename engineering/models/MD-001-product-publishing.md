# MD-001

## Title

Product Publishing Data Model

---

## PublishProductRequest

Purpose

Capture the minimum information required to publish a new product.

### Required

| Field | Description |
|--------|-------------|
| image | Product image |
| starting_price | Starting price of the product |

### Optional

| Field | Description |
|--------|-------------|
| weight_options | Supported weight options |
| custom_instructions | Additional instructions for AI |

---

## ProductDraft

Purpose

Represents the generated product before publication.

### Fields

- title
- slug
- short_description
- long_description
- seo_title
- seo_description
- image_name
- image_alt
- categories
- status

---

## PublishProductResult

Purpose

Represents the result of the publishing workflow.

### Fields

- success
- product_id
- product_url
- message