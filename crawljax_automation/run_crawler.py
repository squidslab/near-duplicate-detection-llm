import subprocess
import time
import os
import requests

from config import APPS, SAS_LIST


FASTAPI_PATH = "../functionality_extraction_sas/semantic sas service" 

SEMANTIC_CRAWLER_PATH = (
    "../functionality_extraction_sas/semantic-crawler"
)


def wait_until_online(url, timeout=120): #funzione che attende che un app sia online 

    print(f"[INFO] Waiting for {url}")

    start = time.time()

    while time.time() - start < timeout: #controlla continuamente che app è online 

        try:

            response = requests.get(url, timeout=5) #invia richiesta http per verificare se app è online 

            if response.status_code < 500: 

                print(f"[INFO] {url} is online")

                return True

        except Exception: #se connessione fallisce ignora errore e riprova 
            pass

        time.sleep(2)

    return False


def start_app(app): #funzione per avviare applicazione 

    print(f"\n[INFO] Starting {app['name']}")

    subprocess.run( #pulisce evntuali container gia esistenti 
        ["docker", "compose", "down","-v"],
        cwd=app["docker_path"],
        check=False
    )

    subprocess.run( #esegue docker 
        ["docker", "compose", "up", "-d"],
        cwd=app["docker_path"],
        check=True
    )

    if not wait_until_online(app["url"]): #verifica se app online 

        raise Exception(
            f"{app['name']} did not start"
        )


def stop_app(app): #ferma container docker app 

    print(f"[INFO] Stopping {app['name']}")

    subprocess.run(
        ["docker", "compose", "down"],
        cwd=app["docker_path"]
    )


def start_fastapi(): #avvia server python della sas 

    print("[INFO] Starting FastAPI SAS server")

    process = subprocess.Popen(
        [
            "uvicorn",
            "api.server:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8000"
        ],
        cwd=FASTAPI_PATH
    )

    time.sleep(5)

    return process


def stop_fastapi(process):

    print("[INFO] Stopping FastAPI server")

    process.terminate()


def run_crawl(app, sas):

    print(
        f"[INFO] Running crawl "
        f"{app['name']} - {sas}"
    )

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(
        log_dir,
        f"{app['name']}-{sas}.log"
    )

    cmd = [
        "java",
        "-jar",
        "target/semantic-crawler-1.0-SNAPSHOT-jar-with-dependencies.jar",

        app["name"],
        sas,
        app["url"],
        app["username"],
        app["password"]
    ]

    with open(log_file, "w", encoding="utf-8") as f:

        result = subprocess.run(
            cmd,
            cwd=SEMANTIC_CRAWLER_PATH,
            stdout=f,
            stderr=subprocess.STDOUT,
            text=True
        )

    print(result.returncode)

def main():

    fastapi_process = start_fastapi() #avvia il server 

    try:

        for app in APPS: 

            try:

                start_app(app) #avvia app 

                for sas in SAS_LIST:

                    run_crawl(app, sas) #esegue sulla singola app le 3 sas 

            finally:

                stop_app(app) #eseguite le 3 sas chiude l'app 

    finally:

        stop_fastapi(fastapi_process) #chiude server 


if __name__ == "__main__":

    main()