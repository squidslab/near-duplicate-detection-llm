# Near-Duplicate Detection with LLMs

## Prerequisites

Before running the project, make sure you have the following installed:

* Python 3.x
* Ollama
* qwen2.5 (model 7b)

To install the model using Ollama:

```
ollama pull qwen2.5:7b
```

---

## Dataset

The dataset is not included in this repository.

To properly set it up, follow the instructions available in:

```
data/README.md
```

---

## Running the Project

To execute the main script, run the following command from the terminal:

``` 
python run_experiment.py
```

---

## Notes

* Make sure Ollama is running before executing the script.
* Ensure the dataset is correctly configured inside the `data/` folder.
