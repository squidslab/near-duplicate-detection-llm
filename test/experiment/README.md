# Experimental Pipeline

This folder contains the experimental pipeline used to evaluate the semantic State Abstraction Function (SAS).

The experiments are based on local Large Language Models (LLMs) and are used to evaluate the semantic classification of web application states.

---

# Dataset Setup

The datasets used during the experiments are not included in this repository.

To correctly configure the datasets, follow the instructions available in:

```
dataset/README.md
```

---

# Experimental Pipeline Structure

The experimental pipeline includes:

- dataset generation scripts
- experiment execution scripts
- prompt definitions
- functionality extraction pipeline
- semantic classification pipeline
- metrics computation

---

# Running the Experiments

To execute the main experimental pipeline:

```
python run_experiment.py
```

---

# Notes

- Make sure Ollama is running before executing the experiments.
- Ensure that the datasets are correctly configured before running the pipeline.
- The experiments use local LLMs executed through Ollama.
- The generated datasets are based on the NDStudy dataset.