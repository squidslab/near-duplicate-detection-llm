from pathlib import Path

BASE_HTML_DIR = Path(__file__).resolve().parent.parent / "data" / "GroundTruthModels"

def get_html(appName: str,crawl:str,state: str) -> str | None: 

    appName = appName.strip()
    crawl = crawl.strip()
    state = state.strip()

    file_path = BASE_HTML_DIR / appName / crawl / "doms" / f"{state}.html" 

    if not file_path.exists(): #verifico se file viene trovato 
        print(f"[WARNING] Missing: {appName}/{crawl}/doms/{state}.html")
        return None

    try:
        return file_path.read_text(encoding="utf-8", errors="ignore") #ritorno html 
    except Exception as e: #in caso di errore interrompo 
        print(f"[ERROR] Errore lettura {file_path}: {e}")
        return None 