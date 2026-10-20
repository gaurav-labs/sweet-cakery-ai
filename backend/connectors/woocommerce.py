import base64
import json
from urllib.request import Request, urlopen

class WooCommerceConnector:
    def __init__(self, url: str, key: str, secret: str):
        token = base64.b64encode(f"{key}:{secret}".encode()).decode()
        self.url, self.auth = url.rstrip("/"), f"Basic {token}"

    def get_attributes(self) -> list:
        return self._request("GET", "/wp-json/wc/v3/products/attributes")

    def create_product(self, data: dict) -> dict:
        return self._request("POST", "/wp-json/wc/v3/products", data)

    def create_variation(self, product_id: int, data: dict) -> dict:
        return self._request("POST", f"/wp-json/wc/v3/products/{product_id}/variations", data)

    def _request(self, method: str, path: str, data: dict | None = None) -> dict:
        request = Request(f"{self.url}{path}", data=json.dumps(data).encode() if data else None, headers={"Authorization": self.auth, "Content-Type": "application/json"}, method=method)
        with urlopen(request) as response: return json.loads(response.read())

    def get_attribute_term(self, attribute_id: int, slug: str) -> dict:
        terms = self._request("GET", f"/wp-json/wc/v3/products/attributes/{attribute_id}/terms?slug={slug}")
        return terms[0]

    def get_attribute(self, slug: str) -> dict:
        attributes = self._request("GET", "/wp-json/wc/v3/products/attributes")
        return next(a for a in attributes if a["slug"] == slug)

    def publish_product(self, product_id: int) -> dict:
        return self._request("PUT", f"/wp-json/wc/v3/products/{product_id}", {"status": "publish"})