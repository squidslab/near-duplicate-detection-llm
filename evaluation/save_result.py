import json
import os
from evaluation.build_metrics import plot_confusion_matrix


def get_next_run_id(folder):
    if not os.path.exists(folder):
        return 1

    run_dirs = [
        d for d in os.listdir(folder)
        if d.startswith("run_") and os.path.isdir(os.path.join(folder, d))
    ]

    if not run_dirs:
        return 1

    ids = []
    for d in run_dirs:
        try:
            num = int(d.replace("run_", ""))
            ids.append(num)
        except:
            continue

    return max(ids) + 1


def save_run(metrics, folder="results"):
    os.makedirs(folder, exist_ok=True)

    run_id = get_next_run_id(folder)

    run_folder = os.path.join(folder, f"run_{run_id}")
    os.makedirs(run_folder, exist_ok=True)

    json_filename = os.path.join(run_folder, f"run_{run_id}.json")

    #copia senza confusion matrix
    metrics_to_save = metrics.copy()
    if "confusion_matrix" in metrics_to_save:
        cm = metrics_to_save.pop("confusion_matrix")
    else:
        cm = None

    with open(json_filename, "w") as f:
        json.dump(metrics_to_save, f, indent=4)

    #salva grafico separato
    if cm is not None:
        confusion_path = os.path.join(run_folder, "confusion_matrix.png")

        labels = ["CLONE", "NEAR-DUPLICATE", "DISTINCT"]

        plot_confusion_matrix(cm, labels, save_path=confusion_path)

    print(f"[INFO] Run {run_id} salvata in: {run_folder}")