from fastapi import FastAPI, File, Form, UploadFile
from app import generate_product, approve_product

app = FastAPI()

@app.post("/workflows/product-publishing")
async def start_product_publishing(image: UploadFile = File(...), starting_price: int = Form(...)):
    workflow_id, product_id = await generate_product(image, starting_price)
    return {"workflow_id": workflow_id, "product_id": product_id, "status": "awaiting_approval"}

@app.post("/workflows/{workflow_id}/approve")
async def approve(workflow_id: str):
    result = approve_product(workflow_id)
    return {"product_id": result["id"], "status": result["status"], "url": result["permalink"]}