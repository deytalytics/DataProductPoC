import yaml, os
from os import getcwd, listdir
from CSVtoJSON import csv_to_json


def load_metadata():
    # load in the metadata for the docs from the yaml file
    ymlf="metadata/data_product_poc.yml"
    with open(ymlf) as yamlfile:
        metadata = yaml.safe_load(yamlfile)
        #Lets add to the /docs metadata the bits that might vary
        metadata['description']+="## Path Parameter Lists of Values\n"
        #Lets add all of the versions to the /docs metadata
        versions=['0.1']
        metadata['description']+="### Version\n"
        for version in versions:
            metadata['description'] += "* %s\n"%version
        #Let's add all of the objects to the /odcs metadata
        #get metadata schema path
        path = os.path.join(getcwd(),"metadata","schema")
        #Loop through all of the schema yaml filenames in the /metadata/schema directory
        metadata['description']+="### Object\n"
        for fname in listdir(path):
            name = fname.split('.')[0]
            #Add data dictionary entries for each object
            metadata['description']+="* [%s](REST/%s/dictionary/%s?format=html)\n"%(name,metadata['version'],name)
            #And also generate JSON files from the csv files in the /data directory
            csv_to_json(name)
        #Lets add all of the formats to the /docs metadata
        formats=['json','csv','html']
        metadata['description']+="## Query Parameter List of Values\n"
        metadata['description']+="### Format\n"
        for format in formats:
            metadata['description'] += "* %s\n"%format
    return metadata