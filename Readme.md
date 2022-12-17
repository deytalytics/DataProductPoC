A working example of the data product REST API is available
at:-
<br>
[https://dp-poc.azurewebsites.net/REST/0.1/countries](https://dp-poc.azurewebsites.net/REST/0.1/countries)
which can be used by applications 
or 
[https://dp-poc.azurewebsites.net/REST/0.1/countries?format=csv](https://dp-poc.azurewebsites.net/REST/0.1/countries?format=csv)
which returns a CSV file so can be used by an end user or by a reporting tool
or [https://dp-poc.azurewebsites.net/REST/0.1/countries?format=html](https://dp-poc.azurewebsites.net/REST/0.1/countries?format=html)
which allows an end user to see the content as a web page before downloading it

The API documentation is at:- 
<br>
[https://dp-poc.azurewebsites.net/docs](https://dp-poc.azurewebsites.net/docs)

To amend for your own needs:-
1. Add your source data to a file called data/{object}.csv
2. Add your schema file to metadata/schema/{object}.yml
3. Amend metadata/data_product_poc.yml and add/edit links to the dictionary entry section.

To run locally, from command line type:-
<br><code> uvicorn main:app --host 0.0.0.0 --port 8000 </code>

And then from web browser type:- 
<code> http://127.0.0.1:8000/docs </code> etc

There is also GraphQL functionality which can be queried by going to:-
<br>[https://dp-poc.azurewebsites.net/graphql](https://dp-pox.azurewebsites.net/graphql) 

Using the GraphiQL console, you can query continent and country data

e.g.
<br><code>
{ 
    countries(CountryName:"Martinique") {
        CountryNumber,CountryName,ContinentName
    }
}
</code>
<br>will return Country Number, Name & Continent Name for Martinique. The console provides type ahead assistance for arguments & fields

