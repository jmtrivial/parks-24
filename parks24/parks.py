

import overpy

from parks24.utils import boundary_area


threshold = 200 * 200

class Parks:
    
    def __init__(self, city):
        self.city = city
        self.parks = []
        
        self.getParksData()
    
    def __str__(self):
        result = "City: " + self.city
        result += "\nNumber of parks: " + str(len(self.parks))
        return result
        
    def getParksData(self):


        # fetch all ways and nodes
        api = overpy.Overpass()
        result = api.query("area[\"name\"=\"" + self.city + "\"" + 
            """]["admin_level"="8"]->.boundaryarea;
            (nwr(area.boundaryarea)[leisure=park];);
            (._;>;);
            out body;
            """)
        
        for way in result.ways:
            
           area = boundary_area(way)
           if area > 0:
                name = way.tags.get("name", None)
                opening_hours = way.tags.get("opening_hours", None)
                self.parks += [{ "name": name, "id": way.id, "opening_hours": opening_hours, "area": area }]
                
    def getStats(self, cityArea, minArea):
        result = { "number": 0, "unknown": 0, "closing": 0, "open24_7": 0,
                   "area": 0, "area_unknown": 0, "area_closing": 0, "area_open24_7": 0 }
        for park in self.parks:
            if park["area"] > minArea:
                result["number"] += 1
                result["area"] += park["area"]
                if park["opening_hours"] == None:
                    result["unknown"] += 1
                    result["area_unknown"] += park["area"]
                elif park["opening_hours"] == "24/7":
                    result["open24_7"] += 1
                    result["area_open24_7"] += park["area"]
                else:
                    result["closing"] += 1
                    result["area_closing"] += park["area"]
        result["park_density"] = cityArea / result["area"]
        areaKnownStatus = result["area_closing"] + result["area_open24_7"]
        if areaKnownStatus != 0:
            result["ratio_open247"] = result["area_open24_7"] / areaKnownStatus
        else:
            result["ratio_open247"] = None
        if result["area"] != 0:
            result["ratio_unknown"] = result["area_unknown"] / result["area"]
        else:
            result["ratio_unknown"] = None
        return result
                
            
                

