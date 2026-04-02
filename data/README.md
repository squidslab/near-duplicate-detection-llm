## Dataset Setup

This project relies on data derived from the NDStudy dataset.

the dataset is not included in this repository.
Please follow the steps below to correctly set up the dataset.

---

### 1. Download Required Files

Download the following resources:

* **SS dataset (database):**
  https://doi.org/10.5281/zenodo.3376730

* **Crawls (HTML data):**
  https://doi.org/10.5281/zenodo.3385377

---

### 2. Extract the Files

* Extract the archive `Crawls_complete.7z`
* Inside the extracted content, locate the folder:

```
GroundTruthModels/
```

---

### 3. Prepare the Data Folder

Move the following elements into the `data/` directory of this project:

* The file:

```
ss.db
```

* The folder:

```
GroundTruthModels/
```

---

### 4. Generate the Final Dataset 

Run the following command to create the final dataset used in the experiments: 

```
python prepare_dataset.py
```


---

### 5. Final Structure

After setup, your `data/` directory should look like this:

```
data/
├── ss.db
├── dataset.db
├── GroundTruthModels/
```

---

### Notes

* This project uses data derived from the NDStudy dataset.
* Make sure the folder names are not modified, as they are required by the data processing scripts.
