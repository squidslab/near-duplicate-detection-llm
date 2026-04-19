from llm.Ollamaclient import OllamaClient
from preprocessing.dataset_builder import build_dataset
from prompting.utils import get_few_shot_examples
from prompting.classification.builder_prompt_few_shot import FewShotPrompt 
from prompting.classification.builder_prompt_zero_shot import ZeroShotPrompt
from prompting.functionality_extraction.builder_prompt_few_shot_functionality_extraction import ZeroShotPromptForFunctionalityExtraction
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

    elif choice == "extraction":    
        input_type = "html"
        llm = OllamaClient(model="qwen2.5:7b")    

    else:
        print("[WARNING] Invalid choice, defaulting to HTML")
        input_type = "html"
        llm = OllamaClient(model="llama3")

    print("[INFO] Costruzione dataset test...")  

    dataset = build_dataset(
        tot_experiment=300,
        seed=42,
        db_path="data/test.db",
        input_type=input_type, 
        example = False  
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
                tot_experiment=6,
                seed=10,
                db_path="data/examples.db",
                input_type=input_type, 
                example= True
            ) 

            ex_nd, ex_clone, ex_diff = get_few_shot_examples(example_data) 


            prompt_strategy = FewShotPrompt(
                ex_nd, ex_clone, ex_diff,
                input_type=input_type
            )
        case "3":
            prompt_strategy = ZeroShotPromptForFunctionalityExtraction(input_type=input_type)    
            start = time.time()

            results = run_experiment_p(dataset, prompt_strategy, llm, max_workers=6,task="extraction") 

            with open("output.txt", "w", encoding="utf-8") as f:
             for i, r in enumerate(results):
               f.write("=" * 50 + "\n")
               f.write(f"[ITEM {i}]\n")
               f.write(f"LABEL: {r['label']}\n")
               f.write("-" * 50 + "\n")
               f.write(f"{r['description']}\n\n")
  
            end = time.time()




    print(f"\n[INFO] Tempo totale: {end - start:.2f} sec")
    print(f"[INFO] Tempo medio: {(end - start) / len(dataset):.2f} sec")


if __name__ == "__main__":
    main()
