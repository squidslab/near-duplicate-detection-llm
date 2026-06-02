import requests


class OllamaClient:

    def __init__(
        self,
        model="qwen2.5:7b",
        url="http://localhost:11434/api/generate",
        timeout=120
    ):

        self.model = model
        self.url = url
        self.timeout = timeout

    def generate(self, prompt):

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        }

        try:

            response = requests.post(
                self.url,
                json=payload,
                timeout=self.timeout
            )

            response.raise_for_status()

            data = response.json()

            return data.get("response", "").strip()

        except requests.Timeout:
            print("[ERROR] Ollama timeout")
            return None

        except requests.RequestException as e:
            print(f"[ERROR] HTTP request failed: {e}")
            return None

        except Exception as e:
            print(f"[ERROR] Unexpected LLM error: {e}")
            return None