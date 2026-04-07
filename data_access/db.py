import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(BASE_DIR, "..", "data", "SS.db")
db_path = os.path.normpath(db_path)

def get_connection():
    return sqlite3.connect(db_path) 


def get_pairs_by_label(num, label,nameApp):
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
              AND a.name = ?             
              ORDER BY n.state1, n.state2
              LIMIT ?
            """, (label, nameApp, num,))

            result = cursor.fetchall()

            if len(result) == 0: #verifico se dati sono stati prelevati dal db
                print(f"Nessuna riga trovata per label {label}")

            return result

    except sqlite3.Error as e:
        print("Errore SQLite:", e)
        return [] 
    

def create_dataset_db(output_path, data):
    try:
        # se esiste già lo eliminiamo (dataset sempre pulito)
        if os.path.exists(output_path):
            os.remove(output_path)

        conn = sqlite3.connect(output_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE dataset_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crawl TEXT,
                state1 INTEGER,
                state2 INTEGER,
                label INTEGER,
                app_name TEXT
            )
        """)

        cursor.executemany("""
            INSERT INTO dataset_pairs (crawl, state1, state2, label, app_name)
            VALUES (?, ?, ?, ?, ?)
        """, data)

        conn.commit()
        conn.close()

        print(f"[INFO] Dataset creato in: {output_path}")
        print(f"[INFO] Totale righe: {len(data)}")

    except sqlite3.Error as e:
        print("Errore creazione dataset:", e) 


#funzione che crea connessione con dataset.db
def get_connection():
    return sqlite3.connect("data/dataset.db")

#funzione che recupera dati da dataset.db
def get_dataset_pairs_by_label(label,app_name):
    try:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT crawl, state1, state2, label, app_name
                FROM dataset_pairs
                WHERE label = ? AND app_name = ?
                ORDER BY id
            """, (label,app_name))

            rows = cursor.fetchall()

            if len(rows) == 0:
                print(f"[WARNING] Nessun dato per label {label}")

            return rows

    except sqlite3.Error as e:
        print("Errore SQLite:", e)
        return []        