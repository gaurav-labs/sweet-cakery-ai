import sqlite3
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from models.publish_product_state import PublishProductState

class ProductPublishingGraph:
    def __init__(self, agent, create_draft, publish_tool): self.agent, self.create_draft, self.publish_tool = agent, create_draft, publish_tool

    def build(self):
        graph = StateGraph(PublishProductState)
        graph.add_node("generate_product_draft", self.generate_product_draft)
        graph.add_node("create_product_draft", self.create_product_draft)
        graph.add_node("human_approval", self.human_approval)
        graph.add_node("publish_product", self.publish_product)
        graph.add_edge(START, "generate_product_draft")
        graph.add_edge("generate_product_draft", "create_product_draft")
        graph.add_edge("create_product_draft", "human_approval")
        graph.add_conditional_edges("human_approval", self.route_approval, {"publish": "publish_product", "end": END})
        graph.add_edge("publish_product", END)
        serde = JsonPlusSerializer(allowed_msgpack_modules=[("models.publish_product_request", "PublishProductRequest"), ("models.product_draft", "ProductDraft"), ("models.woocommerce_draft", "WooCommerceDraft")])
        checkpointer = SqliteSaver(sqlite3.connect("product_publishing.db", check_same_thread=False), serde=serde)
        return graph.compile(checkpointer=checkpointer)

    def generate_product_draft(self, state):
        state["product_draft"] = self.agent.generate(state["request"].image); return state

    def create_product_draft(self, state):
        state["woo_draft"] = self.create_draft.execute(state["product_draft"], state["request"].starting_price, state["request"].image); return state

    def human_approval(self, state):
        state["approval"] = interrupt({"product_id": state["woo_draft"].product_id, "message": "Approve this product for publishing?"}); return state

    def publish_product(self, state):
        state["result"] = self.publish_tool.execute(state["woo_draft"].product_id); return state

    def route_approval(self, state):
        return "publish" if state["approval"] == "approved" else "end"