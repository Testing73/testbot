"""Model training and saving the model for later use"""

import time
from nlu.intent_classification import *
from nlu.named_entity import *
data = pd.read_csv("training_data.csv")
dff = pd.read_csv("emp_details.csv")


def training_pipeline(dataset):
    """
    Entire training pipeline
    :param training_data:
    :return: pickle files which contains models.
    """

    print("Training the given {0} for intent_classification".format(dataset))
    t0 = time.time()

    from pprint import pprint
    pprint(dataset)
    intent_classify(dataset)
    print("Model training time is {}".format(round(time.time()-t0), 3))
    print('Training entity model')
    train_entity(dataset)
    print("---------------------------------------------------------------------------")
    udf = simple_uv(dff)
    while True:
        user_input = input()
        if user_input == 'stop':
            break
        else:
            entities = final_json(user_input, udf, dff)
            intent_name = test_input(user_input)
            entities = test(user_input)
            print(intent_name)

training_pipeline(data)
