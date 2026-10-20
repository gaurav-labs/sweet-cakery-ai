from dataclasses import dataclass

@dataclass
class PublishProductResult:
    success: bool
    product_id: int | None = None
    product_url: str | None = None
    message: str | None = None