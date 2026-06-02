import threading

from preprocessing.builder.build_extraction_result import build_extraction_result

debug_lock = threading.Lock()


def debug_extraction_to_file(
        dom1,
        dom2,
        prompt,
        raw_output,
        extraction):

    with debug_lock:

        with open(
                "debug_functionality_extraction.txt",
                "a",
                encoding="utf-8") as f:

            f.write("=====================================\n")

            f.write("FUNCTIONALITY EXTRACTION\n\n")


            f.write("RAW OUTPUT:\n")
            f.write(str(raw_output) + "\n\n")

            f.write("EXTRACTION RESULT:\n")
            f.write(str(extraction) + "\n\n")

            f.write("=====================================\n\n")


def extract_functionality(dom1,dom2,extraction_prompt,llm_client):

    prompt = extraction_prompt.build(dom1, dom2)

    raw_output = llm_client.generate(prompt)

    extraction = build_extraction_result(raw_output)

    debug_extraction_to_file(
        dom1,
        dom2,
        prompt,
        raw_output,
        extraction
    )

    return extraction