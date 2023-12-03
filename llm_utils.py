import base64
import cv2
from openai import OpenAI
import re

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
class LLMUtils:
    def __init__(self) -> None:
        self.openai_client = OpenAI()

    def chat_with_image(self, prompt, image_path):
        base64_img = encode_image(image_path)

        response = self.openai_client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=
            [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_img}"
                            }
                        }
                    ],
                }
            ],
            max_tokens=1000,
        )
        return response.choices[0].message.content
    
    def extract_python_code(self, response):
        code_list = re.findall(r"```(.*?)```", response, re.DOTALL)
        if len(code_list) == 0:
            raise RuntimeError("No code")
    
        code: str = code_list[0]
        prefix = "python"
        if code.startswith(prefix):
            code = code[len(prefix):]
        
        lines = code.split("\n")
        code_list = []
        for line in lines:
            if len(line) > 0:
                code_list.append(line)
        
        return code_list[:]
