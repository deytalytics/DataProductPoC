import csv, json, yaml

#As we want our API to return both JSON messages and CSV files, we'll need to convert our source CSV files to JSON payload files.
def csv_to_json(object):
    csvf="data/"+object+".csv"
    with open(csvf, newline='', encoding='utf-8-sig') as csvfile:
        # load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvfile)
        objectData = []
        # convert each csv row into python dict
        for row in csvReader:
            # add this python dict to json array
            objectData.append(row)
        #Encapsulate the object data with info about the object
        json_data = {'data': {object:objectData}}

    #Close the CSV file
    csvfile.close()
    #Write the JSON file
    with open("data/"+object+'.json', 'w') as json_file:
        json.dump(json_data, json_file)