from langgraph.types import Command
from models.product_draft import ProductDraft
from models.publish_product_request import PublishProductRequest
from models.woocommerce_draft import WooCommerceDraft
from workflows.product_publishing import ProductPublishingGraph
from tools.publish_product import PublishProductTool

class FakeAgent:
    def generate(self, image):
        return ProductDraft("Test Cake", "test-cake", "short", "long", "seo", "seo desc", "cake.jpg", "cake")

class FakeTool:
    def execute(self, draft, starting_price, image_path=None):
        return WooCommerceDraft(123, "draft")

class FakePublishTool:
    def __init__(self): self.called = False
    def execute(self, product_id): self.called = True; return {"success": True, "product_id": product_id}

class FakeWoo:
    def __init__(self): self.product_id = None
    def publish_product(self, product_id): self.product_id = product_id; return {"id": product_id, "status": "publish"}


def test_approval_routing():
    state = {"request": PublishProductRequest("cake.jpg", 1200)}

    publish = FakePublishTool()
    graph = ProductPublishingGraph(FakeAgent(), FakeTool(), publish).build()
    config = {"configurable": {"thread_id": "test-approved"}}
    graph.invoke(state, config)
    graph.invoke(Command(resume="approved"), config)
    assert publish.called

    publish = FakePublishTool()
    graph = ProductPublishingGraph(FakeAgent(), FakeTool(), publish).build()
    config = {"configurable": {"thread_id": "test-rejected"}}
    graph.invoke(state, config)
    graph.invoke(Command(resume="rejected"), config)
    assert not publish.called

def test_approval_survives_restart():
    state = {"request": PublishProductRequest("cake.jpg", 1200)}
    publish = FakePublishTool()
    config = {"configurable": {"thread_id": "restart-test"}}

    graph = ProductPublishingGraph(FakeAgent(), FakeTool(), publish).build()
    graph.invoke(state, config)

    publish = FakePublishTool()
    graph = ProductPublishingGraph(FakeAgent(), FakeTool(), publish).build()
    graph.invoke(Command(resume="approved"), config)

    assert publish.called

def test_real_publish_tool_wiring():
    state = {"request": PublishProductRequest("cake.jpg", 1200)}
    woo = FakeWoo()
    publish = PublishProductTool(woo)
    graph = ProductPublishingGraph(FakeAgent(), FakeTool(), publish).build()
    config = {"configurable": {"thread_id": "publish-tool-test"}}
    graph.invoke(state, config)
    graph.invoke(Command(resume="approved"), config)
    assert woo.product_id == 123