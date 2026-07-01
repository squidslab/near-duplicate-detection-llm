# General Project Description

This project implements a State Abstraction Function (SAF) based on local Large Language Models (LLMs) for detecting  duplicated states during the crawling of web applications.

The main goal is to reduce the number of redundant states generated during the crawling process by automatically identifying pages that provide the same functionality from the user's perspective, even in the presence of structural or visual differences in the HTML code.

The SAS is integrated with Crawljax and operates by semantically comparing newly discovered states with states already present in the crawler graph. For each pair of HTML pages, a two-stage process is performed:

## Functionality Extraction

HTML pages are preprocessed and analyzed by a local LLM to extract a structured functional description of the page, focused exclusively on:

- actions available to the user
- main goal of the page
- provided functionalities

## Semantic Classification

The extracted functional descriptions are compared through a second classification prompt, which determines whether the two pages represent:

- `CLONE`
- `DISTINCT`

If a newly discovered page is classified as `CLONE` with respect to a state already present in the graph, it is not added to the final crawl graph. Otherwise, the state is considered semantically distinct and is therefore added to the graph.

The entire system uses local LLMs executed through Ollama.

# Prerequisites

Before running the project, make sure the following components are installed:

- Python 3.x
- Ollama
- `qwen2.5:7b`

To install the model using Ollama:

```
ollama pull qwen2.5:7b
```

# Project Structure

## `test/`

This folder contains the experimental pipeline used to evaluate the State Abstraction Function (SAS).

It includes:
- dataset creation scripts
- experiment execution scripts
- prompt definitions
- evaluation utilities
- metrics computation
- debug and analysis tools

The folder is mainly used to perform offline experiments and benchmark the semantic classification pipeline on different datasets and configurations.

---

## `functionlity extraction sas/`

This folder contains the implementation of the State Abstraction Function (SAS) and its runtime integration components.

It includes:
- the FastAPI server
- HTML preprocessing logic
- functionality extraction pipeline
- semantic classification logic
- communication interfaces used during crawling

The SAS operates during the crawling process by semantically comparing newly discovered states with states already present in the crawl graph.
