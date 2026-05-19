import requests


with open(
    "../experiment/data/GroundTruthModels/claroline/crawl-claroline-60min/states/state2.html",
    "r",
    encoding="utf-8"
) as f:
    dom1 = f.read()


with open(
    "../experiment/data/GroundTruthModels/claroline/crawl-claroline-60min/states/state4.html",
    "r",
    encoding="utf-8"
) as f:
    dom2 = f.read()


response = requests.post(
    "http://127.0.0.1:8000/compare",
    json={
        "dom1": dom1,
        "dom2": dom2
    }
)


result = response.json()

print(result) 