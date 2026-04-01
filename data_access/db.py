import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(BASE_DIR, "..", "data", "SS.db")
db_path = os.path.normpath(db_path)

def get_connection():
    return sqlite3.connect(db_path) 


def get_pairs_by_label(num, label):
    if label not in [0, 1, 2]:
        raise ValueError("label deve essere 0 (clone), 1 (near-duplicate), 2 (different)")


    if not isinstance(num, int) or num <= 0: #verifico se num è intero e se maggiore di 0
        raise ValueError("num deve essere un intero positivo")

    try:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
              SELECT 
                n.crawl,
                n.state1,
                n.state2,
                n.human_classification,
                a.name
              FROM nearduplicates n
              JOIN apps a ON n.crawl = a.crawl
              WHERE n.human_classification = ?
              ORDER BY RANDOM()
              LIMIT ?
            """, (label, num))

            result = cursor.fetchall()

            if len(result) == 0: #verifico se dati sono stati prelevati dal db
                print(f"Nessuna riga trovata per label {label}")

            return result

    except sqlite3.Error as e:
        print("Errore SQLite:", e)
        return [] 
    

