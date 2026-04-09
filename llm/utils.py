def clean_output(output):
    if output is None:
        return "INVALID"

    output = output.upper().strip()

    if "NEAR-DUPLICATE" in output or "NEAR DUPLICATE" in output:
        return "NEAR-DUPLICATE"
    if "DISTINCT" in output:
        return "DISTINCT"
    if "CLONE" in output:
        return "CLONE"

    return "INVALID" 