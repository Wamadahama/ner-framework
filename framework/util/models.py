import os
MODELS_PATH = ""

def trained_models():
    pass

def read_model_files(model_name):
    """
    Gets the files from a model in the model folder,
    could be more extensible with an extensions list
    """
    try:
        all_files = os.listdir(model_name)
        return [model_name + "/" + file for file in all_files if ".json" in file or ".h5" in file]
    except:
        print("Unable to read from the models directory. Given directory {}".format(model_name))

def model_algorithms():
    pass
