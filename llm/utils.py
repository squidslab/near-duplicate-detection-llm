def clean_output(output):
    if output is None:
        return "UNKNOWN"

    output = output.upper()

    if "CLONE" in output:
        return "CLONE"
    if "NEAR-DUPLICATE" in output:
        return "NEAR-DUPLICATE"
    if "DISTINCT" in output:
        return "DISTINCT"

    return "UNKNOWN"