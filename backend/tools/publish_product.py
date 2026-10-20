class PublishProductTool:

    def __init__(self, woo): self.woo = woo

    def execute(self, product_id: int):
        return self.woo.publish_product(product_id)