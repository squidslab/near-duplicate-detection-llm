# General Project Description

# Large Language Model-based Near Duplicate Detection for Web Application Testing

This project investigates whether a local Large Language Model (LLM) can identify functional equivalence between web application states during crawling and testing.

It uses `qwen2.5:7b` through Ollama and compares three prompting strategies: zero-shot, few-shot, and Functionality Extraction.

## How It Works

The classification task is binary. In the original NDStudy dataset, `CLONE` and `NEAR-DUPLICATE` are separate labels. In this project, they are grouped into a single functional-equivalence category, represented internally as `CLONE`. `DISTINCT` indicates a meaningful functional difference.

Zero-shot and few-shot classify preprocessed HTML directly. Functionality Extraction uses two LLM calls:

1. The model analyzes each page and extracts its main action, secondary actions, and goal.
2. The model compares those descriptions and classifies the pair as `CLONE` or `DISTINCT`.

Functionality Extraction is integrated into Crawljax as a custom state abstraction strategy through a Python service built with FastAPI. During crawling, Crawljax treats a `CLONE` result as an equivalent state; a `DISTINCT` result means the states remain separate.

## Evaluation

The offline evaluation uses 5,000 pairs from NDStudy. Functionality Extraction achieved 76.08% accuracy and an F1-score of 0.7600.

The Crawljax integration was compared with the Basic and DHash strategies on the AddressBook and PPMA applications. The evaluation considered graph redundancy, functional coverage, and the line coverage of the generated tests.

Functionality Extraction reduced graph redundancy in both applications. Its coverage results varied by application: it achieved the highest line coverage on PPMA, while Basic achieved the highest line coverage on AddressBook.

## Prerequisites

For the offline experiments and semantic service:

- Python 3.x
- Ollama
- The `qwen2.5:7b` model

For the end-to-end Crawljax experiments:

- Java 17
- Maven
- Docker
- Google Chrome

The thesis experiments used Python 3.13.12, Ollama 0.33.3, Java Temurin 17.0.18, Maven 3.9.15, Docker 29.3.1, and Crawljax 5.2.4-SNAPSHOT.

The Python components use FastAPI, Uvicorn, requests, Beautiful Soup, lxml, and scikit-learn.

Install the model with Ollama:

```bash
ollama pull qwen2.5:7b
```

## Project Structure

### `test/`

Contains the dataset preparation and offline experiment pipelines, including scripts for sampling the data, running the prompting strategies, and calculating classification metrics.

### `functionality_extraction_sas/`

Contains the semantic service and Crawljax integration. The Python service preprocesses page content, extracts functionality, and classifies states. The Java crawler uses the result when building the application graph.

### `crawljax_automation/`

Contains the end-to-end experiment orchestration, benchmark applications, logs, and scripts for running crawls and evaluating generated tests.
