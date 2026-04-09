from preprocessing.dataset_builder import build_dataset
from prompting.utils import get_few_shot_examples
from prompting.builder_prompt_few_shot import FewShotPrompt 
from prompting.builder_prompt_zero_shot import ZeroShotPrompt
from llm.Ollamaclient import OllamaClient 
from llm.runner import run_experiment 
from llm.runnerParallel.runnerP import run_experiment_p
import time 
from evaluation.save_result import save_run
from evaluation.build_metrics import build_metrics 
from utils.menu import choose_strategy

def main():
 
    print("[INFO] Costruzione dataset...")

    dataset = build_dataset(n_per_class=100, seed=42)

    print(f"[INFO] Dimensione dataset: {len(dataset)}") 

    choise = choose_strategy()  

    match choise:
      case "1":
          prompt_strategy = ZeroShotPrompt() 
          
      case "2":
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

    #calcolo metriche
    metrics = build_metrics(results,prompt_strategy)

    #salvataggio risultati
    save_run(metrics,"results")

    print(f"\n[INFO] Tempo totale: {end - start:.2f} sec")
    print(f"[INFO] Tempo medio: {(end - start) / len(dataset):.2f} sec") 


if __name__ == "__main__":
    main()  



