from config.settings import WOOCOMMERCE_URL, WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET
from connectors.woocommerce import WooCommerceConnector

connector = WooCommerceConnector(WOOCOMMERCE_URL, WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET)

for attribute in connector.get_attributes():
    if attribute["slug"] in ["pa_flavor", "pa_size"]: print(attribute["id"], attribute["name"], attribute["slug"])
