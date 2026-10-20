from config.settings import WP_URL, WP_USERNAME, WP_APP_PASSWORD
from connectors.wordpress import WordPressConnector

result = WordPressConnector(WP_URL, WP_USERNAME, WP_APP_PASSWORD).upload_media("tests/cake.jpg", "Test cake image from Sweet Cakery AI")
print(result["id"])
print(result["source_url"])
print(result["alt_text"])