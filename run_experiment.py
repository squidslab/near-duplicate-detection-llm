from llm.Ollamaclient import OllamaClient
from preprocessing.dataset_builder import build_dataset
from prompting.utils import get_few_shot_examples
from prompting.builder_prompt_few_shot import FewShotPrompt 
from prompting.builder_prompt_zero_shot import ZeroShotPrompt
from llm.runnerParallel.runnerP import run_experiment_p
import time 
from evaluation.save_result import save_run
from evaluation.build_metrics import build_metrics 
from utils.menu import choose_strategy,choose_input_type

def main():

    #1. scelta input
    choice = choose_input_type()

    if choice == "html":
        input_type = "html"
        llm = OllamaClient(model="llama3")

    elif choice == "image":
        input_type = "image"
        llm = OllamaClient(model="llava:7b")

    else:
        print("[WARNING] Invalid choice, defaulting to HTML")
        input_type = "html"
        llm = OllamaClient(model="llama3")

    print("[INFO] Costruzione dataset test...")  
    dataset = build_dataset(
        n_per_class=100,
        seed=42,
        db_path="data/test.db",
        input_type=input_type
    )

    print(f"[INFO] Dimensione dataset: {len(dataset)}") 


    #2. scelta strategia
    choice = choose_strategy()

    match choice:
        case "1":
            prompt_strategy = ZeroShotPrompt(input_type=input_type)

        case "2":
            print("[INFO] Costruzione dataset esempi...")            

            example_data = build_dataset(
                n_per_class=2,
                seed=10,
                db_path="data/examples.db",
                input_type=input_type
            )

            print(example_data[0])

            ex_nd, ex_clone, ex_diff = get_few_shot_examples(example_data)

            prompt_strategy = FewShotPrompt(
                ex_nd, ex_clone, ex_diff,
                input_type=input_type
            )


    start = time.time()

    results = run_experiment_p(dataset, prompt_strategy, llm, max_workers=4)

    end = time.time()

    metrics = build_metrics(results, prompt_strategy)

    save_run(metrics, "results")

    print(f"\n[INFO] Tempo totale: {end - start:.2f} sec")
    print(f"[INFO] Tempo medio: {(end - start) / len(dataset):.2f} sec")


if __name__ == "__main__":
    main()
