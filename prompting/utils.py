def get_few_shot_examples(dataset):

    example_near_duplicates = None
    example_clone = None 
    example_different = None
    for data in dataset:

        if data["label"] == 1 and example_near_duplicates is None: 
            example_near_duplicates = data

        elif data["label"] == 0 and example_clone is None:
            example_clone = data 

        elif data["label"] == 2 and example_different is None: 
            example_different = data    

        if example_near_duplicates and example_clone and example_different: #interrompo quando trovo esempi 
            break

    return example_near_duplicates,example_clone,example_different 