from dataclasses import dataclass

@dataclass
class PublishProductRequest:
    image: str
    starting_price: int