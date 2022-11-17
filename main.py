from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from os import getcwd
from CSVtoJSON import csv_to_json
import yaml,json, os

ymlf="metadata/data_product_poc.yml"
with open(ymlf) as yamlfile:
    # load in the metadata for the docs from the yaml file
    metadata = yaml.safe_load(yamlfile)
app = FastAPI(title=metadata['title'], description=metadata['description'],
              version=metadata['version'])

csv_to_json("countries")

#Handle requests to root. Provide defaults for object of 'countries' and API message format of JSON
@app.get("/REST/{version}/{object}")
def read_root(version, object, format: str="json"):
    print(version, object, format)
    fname = "data/" + object + ".json"
    #If file exists
    if os.path.isfile(fname):
        #If the end user hasn't provided a format or has requested a format of JSON
        if format=="json":
            with open(fname, "r") as file:
                jsonData = json.load(file)
            file.close()
            return jsonData
        else:
            filename = object+"."+format
            return FileResponse(path=getcwd() + "/data/"+filename, media_type='application/octet-stream', filename=filename)
    else:
        #File does not exist so raise an exception
        raise HTTPException(status_code=404, detail="{0}/{1} data does not exist".format(version,object))
@app.get("/REST/{version}/dictionary/{object}")
def read_dictionary(version, object, format:str="json"):
    fname = "metadata/schema/"+object+".yml"
    #If file exists
    if os.path.isfile(fname):
        with open(fname) as ymlfile:
            dictionary_entry = yaml.safe_load(ymlfile)
            if format == "json":
                ymlfile.close()
                return dictionary_entry
            else:
                html="""<html>
<head>
<style>

table {

  font-family: arial, sans-serif;

  border-collapse: collapse;

}


td, th {

  border: 1px solid #dddddd;

  text-align: left;

  padding: 8px;

}


tr:nth-child(even) {

  background-color: #dddddd;

}

</style></head>
<body>
<h1>%s payload data dictionary</h1>
    <table>
            <tr>
                <th>Name</th>
                <th>Definition</th>
                <th>Datatype</th>
            </tr>"""%(object[0].upper()+object[1:])
            #Print out the entire table row for the dictionary entry
            for row in dictionary_entry['fields']:
                html+="<tr><td>%s</td><td>%s</td><td>%s</td></tr>"%tuple(row.values())
            html+="</table></body></html>"
            ymlfile.close()
            return HTMLResponse(html)
    else:
        #File does not exist so raise an exception
        raise HTTPException(status_code=404,detail="REST/{0}/dictionary/{1} data does not exist".format(version,object))
