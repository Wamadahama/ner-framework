import os
import json

def read_json(filename, output='json'):
    """ Reads a json file given its file name.
        Tries to add the file extension if it is not there

        output options:
           dict -> returns read json as a python dictionary
           text -> returns read json as a python dictionary
    """

    raw_json = ""

    # Check if the file exists
    if not os.path.exists(filename):
        print("File {} does not exist!".format(filename))
        return None
    else:
        try:
            file = open(filename, 'r')
        except OSError:
            print("Could not read file: {}".format(filename))
            read_json(filename + '.json')
        with file:
            raw_json = file.read()
            file.close()

    if output == 'pairs-list':
        # [ { "word" : "area", "index": 0}, ...]
        pairs = json.loads(raw_json)
        return { pair["word"]:pair["index"] for pair in pairs}
    elif output == 'json':
        return raw_json
    elif output == 'dict':
        return json.loads(raw_json)
    else:
        return "Bad output"
