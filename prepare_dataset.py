import os
from data_access.sampler import get_stratified_sample
from data_access.db import create_dataset_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    print("[INFO] Avvio costruzione dataset...")

    # 1️ sampling
    dataset = get_stratified_sample(50)

    print(f"[INFO] Coppie totali: {len(dataset)}")

    # path output
    output_db = os.path.join(BASE_DIR, "data", "dataset.db")
    output_db = os.path.normpath(output_db)

    # creazione DB
    create_dataset_db(output_db, dataset)

    print("[INFO] Dataset creato con successo!")

# entry point
if __name__ == "__main__":
    main()