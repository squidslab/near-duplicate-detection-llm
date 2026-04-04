from concurrent.futures import ThreadPoolExecutor, as_completed

from llm.utils import clean_output

def process_item(data, prompt_strategy, llm_client):
    
    # 1. costruzione prompt
    prompt = prompt_strategy.build(
        data["html1"],
        data["html2"]
    )

    # 2. chiamata LLM
    raw_output = llm_client.generate(prompt)

    # 3. pulizia output
    pred = clean_output(raw_output)

    return {
        "label": data["label"],
        "prediction": pred,
        "raw_output": raw_output
    }


def run_experiment_p(dataset, prompt_strategy, Llm_client, max_workers=4):

    results = [None] * len(dataset)
    print("PROCESSING (parallel)...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:

        futures = {
            executor.submit(process_item, data, prompt_strategy, Llm_client): i
            for i, data in enumerate(dataset)
        }

        for future in as_completed(futures):
            i = futures[future]  

            try:
                result = future.result()
                results[i] = result  
            except Exception as e:
                print("[ERROR]", e)

    return results