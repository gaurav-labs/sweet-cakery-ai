from dataclasses import dataclass

@dataclass
class PublishProductRequest:
    image: str
    starting_price: float
    weight_options: list[int] | None = None
    custom_instructions: str | None = None