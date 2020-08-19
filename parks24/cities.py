

import sys
from SPARQLWrapper import SPARQLWrapper, JSON


class Cities:
    
    def __init__(self, country, max_population = 100000, language = "fr"):
        self.cities = {}
        self.country = country
        self.max_population = max_population
        self.language = language
        
        if not self.country in [ "France" ]:
            print ("Unknown country")
            return
        
        self.getCitiesData()

        
    def __str__(self):
        return str(self.cities)
        
    def getWDResults(self, endpoint_url, query):
        user_agent = "Parks24 Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()        
    
    def getCitiesName(self):
        return [city for city in self.cities]
        
    def getCityAreaInMeterSquare(self, city):
        if not city in self.cities:
            return 0.0
        else:
            unit = self.cities[city]["areaUnit"]
            area = self.cities[city]["area"]
            if unit == "kilomètre carré":
                return float(area) * 1000 * 1000
            else:
                return None
    
    def getCitiesData(self):

        endpoint_url = "https://query.wikidata.org/sparql"

        if self.country == "France":
            query = """SELECT ?City ?CityLabel ?Population ?Area ?AreaUnitLabel
            WHERE {
            BIND(wd:Q142 AS ?France)
            BIND(wd:Q484170 AS ?Commune)
            ?City wdt:P31 ?Commune; 
            wdt:P17 ?France;
            p:P2046/psv:P2046  ?AreaNode;
            wdt:P1082 ?Population.
            ?AreaNode wikibase:quantityAmount ?Area.
            ?AreaNode     wikibase:quantityUnit       ?AreaUnit.
            SERVICE wikibase:label { bd:serviceParam wikibase:language 
            \"""" + self.language + """\". } FILTER ( ?Population > """ +  str(self.max_population) + """)
            }
            ORDER BY DESC (?Population)"""


        results = self.getWDResults(endpoint_url, query)

        for result in results["results"]["bindings"]:
            name = result["CityLabel"]["value"]
            self.cities[name] = {"name": name, "population": result["Population"]["value"], "area": result["Area"]["value"], "areaUnit": result["AreaUnitLabel"]["value"] }


        
