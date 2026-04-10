from collections import Counter
import random
from data_access.db import get_dataset_pairs_by_label, get_pairs_by_label

VALID_LABELS = [0, 1, 2] 
NAME_APPS = ["addressbook","petclinic","claroline","dimeshift","mrbs","phoenix","ppma", "mantisbt","pagekit"]

def get_stratified_sample(n_per_class=50): #funzione per stratificazione su test.db 

    if not isinstance(n_per_class, int) or n_per_class <= 0: #controllo che parametro sia int e maggiore di 0
        raise ValueError("n_per_class deve essere un intero positivo")

    dataset = []

    for name in NAME_APPS:
     for label in VALID_LABELS:
        rows = get_pairs_by_label(n_per_class, label, name, offset=0)

        if len(rows) == 0: #controllo che per label corrente ci siano dati, se non ci sono non prende nulla 
          print(f"[WARNING] Skip app {name}, label {label}")
          continue
        
        #caso in cui per una determinata app non ci sono dati sufficienti 
        # se dati < 50 allora prende massimo disponibile per label, altrimetni se dati > 50 prende massimo 50 
        actual_n = min(len(rows), n_per_class)
        rows = rows[:actual_n]
 
        dataset.extend(rows)

    return dataset 


def get_examples_sample(n_per_class, test_dataset):  #funzione per stratificazione su example.db 

    dataset = []

    #chiavi da escludere
    test_keys = set(
        (d["crawl"], d["state1"], d["state2"])
        for d in test_dataset
    )

    for name in NAME_APPS:
        for label in VALID_LABELS:

            rows = get_pairs_by_label(n_per_class *5, label, name, offset=n_per_class)

            if len(rows) == 0:
                print(f"[WARNING] Skip app {name}, label {label}")
                continue

            filtered = []

            for row in rows:
                key = (row["crawl"], row["state1"], row["state2"])

                if key not in test_keys:
                    filtered.append(row)

                if len(filtered) == n_per_class:
                    break

            dataset.extend(filtered)

    return dataset


def get_stratified_sample_for_experiment(n_per_class=50, seed=42): #funzione stratificazione dataset finale 
    dataset = []
    NAME_APPS = ["addressbook", "petclinic", "claroline", "dimeshift", "mrbs", "phoenix", "ppma", "mantisbt", "pagekit"]

    num_apps = len(NAME_APPS)

    for label in [0, 1, 2]:

        per_app_quota = n_per_class // num_apps
        remainder = n_per_class % num_apps

        for i, name in enumerate(NAME_APPS):

            rows = get_dataset_pairs_by_label(label, name)

            if len(rows) == 0:
                continue

            random.seed(seed + label + i)
            random.shuffle(rows)

            extra = 1 if i < remainder else 0
            k = min(per_app_quota + extra, len(rows))

            selected = rows[:k]
            dataset.extend(selected)

    # completamento classi mancanti
    label_counts = Counter([d["label"] for d in dataset])

    for label in [0, 1, 2]:
        missing = n_per_class - label_counts[label]

        if missing > 0:
            all_rows = []
            for name in NAME_APPS:
                rows = get_dataset_pairs_by_label(label, name)
                all_rows.extend(rows)

            random.seed(seed + label + 999)
            random.shuffle(all_rows)

            #controllo duplicati con ID
            existing_ids = set(d["id"] for d in dataset)

            new_samples = []

            for row in all_rows:
                if row["id"] not in existing_ids:
                    new_samples.append(row)
                    existing_ids.add(row["id"])

                if len(new_samples) == missing:
                    break

            dataset.extend(new_samples)

    random.seed(seed)
    random.shuffle(dataset)

    return dataset