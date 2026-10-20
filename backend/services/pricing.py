import json

class PricingService:
    def __init__(self, path: str):
        self.config = json.load(open(path))

    def calculate(self, starting_price: int, tier: str, size: int) -> int:
        pricing = self.config["pricing"][tier]
        return starting_price + pricing["starting_price_addon"] + (size - 1) * pricing["additional_kg_price"]