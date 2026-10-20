from services.pricing import PricingService

class VariationBuilder:
    def __init__(self, pricing: PricingService): self.pricing = pricing

    def build(self, starting_price: int, flavor_id: int, size_id: int) -> list[dict]:
        variations = []
        for tier, flavors in self.pricing.config["flavors"].items():
            for flavor in flavors:
                for size in self.pricing.config["sizes"]:
                    variations.append({"attributes": [{"id": flavor_id, "option": flavor}, {"id": size_id, "option": f"{size} KG"}], "regular_price": str(self.pricing.calculate(starting_price, tier, size))})
        return variations
