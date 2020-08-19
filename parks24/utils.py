
from shapely.geometry import Polygon
import shapely.ops as ops
from functools import partial
import pyproj

def boundary_area(way):
    points = [ (node.lat, node.lon) for node in way.nodes ]
    if len(points) > 2:
        geom = Polygon(points)
        geom_meters = ops.transform(
            partial(
                pyproj.transform,
                pyproj.Proj(init='EPSG:4326'),  # EPSG:4326 est WGS 84
                pyproj.Proj(
                    proj='aea',
                    lat1=geom.bounds[1],
                    lat2=geom.bounds[3]
                )
            ),
            geom)
        return geom_meters.area
    else:
        return 0
