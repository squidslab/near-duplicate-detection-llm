from fastapi import FastAPI
from pydantic import BaseModel

from engine.compare_state import compare_states

from llm.ollamaclient import OllamaClient

from prompting.classification_prompt.builder_prompt_zero_shot_classification_extr import ZeroShotPromptExtr

from prompting.functionality_extraction_prompt.builder_prompt_zero_shot_extraction import ZeroShotPromptForFunctionalityExtraction


app = FastAPI()


# inizializzazione globale
llm_client = OllamaClient()

extraction_prompt = ZeroShotPromptForFunctionalityExtraction()

classification_prompt = ZeroShotPromptExtr()


class CompareRequest(BaseModel): #definisco la strttura json della richiesta 
    dom1: str
    dom2: str


@app.post("/compare") #definisco endpoint 
def compare(request: CompareRequest):

    result = compare_states(
        request.dom1,
        request.dom2,
        extraction_prompt,
        classification_prompt,
        llm_client
    )

    return result