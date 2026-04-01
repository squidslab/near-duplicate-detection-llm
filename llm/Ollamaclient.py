import requests

class OllamaClient:

    def __init__(self, model="llama3"): #inizializzo proprietà tramite costrutture 
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt): #genero payload 
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status() #controllo status code e lancio eccezzione 
            return response.json()["response"].strip() #recupero risposta in formato json converto in dizionario e la ritorno 
        except Exception as e:
            print(f"Errore LLM: {e}")
            return None