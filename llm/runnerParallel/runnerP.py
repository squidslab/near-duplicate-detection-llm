from concurrent.futures import ThreadPoolExecutor, as_completed

from llm.utils import clean_output

    
def process_item(data, prompt_strategy, llm_client):

    # 1. costruzione prompt
    if prompt_strategy.uses_images():
      prompt = prompt_strategy.build(None, None)
    else:
      prompt = prompt_strategy.build(data["input1"], data["input2"])

    # 2. chiamata LLM
    if prompt_strategy.uses_images():
        raw_output = llm_client.generate({
            "image1": data["input1"],
            "image2": data["input2"],
            "text": prompt
        })
    else:
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