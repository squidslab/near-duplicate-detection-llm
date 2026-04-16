from evaluation.metrics import compute_metrics
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def build_metrics(results,prompt_strategy):
    
    metrics = compute_metrics(results) #calcolano le metriche 

    for key in ["accuracy", "precision", "recall", "f1"]:
      metrics[key] = round(metrics[key], 4)

    metrics["model"] = "llama3"
    metrics["dataset_size"] = len(results)
    metrics["input_type"] = "raw html"

    metrics.update(prompt_strategy.get_metadata())
    
    return metrics 




def plot_confusion_matrix(cm, labels, save_path=None):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np

    cm = np.array(cm)

    plt.figure(figsize=(6,5))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=labels,
        yticklabels=labels,
        linewidths=0.5
    )

    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.close() 