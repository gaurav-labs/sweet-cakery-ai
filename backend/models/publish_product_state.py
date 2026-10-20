from typing import TypedDict
from models.approval_status import ApprovalStatus
from models.product_draft import ProductDraft
from models.publish_product_request import PublishProductRequest
from models.publish_product_result import PublishProductResult
from models.woocommerce_draft import WooCommerceDraft
from models.workflow_error import WorkflowError

class PublishProductState(TypedDict, total=False):
    request: PublishProductRequest
    product_draft: ProductDraft
    woo_draft: WooCommerceDraft
    approval: ApprovalStatus
    result: PublishProductResult
    error: WorkflowError