# Dataset Setup

This project relies on data derived from the NDStudy dataset.

The dataset is not included in this repository.  
Please follow the steps below to correctly configure the required resources.

---

# 1. Download Required Resources

Download the following resources:

## SS Dataset (Database)

https://doi.org/10.5281/zenodo.3376730

## Crawls (HTML Data)

https://doi.org/10.5281/zenodo.3385377

---

# 2. Extract the Crawls Archive

Extract the archive:

```
Crawls_complete.7z
```

Inside the extracted content, locate the folder:

```
GroundTruthModels/
```

---

# 3. Prepare the `data/` Directories

## `data/` Directory of This Script

Move the file:

```
ss.db
```

into the `data/` directory used by this script.

---

## `data/` Directory of the `experiment` Script

Move the folder:

```
GroundTruthModels/
```

into the `data/` directory used by the `experiment` script.

---

# 4. Generate the Experimental Datasets

Run the following command to generate the datasets used during the experiments:

```
python prepare_dataset.py
```

The script automatically generates two separate databases:

- `test.db`
- `example.db`

---

# 5. Generated Dataset Structure

## `test.db`

Contains the elements used during the testing and evaluation phase of the semantic classification pipeline.

The elements stored in this database are used as the state pairs to classify during the experiments.

---

## `example.db`

Contains the examples used in the few-shot prompts.

The elements stored in this database are used exclusively as support examples provided to the model during classification.

---

## Important Property

The elements contained in `test.db` and `example.db` are completely disjoint.

This guarantees that:
- no example used in few-shot prompting is reused during testing
- no data leakage occurs between the testing phase and the few-shot prompting phase

---

# Notes

- This project uses data derived from the NDStudy dataset.
- File and folder names must not be modified, as they are required by the dataset generation scripts.
- The generated datasets are used by the experimental pipeline located in the `test/` folder.