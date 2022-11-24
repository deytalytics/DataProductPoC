A working example of this data product REST API is available
at http://dp-poc.herokuapp.com/REST/0.1/countries
which can be used by applications 
or http://dp-poc.herokuapp.com/REST/0.1/countries?format=csv
which returns a CSV file so can be used by an end user or by a reporting tool
or http://dp-poc.herokuapp.com/REST/0.1/countries?format=html
which allows an end user to see the content as a web page before downloading it

The API documentation is at:- http://dp-poc.herokuapp.com/docs

To amend for your own needs:-
1. Add your source data to a file called data/{object}.csv
2. Add your schema file to metadata/schema/{object}.yml
3. Amend metadata/data_product_poc.yml and add/edit links to the dictionary entry section.

To run locally, from command line type 'uvicorn main:app --host 0.0.0.0 --port 8000'

And then from url type:- http://127.0.0.1:8000/docs etc


