

def collapse_labels(rows):
    collapsed_rows = []

    for row in rows:

        # converto Row -> dict
        row_dict = dict(row)

        # clone + near => 0
        if row_dict["HUMAN_CLASSIFICATION"] in [0, 1]:
            row_dict["label"] = 0
        else:
            row_dict["label"] = 2

        collapsed_rows.append(row_dict)

    return collapsed_rows