import sqlite3


#funzione che crea connessione con test.db e example.db
def get_connection(db_path):
    return sqlite3.connect(db_path)


def load_all_pairs(db_path): #carico intero db 
    try:
        with get_connection(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT crawl, state1, state2, label, app_name, id
                FROM dataset_pairs
            """)

            result = cursor.fetchall()

            print(f"[INFO] Totale righe caricate: {len(result)}")

            return result

    except sqlite3.Error as e:
        print("Errore SQLite:", e)
        return []

       
    
