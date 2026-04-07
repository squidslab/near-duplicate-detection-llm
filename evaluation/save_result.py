import json
import os

def get_next_run_id(folder):
    if not os.path.exists(folder):
        return 1

    files = [f for f in os.listdir(folder) if f.startswith("run_") and f.endswith(".json")]

    if not files:
        return 1

    ids = []
    for f in files:
        try:
            num = int(f.replace("run_", "").replace(".json", ""))
            ids.append(num)
        except:
            continue

    return max(ids) + 1


def save_run(metrics, folder="results"):
    os.makedirs(folder, exist_ok=True)

    run_id = get_next_run_id(folder)

    filename = f"{folder}/run_{run_id}.json"

    with open(filename, "w") as f:
        json.dump(metrics, f, indent=4)

    print(f"[INFO] Run {run_id} salvata in: {filename}")