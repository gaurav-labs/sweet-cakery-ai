from models.product_draft import ProductDraft
from models.woocommerce_draft import WooCommerceDraft
from services.pricing import PricingService
from services.variation_builder import VariationBuilder
from connectors.woocommerce import WooCommerceConnector
from connectors.wordpress import WordPressConnector

class CreateProductDraftTool:
    def __init__(self, woo: WooCommerceConnector, wordpress: WordPressConnector, pricing: PricingService): self.woo, self.wordpress, self.pricing = woo, wordpress, pricing

    def execute(self, draft: ProductDraft, starting_price: int, image_path: str | None = None) -> WooCommerceDraft:
        flavor_id = self.woo.get_attribute("pa_flavor")["id"]
        size_id = self.woo.get_attribute("pa_size")["id"]
        variations = VariationBuilder(self.pricing).build(starting_price, flavor_id, size_id)
        data = {"name": draft.title, "slug": draft.slug, "type": "variable", "status": "draft", "description": draft.long_description, "short_description": draft.short_description, "meta_data": [{"key": "rank_math_description", "value": draft.seo_description}], "attributes": [{"id": flavor_id, "variation": True, "visible": True, "options": sum(self.pricing.config["flavors"].values(), [])}, {"id": size_id, "variation": True, "visible": True, "options": [f"{size} KG" for size in self.pricing.config["sizes"]]}]}
        if image_path:
            media = self.wordpress.upload_media(image_path, draft.image_alt, draft.image_name)
            data["images"] = [{"id": media["id"], "alt": draft.image_alt}]
        product = self.woo.create_product(data)
        for variation in variations: self.woo.create_variation(product["id"], variation)
        return WooCommerceDraft(product["id"], product["status"])