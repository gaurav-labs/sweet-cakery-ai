from config.settings import OPENAI_API_KEY, OPENAI_MODEL
from services.ai_gateway import AIGateway
from agents.product_draft_agent import ProductDraftAgent

gateway = AIGateway(OPENAI_API_KEY, OPENAI_MODEL)
agent = ProductDraftAgent(gateway, open("prompts/product_generation.txt").read())

draft = agent.generate("tests/cake.jpg")

print(draft)