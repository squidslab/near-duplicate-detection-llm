
from data_access.db import get_pairs_by_label

VALID_LABELS = [0, 1, 2]

def get_stratified_sample(n_per_class=50):

    if not isinstance(n_per_class, int) or n_per_class <= 0: #controllo che parametro sia int e maggiore di 0
        raise ValueError("n_per_class deve essere un intero positivo")

    dataset = []

    for label in VALID_LABELS:
        rows = get_pairs_by_label(n_per_class, label)

        if len(rows) < n_per_class: #controllo che database abbia abbastanza dati per classe 
            raise ValueError(
                f"Dati insufficienti per label {label}: trovati {len(rows)}"
            )

 
        dict_rows = [dict(row) for row in rows] #trasformo i dati in formato dict
        dataset.extend(dict_rows)

    return dataset 