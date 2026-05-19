from preprocessing.trasformer.html_extractor import html_extractor

from engine.extractor import extract_functionality
from engine.classifier import classify_states


def compare_states(dom1,dom2,extraction_prompt,classification_prompt,llm_client):

    # preprocessing
    dom1 = html_extractor(dom1)
    dom2 = html_extractor(dom2)

    # extraction
    extraction = extract_functionality(dom1,dom2,extraction_prompt,llm_client)

    # classification
    result = classify_states(extraction,classification_prompt,llm_client)

    return result 