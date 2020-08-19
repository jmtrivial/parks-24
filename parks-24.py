#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from parks24.parks import Parks
from parks24.cities import Cities

minArea = 100 * 100

french_cities = Cities("France")

parks = {}

for city in french_cities.getCitiesName():
    cityArea = french_cities.getCityAreaInMeterSquare(city)
    parks[city] = Parks(city)
    print("City: " + city)
    print(parks[city].getStats(cityArea, minArea))
