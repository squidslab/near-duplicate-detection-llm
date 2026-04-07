from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, classification_report 

def compute_metrics(results):
    y_true = [r["label"] for r in results]
    y_pred = [r["prediction"] for r in results]

    precision = precision_score(y_true, y_pred, average="macro") # calcola quanto sono affidabili le predizioni positive
    recall = recall_score(y_true, y_pred, average="macro") # misura quanto il modello riesce a identificare tutti i casi reali (copertura)
    f1 = f1_score(y_true, y_pred, average="macro") #calcola equilibrio fra precision e recall 
    accuracy = accuracy_score(y_true, y_pred) #misura numero di predizioni corrette sul totale di esempi

    print("=== METRICS ===")
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1-score : {f1:.4f}")

    report = classification_report(y_true,y_pred,output_dict=True) 

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

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1, 
        "per class":per_class 
    }



