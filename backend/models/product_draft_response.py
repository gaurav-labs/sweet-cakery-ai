from pydantic import BaseModel

class ProductDraftResponse(BaseModel):
    title: str
    slug: str
    short_description: str
    long_description: str
    seo_title: str
    seo_description: str
    image_name: str
    image_alt: str
