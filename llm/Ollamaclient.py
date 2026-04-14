import requests
from preprocessing.image_loader import encode_image


class OllamaClient:

    def __init__(self, model="llama3"):
        self.model = model
        self.url = "http://localhost:11434/api/chat"   

    def generate(self, input_data):

        if isinstance(input_data, str):
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": input_data
                    }
                ],
                "stream":False,
                "options": {
                    "temperature": 0
                }
            }

        elif isinstance(input_data, dict):
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": input_data["text"],
                        "images": [
                            encode_image(input_data["image1"]),
                            encode_image(input_data["image2"])
                        ]
                    }
                ],
                "stream":False,
                "options": {
                    "temperature": 0
                }
            }

        else:
            raise ValueError("Invalid input type for generate()")

        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()

            return response.json()["message"]["content"].strip()

        except Exception as e:
            print(f"Errore LLM: {e}")
            return None