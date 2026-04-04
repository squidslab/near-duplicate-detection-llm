from llm.utils import clean_output

def run_experiment(dataset, prompt_strategy, llm_client): #riceve dataset oggetto prompt e oggetto client 
    results = []
    
    print("PROCESSING")
    for i, data in enumerate(dataset):

        # 1. costruzione prompt
        prompt = prompt_strategy.build(
            data["html1"],
            data["html2"]
        )

        # 2. chiamata LLM
        raw_output = llm_client.generate(prompt)

        # 3. pulizia output
        pred = clean_output(raw_output)

        # 4. salva risultato
        results.append({
            "label": data["label"],     # ground truth
            "prediction": pred,         # output pulito
            "raw_output": raw_output    # output originale 
        })

    return results 