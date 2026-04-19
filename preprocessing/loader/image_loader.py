from pathlib import Path
import base64


BASE_IMAGE_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "GroundTruthModels"

def get_image(appName: str,crawl:str,state: str) -> str | None: 

    appName = appName.strip()
    crawl = crawl.strip()
    state = state.strip()

    file_path = BASE_IMAGE_DIR / appName / crawl / "screenshots" / f"{state}.png" 

    if not file_path.exists(): #verifico se file viene trovato 
        print(f"[WARNING] Missing: {appName}/{crawl}/screenshots/{state}.png")
        return None

    return str(file_path) 



def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")