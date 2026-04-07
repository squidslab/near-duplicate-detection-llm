from evaluation.metrics import compute_metrics


def build_metrics(results):
    
    metrics = compute_metrics(results) #calcolano le metriche 

    for key in ["accuracy", "precision", "recall", "f1"]:
      metrics[key] = round(metrics[key], 4)

    metrics["model"] = "llama3"
    metrics["dataset_size"] = len(results)
    metrics["prompt_type"] = "few shot"
    metrics["num_examples_for_prompt"] = 3 
    metrics["input_type"] = "raw html"
    metrics["description"] = "Test with a few-shot prompting strategy, using 3 examples with raw HTML."

    return metrics 