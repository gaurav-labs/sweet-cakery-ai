import os
import uuid
from agents.product_draft_agent import ProductDraftAgent
from config.settings import OPENAI_API_KEY, OPENAI_MODEL, WOOCOMMERCE_URL, WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WP_URL, WP_USERNAME, WP_APP_PASSWORD
from connectors.woocommerce import WooCommerceConnector
from connectors.wordpress import WordPressConnector
from models.publish_product_request import PublishProductRequest
from services.ai_gateway import AIGateway
from services.pricing import PricingService
from tools.create_product_draft import CreateProductDraftTool
from tools.publish_product import PublishProductTool
from workflows.product_publishing import ProductPublishingGraph
from langgraph.types import Command

gateway = AIGateway(OPENAI_API_KEY, OPENAI_MODEL)
agent = ProductDraftAgent(gateway, open("prompts/product_generation.txt").read())
woo = WooCommerceConnector(WOOCOMMERCE_URL, WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET)
wordpress = WordPressConnector(WP_URL, WP_USERNAME, WP_APP_PASSWORD)
pricing = PricingService("config/pricing.json")
create_draft = CreateProductDraftTool(woo, wordpress, pricing)
graph = ProductPublishingGraph(agent, create_draft, PublishProductTool(woo)).build()

async def generate_product(image, starting_price):
    workflow_id = f"publish-{uuid.uuid4()}"
    image_path = f"/tmp/{workflow_id}-{image.filename}"
    with open(image_path, "wb") as f: f.write(await image.read())
    config = {"configurable": {"thread_id": workflow_id}}
    result = graph.invoke({"request": PublishProductRequest(image_path, starting_price)}, config)
    return workflow_id, result["woo_draft"].product_id

def approve_product(workflow_id):
    config = {"configurable": {"thread_id": workflow_id}}
    result = graph.invoke(Command(resume="approved"), config)
    return result["result"]