import os
from data_access.sampler import get_stratified_sample, get_examples_sample
from data_access.db import create_test_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    print("[INFO] Avvio costruzione dataset...")

    #TEST DATASET
    test_dataset = get_stratified_sample(50)

    #EXAMPLES DATASET (senza overlap)
    examples_dataset = get_examples_sample(10, test_dataset)

    #PATH DB
    test_db_path = os.path.normpath(os.path.join(BASE_DIR, "data", "test.db"))
    examples_db_path = os.path.normpath(os.path.join(BASE_DIR, "data", "examples.db"))

    #CREAZIONE DB
    create_test_db(test_db_path, test_dataset)
    create_test_db(examples_db_path, examples_dataset)

    print("[INFO] Database creati con successo!")

if __name__ == "__main__":
    main()