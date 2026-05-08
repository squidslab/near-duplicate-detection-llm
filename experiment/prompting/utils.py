def get_few_shot_examples(dataset):

    example_clone = None 
    example_different = None
    for data in dataset:

        if data["label"] == "CLONE" and example_clone is None:
            example_clone = data 

        elif data["label"] == "DISTINCT" and example_different is None: 
            example_different = data    

        if example_clone and example_different: #interrompo quando trovo esempi 
            break

    return example_clone,example_different 