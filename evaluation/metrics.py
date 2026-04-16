from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score, classification_report

def compute_metrics(results):

    from collections import Counter

    # funzione di collasso: NEAR-DUPLICATE -> CLONE
    def collapse_label(label):
        if label in ["CLONE", "NEAR-DUPLICATE"]:
            return "CLONE"
        return "DISTINCT"

    y_true = [collapse_label(r["label"]) for r in results]

    # y_pred collassato + gestione INVALID
    y_pred = [
        collapse_label(r["prediction"]) if r["prediction"] != "INVALID" else "__INVALID__"
        for r in results
    ]

    labels = ["CLONE", "DISTINCT"]

    # ===== DEBUG MINIMO =====
    print("\n[DEBUG] Distribution y_true:")
    print(Counter(y_true))

    print("\n[DEBUG] Distribution y_pred:")
    print(Counter(y_pred))
    # =======================

    # Metriche globali
    precision = precision_score(y_true, y_pred, average="weighted", labels=labels, zero_division=0)
    recall = recall_score(y_true, y_pred, average="weighted", labels=labels, zero_division=0)
    f1 = f1_score(y_true, y_pred, average="weighted", labels=labels, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    accuracy = accuracy_score(y_true, y_pred)

    report = classification_report(
        y_true,
        y_pred,
        labels=labels,
        output_dict=True,
        zero_division=0
    )

    per_class = {
        label: {
            "precision": round(values["precision"], 4),
            "recall": round(values["recall"], 4),
            "f1": round(values["f1-score"], 4)
        }
        for label, values in report.items()
        if label not in ["accuracy", "macro avg", "weighted avg"]
    }

    invalid_rate = sum(
        1 for r in results if r["prediction"] == "INVALID"
    ) / len(results)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "invalid_rate": invalid_rate,
        "confusion_matrix": cm.tolist(),
        "per_class": per_class
    }