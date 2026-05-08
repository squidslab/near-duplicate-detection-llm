from collections import Counter, defaultdict
import random


VALID_LABELS = [0, 1, 2] 
NAME_APPS = ["addressbook","petclinic","claroline","dimeshift","mrbs","phoenix","ppma", "mantisbt","pagekit"]

def get_stratified_sample(rows,n_total=10000,seed=42,exclude_keys=None): # funzione di stratificazione per creazione test.db / examples.db

    if not isinstance(n_total, int) or n_total <= 0:
        raise ValueError("n_total deve essere un intero positivo")

    random.seed(seed)

    dataset = []

    # se non vengono passate chiavi da escludere
    if exclude_keys is None:
        exclude_keys = set()

    # 50% label 0, 50% label 2
    n_per_label = n_total // 2

    # quota base per app
    n_per_app = n_per_label // len(NAME_APPS)

    # resto da distribuire
    remainder = n_per_label % len(NAME_APPS)

    # grouping per app
    grouped = defaultdict(list)

    for row in rows:
        grouped[row["app_name"]].append(row)

    for i, app in enumerate(NAME_APPS):

        app_rows = grouped[app]

        # rimozione elementi già presenti in altri dataset
        filtered_rows = [
            r for r in app_rows
            if (r["crawl"], r["state1"], r["state2"]) not in exclude_keys
        ]

        label0 = [r for r in filtered_rows if r["label"] == 0]
        label2 = [r for r in filtered_rows if r["label"] == 2]

        # distribuzione remainder
        quota = n_per_app

        if i < remainder:
            quota += 1

        # sampling casuale ma deterministico
        take0 = min(len(label0), quota)
        take2 = min(len(label2), quota)

        sampled0 = random.sample(label0, take0)
        sampled2 = random.sample(label2, take2)

        dataset.extend(sampled0)
        dataset.extend(sampled2)

    return dataset