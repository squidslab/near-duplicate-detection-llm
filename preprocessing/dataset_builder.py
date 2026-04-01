from data_access.sampler import get_stratified_sample
from preprocessing.html_loader import get_html


def build_dataset(n_per_class=50): 

    stratified_data = get_stratified_sample(n_per_class)
    dataset = [] 

    for data in stratified_data:

        html1 = get_html(data["name"],data["crawl"],data["state1"])

        html2 = get_html(data["name"],data["crawl"],data["state2"])

       
        if html1 is None or html2 is None:  # scarta coppie con file mancanti
            continue

        dataset.append({
            "html1": html1,
            "html2": html2,
            "label": data["HUMAN_CLASSIFICATION"] 
        })

    return dataset 