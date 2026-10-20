import base64
import json
import mimetypes
import uuid
from urllib.request import Request, urlopen

class WordPressConnector:
    def __init__(self, url: str, username: str, password: str):
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        self.url, self.auth = url.rstrip("/"), f"Basic {token}"

    def upload_media(self, image_path: str, alt_text: str, title: str) -> dict:
        boundary = uuid.uuid4().hex
        filename = image_path.split("/")[-1]
        image = open(image_path, "rb").read()
        body = f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{filename}\"\r\nContent-Type: {mimetypes.guess_type(filename)[0] or 'application/octet-stream'}\r\n\r\n".encode() + image + b"\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"alt_text\"\r\n\r\n{alt_text}\r\n".encode()
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"title\"\r\n\r\n{title}\r\n".encode()
        body += f"--{boundary}--\r\n".encode()
        request = Request(f"{self.url}/wp-json/wp/v2/media", data=body, headers={"Authorization": self.auth, "Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
        with urlopen(request) as response: return json.loads(response.read())