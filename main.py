from typing import Union
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from os import getcwd, listdir
from CSVtoJSON import csv_to_json
import yaml,json, os, secrets
import logging


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
app = FastAPI(title=metadata['title'], description=metadata['description'],
              version=metadata['version'])

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    userpwd_db = [{"username": "james_dey@hotmail.com", "password": "test"},
                 {"username": "scott", "password": "tiger"}]
    current_username_bytes = credentials.username.encode("utf8")
    current_password_bytes = credentials.password.encode("utf8")
    #Loop through all of the stored usernames and passwords to look for a match
    for index in range(len(userpwd_db)):
        user=userpwd_db[index]['username']
        pwd=userpwd_db[index]['password']
        is_correct_username = secrets.compare_digest(current_username_bytes, bytes(user,'utf-8'))
        is_correct_password = secrets.compare_digest(current_password_bytes, bytes(pwd, 'utf-8'))
        #If we've found a match then return the username
        if is_correct_username and is_correct_password:
            return credentials.username
    #If we've not found a match for the username & password then we need to raise an exception
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Basic"},
    )



#Handle requests to root. Provide defaults for object of 'countries' and API message format of JSON
@app.get("/aboutme")
async def root(request: Request):
    return f"{request.headers} {request.method} {request.url}"

@app.get("/REST/{version}/{object}")
def read_root(version, object, format: str="json", username: str=Depends(get_current_username)):
    fname = "data/" + object + ".json"
    print(username)
    if not username:
        # If we've not found a match for the username & password then we need to raise an exception
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    #If file exists
    if os.path.isfile(fname):
        #If the end user hasn't provided a format or has requested a format of JSON
        if format=="json":
            with open(fname, "r") as file:
                jsonData = json.load(file)
            file.close()
            return jsonData
        elif format=="csv":
            filename = object+"."+format
            return FileResponse(path=getcwd() + "/data/"+filename, media_type='application/octet-stream', filename=filename)
        elif format=="html":
            with open(fname, "r") as file:
                jsonData = json.load(file)
            file.close()
            # Read the template for the data dictionary in to a string
            metafile = os.path.join('metadata', 'datadict_template.html')
            with open(metafile, 'r') as htmltemplate:
                htmlstr = htmltemplate.read()
                html = htmlstr % (object[0].upper() + object[1:])
                #Lets add the headings
                html += "<tr>"
                for heading in jsonData[0].keys():
                      html += "<th>%s</th>" %heading
                html += "</tr>"
                # Print out the entire table row for the dictionary entry
                for row in jsonData:
                    html+="<tr>"
                    for value in row.values():
                        html += "<td>%s</td>"%value
                    html+="</tr>"
                html += "</table></body></html>"
            return HTMLResponse(html)
        else:
        #Format is wrong so raise an exception
            raise HTTPException(status_code=404, detail="The supplied format is wrong. It needs to be csv or json")
    else:
        #File does not exist so raise an exception
        raise HTTPException(status_code=404, detail="{0}/{1} data does not exist".format(version,object))
@app.get("/REST/{version}/dictionary/{object}")
def read_dictionary(version, object, format:str="json"):
    fname = "metadata/schema/"+object+".yml"
    #If the schema file for the object exists
    if os.path.isfile(fname):
        #Load in the object schema from the yaml file which converts it to JSON
        with open(fname) as ymlfile:
            dictionary_entry = yaml.safe_load(ymlfile)
            if format == "json":
                ymlfile.close()
                return dictionary_entry
            elif format == "html":
                #Read the template for the data dictionary in to a string
                metafile = os.path.join('metadata','datadict_template.html')
                with open(metafile,'r') as htmltemplate:
                    htmlstr=htmltemplate.read()
                    html = htmlstr%(object[0].upper()+object[1:]+" data dictionary")
                    headings=['Name','Definition','Datatype']
                    html+="<tr>"
                    for heading in headings:
                        html+="<th>%s</th>"%heading
                    html+="<tr>"
                    #Print out the entire table row for the dictionary entry
                    for row in dictionary_entry['fields']:
                        html+="<tr><td>%s</td><td>%s</td><td>%s</td></tr>"%tuple(row.values())
                    html+="</table></body></html>"
                ymlfile.close()
                return HTMLResponse(html)
            else:
                ymlfile.close()
                # Format is wrong so raise an exception
                raise HTTPException(status_code=404, detail="The supplied format is wrong. It needs to be html or json")
    else:
        #File does not exist so raise an exception
        raise HTTPException(status_code=404,detail="REST/{0}/dictionary/{1} data does not exist".format(version,object))
