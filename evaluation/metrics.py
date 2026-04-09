from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score, classification_report

def compute_metrics(results):

    y_true = [r["label"] for r in results]

    #se la predizione è valida la prende com'è, se è invalid la sostituisce con __INVALID__ in modo da considerare gli errori nel calcolo delle metriche 
    y_pred = [
        r["prediction"] if r["prediction"] != "INVALID" else "__INVALID__"
        for r in results
    ]

    
    labels = ["CLONE", "NEAR-DUPLICATE", "DISTINCT"]

    #Metriche globali
    precision = precision_score(y_true, y_pred, average="weighted", labels=labels, zero_division=0)
    recall = recall_score(y_true, y_pred, average="weighted", labels=labels, zero_division=0)
    f1 = f1_score(y_true, y_pred, average="weighted", labels=labels, zero_division=0) 
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    accuracy = accuracy_score(y_true, y_pred)

    print("=== METRICS ===")
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1-score : {f1:.4f}")


    report = classification_report(y_true,y_pred,labels=labels,output_dict=True,zero_division=0)

    print("\n=== REPORT ===")
    for label, values in report.items():
        print(label, values)

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