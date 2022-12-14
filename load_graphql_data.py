import os, json
from collections import namedtuple


# This function will load a JSON file into a Python NamedTuple object which is required for Strawberry-GraphqL
def customJSONDecoder(Object):
    return namedtuple('X', Object.keys())(*Object.values())


def load_graphql_data (fname):
    # If file exists
    if os.path.isfile(fname):
        with open(fname, "r") as file:
            # And convert each row in the JSON file into a Python Object
            objectData = json.load(file, object_hook=customJSONDecoder)

            file.close()
    return objectData