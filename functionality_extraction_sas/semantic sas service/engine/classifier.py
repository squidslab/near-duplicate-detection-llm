import threading

from llm.model_output_parser import clean_output

debug_lock = threading.Lock()


def debug_classification_to_file(
        extraction,
        prompt,
        raw_output,
        prediction):

    with debug_lock:

        with open(
                "debug_classification.txt",
                "a",
                encoding="utf-8") as f:

            f.write("=====================================\n")

            f.write("CLASSIFICATION\n\n")

            f.write("EXTRACTION INPUT 1:\n")
            f.write(extraction["input1"] + "\n\n")

            f.write("EXTRACTION INPUT 2:\n")
            f.write(extraction["input2"] + "\n\n")

            f.write("PREDICTION:\n")
            f.write(str(prediction) + "\n\n")

            f.write("=====================================\n\n")


def classify_states(extraction,classification_prompt,llm_client):

    prompt = classification_prompt.build(
        extraction["input1"],
        extraction["input2"]
    )

    raw_output = llm_client.generate(prompt)

    prediction = clean_output(raw_output)

    debug_classification_to_file(
        extraction,
        prompt,
        raw_output,
        prediction
    )

    return {
        "prediction": prediction,
    }