from typing import Counter
from collections import defaultdict, Counter
from data_access.sampler import get_stratified_sample_for_experiment, get_stratified_sample_for_ex_two_class
from preprocessing.html_loader import get_html
from preprocessing.image_loader import get_image


def build_dataset(tot_experiment=50, seed=42, db_path=None, input_type="html", example=False):

    if(example== False):
       stratified_data = get_stratified_sample_for_ex_two_class(tot_experiment, seed, db_path) 
    elif(example==True):
        n_per_class = tot_experiment // 3 
        stratified_data = get_stratified_sample_for_experiment(n_per_class,seed,db_path)   
       

    dataset = []

    if(example == True):
      label_map = {
        0: "CLONE",
        1: "NEAR-DUPLICATE",
        2: "DISTINCT"
        }
    elif (example == False):
        label_map = {
        0: "CLONE",
        1: "CLONE",
        2: "DISTINCT"
        }


    for data in stratified_data:

        if input_type == "html":
            input1 = get_html(data["app_name"], data["crawl"], data["state1"])
            input2 = get_html(data["app_name"], data["crawl"], data["state2"])

        elif input_type == "image":
            input1 = get_image(data["app_name"], data["crawl"], data["state1"])
            input2 = get_image(data["app_name"], data["crawl"], data["state2"])

        else:
            raise ValueError("input_type must be 'html' or 'image'")

        if input1 is None or input2 is None:
            continue

        dataset.append({
            "input1": input1,
            "input2": input2,
            "label": label_map[data["label"]]
        })

    return dataset 