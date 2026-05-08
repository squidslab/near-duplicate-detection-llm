import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(BASE_DIR, "..", "data", "SS.db")
db_path = os.path.normpath(db_path)

def get_connection_ss_db():
    return sqlite3.connect(db_path) 


def load_all_pairs(): #carico intero db 
    try:
        with get_connection_ss_db() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    n.crawl,
                    n.state1,
                    n.state2,
                    n.human_classification,
                    a.name AS app_name
                FROM nearduplicates n
                JOIN apps a ON n.crawl = a.crawl
            """)

            result = cursor.fetchall()

            print(f"[INFO] Totale righe caricate: {len(result)}")

            return result

    except sqlite3.Error as e:
        print("Errore SQLite:", e)
        return []


def create_test_db(output_path, data): #crea test e example db  
    try:
        # se esiste già lo eliminiamo (dataset sempre pulito)
        with sqlite3.connect(output_path) as conn:
            cursor = conn.cursor()

            cursor.execute("DROP TABLE IF EXISTS dataset_pairs")

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

           #supporto sia dict che tuple/Row
            rows_to_insert = [
                (
                    row["crawl"],
                    row["state1"],
                    row["state2"],
                    row["label"],
                    row["app_name"]
                ) if isinstance(row, dict) else row
                for row in data
            ]

            cursor.executemany("""
                INSERT INTO dataset_pairs (crawl, state1, state2, label, app_name)
                VALUES (?, ?, ?, ?, ?)
            """, rows_to_insert)

            conn.commit()

        print(f"[INFO] database test creato in: {output_path}")
        print(f"[INFO] Totale righe: {len(data)}")

    except sqlite3.Error as e:
        print("Errore creazione database test:", e)