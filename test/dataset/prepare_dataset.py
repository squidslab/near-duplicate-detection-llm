import os
from data_access.sampler import get_stratified_sample
from data_access.db import create_test_db
from data_access.db import load_all_pairs
from data_processing.collaps_label import collapse_labels

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    print("[INFO] Avvio costruzione dataset...")
    
    ss_db = load_all_pairs() 

    ss_db_collaps = collapse_labels(ss_db) 


    #TEST DATASET
    test_dataset = get_stratified_sample(ss_db_collaps,n_total=9000,seed=42)  
  
    #creo chiavi per escludere elementi presenti in test.db da example db 
    test_keys = set(
    (r["crawl"], r["state1"], r["state2"])
    for r in test_dataset
     )

    #EXAMPLES DATASET (senza overlap)
    examples_dataset = get_stratified_sample(ss_db_collaps,n_total=220,seed=32,exclude_keys=test_keys)

    #PATH DB
    test_db_path = os.path.normpath(os.path.join(BASE_DIR, "..", "experiment", "data", "test.db"))
    examples_db_path = os.path.normpath(os.path.join(BASE_DIR, "..", "experiment", "data", "examples.db"))

    #CREAZIONE DB
    create_test_db(test_db_path, test_dataset)
    create_test_db(examples_db_path, examples_dataset)

    print("[INFO] Database creati con successo!")

if __name__ == "__main__":
    main()