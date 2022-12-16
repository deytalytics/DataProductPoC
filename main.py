from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import FileResponse, HTMLResponse
from strawberry.asgi import GraphQL

from authentication import get_current_username
import yaml,json, os
from os import getcwd
from load_metadata import load_metadata
from graphql_schema import load_schema
from load_data import load_data

#Import data
jsonData = load_data("data/countries.json")

#Fetch metadata for REST
metadata = load_metadata()

#Fetch metadata for GraphQL
schema = load_schema(jsonData)
graphql_app = GraphQL(schema)

#Start the FastAPI server providing a title, description and version
app = FastAPI(title=metadata['title'], description=metadata['description'],
              version=metadata['version'])

#Add in the routing info for GraphQL
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

#Handle requests to root. Provide defaults for object of 'countries' and API message format of JSON
@app.get("/aboutme")
async def root(request: Request):
    return f"{request.headers} {request.method} {request.url}"

@app.get("/REST/{version}/{object}")
def read_root(version, object, format: str="json"
              #,username: str=Depends(get_current_username)
):
    fname = "data/" + object + ".json"
    """
    if not username:
        # If we've not found a match for the username & password then we need to raise an exception
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
"""
    #If file exists
    if os.path.isfile(fname):
        #If the end user hasn't provided a format or has requested a format of JSON
        if format=="json":
            with open(fname, "r") as file:
                jsonData = json.load(file)
            file.close()
            return {'data':{'countries': jsonData }}
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

