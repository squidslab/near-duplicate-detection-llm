from preprocessing.dataset_builder import build_dataset
from prompting.utils import get_few_shot_examples
from prompting.builder_prompt_few_shot import FewShotPrompt
from llm.Ollamaclient import OllamaClient 
from llm.runner import run_experiment 
import time 


def main():


 
    print("[INFO] Costruzione dataset...")

    dataset = build_dataset(n_per_class=5, seed=42)

    print(f"[INFO] Dimensione dataset: {len(dataset)}") 

    # 2. recupero esempi few-shot
    ex_nd, ex_clone, ex_diff = get_few_shot_examples(dataset) 

    # 3. inizializzazione prompt
    prompt_strategy = FewShotPrompt(ex_nd, ex_clone, ex_diff) 

    # 4. inizializzazione LLM
    llm = OllamaClient(model="llama3") 

    start = time.time()

    # 5. esecuzione test 
    results = run_experiment(dataset, prompt_strategy, llm) 

    end = time.time()

    # 6. stampa risultati
    for r in results:
        print("\n------------------------")
        print(f"TRUE LABEL: {r['label']}") #classififcazione umana 
        print(f"PREDICTION: {r['prediction']}") #output llm pulito 
        print(f"RAW OUTPUT: {r['raw_output']}") #output grezzo 

    print(f"\n[INFO] Tempo totale: {end - start:.2f} sec")
    print(f"[INFO] Tempo medio: {(end - start) / len(dataset):.2f} sec") 


if __name__ == "__main__":
    main()  



