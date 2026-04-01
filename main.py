from preprocessing.dataset_builder import build_dataset
from prompting.utils import get_few_shot_examples
from prompting.builder_prompt_few_shot import FewShotPrompt
from llm.Ollamaclient import OllamaClient 
from llm.runner import run_experiment 
import random


def main():

    # 1. costruzione dataset 
    dataset = build_dataset(5) 

    # 2. recupero esempi few-shot
    ex_nd, ex_clone, ex_diff = get_few_shot_examples(dataset) 

    # 3. inizializzazione prompt
    prompt_strategy = FewShotPrompt(ex_nd, ex_clone, ex_diff) 

    #mischio dati
    random.shuffle(dataset) 

    # 4. inizializzazione LLM
    llm = OllamaClient(model="llama3") 

    # 5. esecuzione test
    results = run_experiment(dataset, prompt_strategy, llm)

    # 6. stampa risultati
    for r in results:
        print("\n------------------------")
        print(f"TRUE LABEL: {r['label']}") #classififcazione umana 
        print(f"PREDICTION: {r['prediction']}") #output llm pulito 
        print(f"RAW OUTPUT: {r['raw_output']}") #output grezzo


if __name__ == "__main__":
    main()  



