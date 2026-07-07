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

def get_output_directory(app, sas):

    log_file = os.path.join(
        "logs",
        f"{app['name']}-{sas}.log"
    )

    with open(log_file, "r", encoding="utf-8",errors="ignore") as f:

        for line in f:

            if line.startswith("OUTPUT_DIRECTORY="):

                return line.strip().split("=", 1)[1]

    raise Exception(
        f"Output directory not found for "
        f"{app['name']} - {sas}"
    )


def run_generated_tests(output_directory, app):

    test_directory = os.path.abspath(
        os.path.join(
            SEMANTIC_CRAWLER_PATH,
            output_directory,
            "localhost",
            "crawl0"
        )
    )

    if not os.path.exists(test_directory):
        raise Exception(
            f"Directory not found: {test_directory}"
        )

    result = subprocess.run(
        [
            "cmd",
            "/c",
            "mvn",
            "test",
            f"-Dcrawljax.test.username={app['username']}",
            f"-Dcrawljax.test.password={app['password']}"
        ],
        cwd=test_directory
    )

    return result.returncode


def reset_coverage(app):

    subprocess.run(
        [
            "docker",
            "exec",
            app["container_name"],
            "rm",
            "-f",
            app["coverage_file"]
        ],
        check=False
    )


def export_coverage(app):

    result = subprocess.run(
        [
            "docker",
            "exec",
            app["container_name"],
            "php",
            app["coverage_export"]
        ],
        capture_output=True,
        text=True
    )

    return result.stdout.strip()


def save_coverage(output_directory, coverage):

    coverage_file = os.path.join(
        SEMANTIC_CRAWLER_PATH,
        output_directory,
        "coverage.txt"
    )

    with open(
        coverage_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(str(coverage))




def main():

    fastapi_process = start_fastapi()

    try:

        for app in APPS:

            for sas in SAS_LIST:

                try:

                    print(
                        f"\n[INFO] Preparing clean environment "
                        f"for crawl {app['name']} - {sas}"
                    )

                    start_app(app)

                    print(
                        f"[INFO] Starting coverage collection "
                        f"for crawl {app['name']} - {sas}"
                    )

                    reset_coverage(app)

                    run_crawl(app, sas)

                    output_directory = get_output_directory(
                        app,
                        sas
                    )

                    print(
                        f"[INFO] Resetting {app['name']} "
                        f"before running generated tests"
                    )

                    start_app(app)

                    print(
                        f"[INFO] Starting coverage collection "
                        f"for generated tests {app['name']} - {sas}"
                    )

                    reset_coverage(app)

                    test_result = run_generated_tests(
                        output_directory,  
                        app
                    )

                    print(
                        f"[INFO] Maven test exit code: "
                        f"{test_result}"
                    )

                    coverage = export_coverage(app)

                    save_coverage(
                        output_directory,
                        coverage
                    )

                    print(
                        f"[INFO] Coverage "
                        f"{app['name']} - {sas}: "
                        f"{coverage}%"
                    )

                finally:

                    stop_app(app)

    finally:

        stop_fastapi(fastapi_process)


if __name__ == "__main__":

    main() 