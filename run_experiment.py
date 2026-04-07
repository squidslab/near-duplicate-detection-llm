from preprocessing.dataset_builder import build_dataset
from prompting.utils import get_few_shot_examples
from prompting.builder_prompt_few_shot import FewShotPrompt
from llm.Ollamaclient import OllamaClient 
from llm.runner import run_experiment 
from llm.runnerParallel.runnerP import run_experiment_p
import time 
from evaluation.save_result import save_run
from evaluation.build_metrics import build_metrics

def main():
 
    print("[INFO] Costruzione dataset...")

    dataset = build_dataset(n_per_class=100, seed=42)

    print(f"[INFO] Dimensione dataset: {len(dataset)}") 

    # 2. recupero esempi few-shot
    ex_nd, ex_clone, ex_diff = get_few_shot_examples(dataset) 

    # 3. inizializzazione prompt
    prompt_strategy = FewShotPrompt(ex_nd, ex_clone, ex_diff) 

    # 4. inizializzazione LLM
    llm = OllamaClient(model="llama3") 

    start = time.time()

    # 5. esecuzione test 
    results = run_experiment_p(dataset, prompt_strategy, llm, max_workers=4) 

    end = time.time()

    #separazione risultati 
    valid_results = [r for r in results if r["prediction"] != "UNKNOWN"] # valid_results contiene solo predizioni valide (esclude UNKNOWN)

    #calcolo metriche
    metrics = build_metrics(valid_results)

    #salvataggio risultati
    save_run(metrics,"results")

    print(f"\n[INFO] Tempo totale: {end - start:.2f} sec")
    print(f"[INFO] Tempo medio: {(end - start) / len(dataset):.2f} sec") 


if __name__ == "__main__":
    main()  



