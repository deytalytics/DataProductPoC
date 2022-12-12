from strawberry import Schema, type, field
import typing, os, json
from json import JSONEncoder

def load_schema(jsonData):
    @type
    class Country:
        ContinentName: str
        ContinentCode: str
        CountryName: str
        ThreeLetterCountryCode: str
        TwoLetterCountryCode: str
        CountryNumber: str

    #We will fetch the data from a JSON file
    def get_countries(countryName, continentCode):
        if countryName:
            # Filter the countries based on the CountryName if the argument was supplied
            filteredData = [d for d in jsonData if d.CountryName == countryName]
            return filteredData
        if continentCode:
            # Filter the countries based on the ContientCode if the argument was supplied
            filteredData = [d for d in jsonData if d.ContinentCode == continentCode]
            return filteredData
        else:
            #Otherwise just return the unfiltered data
            return jsonData

    #Define a legitimate query where continent and countries can be returned, filtered on CountryName if it is supplied
    @type
    class Query:
        @field
        def countries(self, info, CountryName: str = None, ContinentCode: str = None) -> typing.List[Country]:
            return get_countries(CountryName, ContinentCode)


    schema = Schema(query=Query)
    return schema



