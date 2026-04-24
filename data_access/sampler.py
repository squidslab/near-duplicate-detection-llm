from collections import Counter, defaultdict
import random
from data_access.db import get_dataset_pairs_by_label, get_pairs_by_label

VALID_LABELS = [0, 1, 2] 
NAME_APPS = ["addressbook","petclinic","claroline","dimeshift","mrbs","phoenix","ppma", "mantisbt","pagekit"]

def get_stratified_sample(n_per_class=100, near_ratio=0.8):

    if not isinstance(n_per_class, int) or n_per_class <= 0:
        raise ValueError("n_per_class deve essere un intero positivo")

    dataset = []

    for name in NAME_APPS:

        rows_distinct = get_pairs_by_label(n_per_class, 2, name)

        if len(rows_distinct) == 0:
            taken_distinct = 0
        else:
            taken_distinct = min(len(rows_distinct), n_per_class)
            dataset.extend(rows_distinct[:taken_distinct])

        rows_clone = get_pairs_by_label(n_per_class * 2, 0, name)
        rows_near  = get_pairs_by_label(n_per_class * 2, 1, name)

        n_near_target = int(n_per_class * near_ratio)

        take_near = min(len(rows_near), n_near_target)

        remaining = n_per_class - take_near
        take_clone = min(len(rows_clone), remaining)

        if take_clone < remaining:
            deficit = remaining - take_clone
            extra_near = rows_near[take_near:take_near + deficit]
            take_near += len(extra_near)

        selected = rows_near[:take_near] + rows_clone[:take_clone]

        dataset.extend(selected)

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

            rows = get_pairs_by_label(n_per_class *200, label, name, offset=n_per_class)

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


def get_stratified_sample_for_experiment(n_per_class=50, seed=42, db_path=None): #funzione stratificazione dataset example (per costruzione dataset di example) 
    dataset = []
    num_apps = len(NAME_APPS)

    for label in [0, 1, 2]:

        per_app_quota = n_per_class // num_apps
        remainder = n_per_class % num_apps

        for i, name in enumerate(NAME_APPS):

            rows = get_dataset_pairs_by_label(label, name, db_path)

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
                rows = get_dataset_pairs_by_label(label, name, db_path)
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

def get_stratified_sample_for_ex_two_class(tot_experiment=300, seed=42, db_path=None):
    dataset = []

    num_apps = len(NAME_APPS)

    n_distinct = tot_experiment // 2 
    n_label0 = tot_experiment // 2 


    for i, name in enumerate(NAME_APPS):

        rows = get_dataset_pairs_by_label(2, name, db_path)

        if len(rows) == 0:
            continue

        per_app_quota = n_distinct // num_apps
        remainder = n_distinct % num_apps

        random.seed(seed + 2 + i)
        random.shuffle(rows)

        extra = 1 if i < remainder else 0
        k = min(per_app_quota + extra, len(rows))

        selected = rows[:k]
        dataset.extend(selected)

    for i, name in enumerate(NAME_APPS):

        rows = get_dataset_pairs_by_label(0, name, db_path)

        if len(rows) == 0:
            continue

        per_app_quota = n_label0 // num_apps
        remainder = n_label0 % num_apps

        random.seed(seed + 100 + i)
        random.shuffle(rows)

        extra = 1 if i < remainder else 0
        k = min(per_app_quota + extra, len(rows))

        selected = rows[:k]
        dataset.extend(selected)

    random.seed(seed)
    random.shuffle(dataset)

    return dataset
