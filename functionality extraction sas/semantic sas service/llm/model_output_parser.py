def clean_output(output):
    if output is None:
        return "INVALID"

    output = output.upper().strip()

    if "DISTINCT" in output:
        return "DISTINCT"
    if "CLONE" in output:
        return "CLONE"

    return "INVALID" 