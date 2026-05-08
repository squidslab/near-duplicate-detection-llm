import re


def dataset_builder_for_extraction(extraction_results,dataset): 
        new_dataset = []

        for i, res in enumerate(extraction_results):

            raw_output = res["description"]

            try:
                page1_match = re.search(r"PAGE 1:(.*?)(PAGE 2:|$)", raw_output, re.DOTALL | re.IGNORECASE)
                page2_match = re.search(r"PAGE 2:(.*)", raw_output, re.DOTALL | re.IGNORECASE)

                page1_text = page1_match.group(1).strip() if page1_match else ""
                page2_text = page2_match.group(1).strip() if page2_match else ""

            except Exception:
                page1_text = ""
                page2_text = ""

            new_dataset.append({
                "input1": page1_text,
                "input2": page2_text,
                "label": dataset[i]["label"]
            })

        return new_dataset