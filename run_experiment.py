from llm.Ollamaclient import OllamaClient
from preprocessing.dataset_builder import build_dataset
from preprocessing.builder.dataset_builder_extr import dataset_builder_for_extraction
from prompting.utils import get_few_shot_examples
from prompting.classification.builder_prompt_few_shot import FewShotPrompt 
from prompting.classification.builder_prompt_zero_shot import ZeroShotPrompt
from prompting.classification.builder_prompt_zero_shot_extraction import ZeroShotPromptExtr
from prompting.functionality_extraction.builder_prompt_zero_shot_functionality_extraction import ZeroShotPromptForFunctionalityExtraction
from llm.runnerParallel.runnerP import run_experiment_p
import time 
from evaluation.save_result import save_run
from evaluation.build_metrics import build_metrics 
from utils.menu import choose_strategy, choose_input_type

MODEL="qwen2.5:7b"

def debug_dataset_to_file(dataset, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for i, item in enumerate(dataset):
            f.write(f"===== ITEM {i} =====\n")
            f.write(f"LABEL: {item['label']}\n\n")

            if "input1" in item:
                f.write("PAGE 1:\n")
                f.write(item["input1"] + "\n\n")

            if "input2" in item:
                f.write("PAGE 2:\n")
                f.write(item["input2"] + "\n\n")

            f.write("="*50 + "\n\n")


def main():

    choice = choose_input_type()

    if choice == "html":
        input_type = "html"
    elif choice == "image":
        input_type = "image"
    elif choice == "extraction":
        input_type = "html"
    else:
        print("[WARNING] Invalid choice, defaulting to HTML")
        input_type = "html"

    llm_classification = OllamaClient(MODEL) 
    llm_extraction = OllamaClient(MODEL)

    print("[INFO] Costruzione dataset test...")  

    dataset = build_dataset(
        tot_experiment=1000,
        seed=42,
        db_path="data/test.db",
        input_type=input_type, 
        example=False  
    )

    print(f"[INFO] Dimensione dataset: {len(dataset)}") 
 

    choice = choose_strategy()

    if choice == "1": # zero shot classification 

        prompt_strategy = ZeroShotPrompt(input_type=input_type, model=MODEL)

        start = time.time()

        results = run_experiment_p(
            dataset,
            prompt_strategy,
            llm_classification,
            max_workers=12,
            task="classification"
        )

        end = time.time()

    elif choice == "2":  # few shot classification 

        print("[INFO] Costruzione dataset esempi...")            

        example_data = build_dataset(
            tot_experiment=6,
            seed=10,
            db_path="data/examples.db",
            input_type=input_type, 
            example=True
        ) 

        ex_nd, ex_clone, ex_diff = get_few_shot_examples(example_data) 

        prompt_strategy = FewShotPrompt(
            ex_nd, ex_clone, ex_diff,
            input_type=input_type,
            model=MODEL
        )

        start = time.time()

        results = run_experiment_p(
            dataset,
            prompt_strategy,
            llm_classification,
            max_workers=12,
            task="classification"
        )

        end = time.time()


    elif choice == "3": # functionality extraction + classification 

        print("[INFO] Running functionality extraction...")

        extraction_strategy = ZeroShotPromptForFunctionalityExtraction(input_type="html")

        start = time.time()

        extraction_results = run_experiment_p(
            dataset,
            extraction_strategy,
            llm_extraction,
            max_workers=12,
            task="extraction"
        )

        new_dataset = dataset_builder_for_extraction(extraction_results, dataset)

        # DEBUG DATASET DOPO EXTRACTION (già presente ma reso uniforme)
        debug_dataset_to_file(new_dataset, "debug_extraction_output.txt")

        print(f"[INFO] Dimensione newdataset: {len(new_dataset)}")                 

        print("[INFO] Running classification on extracted descriptions...")

        classification_strategy = ZeroShotPromptExtr(input_type="html", model=MODEL)

        results = run_experiment_p(
            new_dataset,
            classification_strategy,
            llm_classification,
            max_workers=12,
            task="classification"
        )

        with open("debug_classification_output.txt", "w", encoding="utf-8") as f:
            for i, r in enumerate(results):
                f.write(f"===== ITEM {i} =====\n")
                f.write(f"TRUE LABEL: {r['label']}\n")
                f.write(f"PREDICTION: {r['prediction']}\n\n")
                f.write("RAW OUTPUT:\n")
                f.write(r["raw_output"] + "\n\n")
                f.write("="*50 + "\n\n")

        end = time.time()

    else:
        raise ValueError("Invalid strategy choice")

    print(f"\n[INFO] Tempo totale: {end - start:.2f} sec")
    print(f"[INFO] Tempo medio: {(end - start) / len(dataset):.2f} sec") 

    if choice == "3":
        final_strategy = classification_strategy
    else:
        final_strategy = prompt_strategy

    metrics = build_metrics(results, final_strategy)
    save_run(metrics)


if __name__ == "__main__":
    main()