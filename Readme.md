A working example of this data product REST API is available
at http://dp-poc.herokuapp.com/REST/v1/countries
which can be used by applications 
or http://dp-poc.herokuapp.com/REST/v1/countries?format=csv
which returns a CSV file so can be used by an end user or by a reporting tool

The API documentation is at:- http://dp-poc.herokuapp.com/docs

To amend for your own needs:-
1. Add your source data to a file called data/{object}.csv
2. Add your schema file to metadata/schema/{object}.yml
3. Amend metadata/data_product_poc.yml and add/edit links to the dictionary entry section.


