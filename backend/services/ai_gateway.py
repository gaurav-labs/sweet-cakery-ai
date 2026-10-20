import base64
from typing import Any, TypeVar
from openai import OpenAI

T = TypeVar("T")

class AIGateway:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str, output_type: type[T], context: list[str] | None = None, image: str | None = None, model: str | None = None) -> T:
        content: list[dict[str, Any]] = [{"type": "input_text", "text": user_prompt}]
        if image: content.append({"type": "input_image", "image_url": f"data:image/jpeg;base64,{base64.b64encode(open(image, 'rb').read()).decode()}"})
        if context: content.append({"type": "input_text", "text": "\n".join(context)})
        response = self.client.responses.parse(model=model or self.model, instructions=system_prompt, input=[{"role": "user", "content": content}], text_format=output_type)
        return response.output_parsed