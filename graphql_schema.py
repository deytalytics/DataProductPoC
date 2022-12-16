from strawberry import Schema, type, field
import typing

def load_schema(objectData):
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
            filteredData = [d for d in objectData if d.CountryName == countryName]
            return filteredData
        if continentCode:
            # Filter the countries based on the ContientCode if the argument was supplied
            filteredData = [d for d in objectData if d.ContinentCode == continentCode]
            return filteredData
        else:
            #Otherwise just return the unfiltered data
            return objectData

    #Define a legitimate query where continent and countries can be returned, filtered on CountryName if it is supplied
    @type
    class Query:
        @field
        def countries(self, info, CountryName: typing.Optional[str], ContinentCode: typing.Optional[str]) -> typing.List[Country]:
            return get_countries(CountryName, ContinentCode)


    schema = Schema(query=Query)
    return schema