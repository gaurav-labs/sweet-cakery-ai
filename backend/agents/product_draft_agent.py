from models.product_draft import ProductDraft
from models.product_draft_response import ProductDraftResponse
from services.ai_gateway import AIGateway

class ProductDraftAgent:
    def __init__(self, gateway: AIGateway, prompt: str): self.gateway, self.prompt = gateway, prompt
    def generate(self, image: str) -> ProductDraft:
        response = self.gateway.generate(self.prompt, "", ProductDraftResponse, image=image)
        return ProductDraft(**response.model_dump())

