from typing import Any, Dict, Optional, TextIO
import overpy
import geopandas as gpd

def overpass_to_geojson(result: overpy.Result, nodes: bool = False, ways: bool = True):
    features = []
    if nodes:
        for node in result.nodes:
            properties: Dict[str, Any] = {}
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        float(node.lon),
                        float(node.lat)
                    ]
                },
                "properties": properties
            })

    if ways:
        for way in result.ways:
            properties = {}
            coordinates = []
            for node in way.nodes:
                coordinates.append([
                    float(node.lon),
                    float(node.lat)
                ])
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordinates
                },
                "properties": properties
            })

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return geojson


def get_overpass_gdf(bbox):
    api = overpy.Overpass()

    result = api.query(
        f"""[out:json] [timeout:60];
        (
            way["highway"="motorway"]( {bbox});
            way["highway"="motorway_link"]( {bbox});
            way["highway"="trunk"]( {bbox});
            way["highway"="trunk_link"]( {bbox});
            way["highway"="primary"]( {bbox});
            way["highway"="primary_link"]( {bbox});
            way["highway"="secondary"]( {bbox});
            way["highway"="secondary_link"]( {bbox});
            way["highway"="tertiary"]( {bbox});
            way["highway"="tertiary_link"]( {bbox});
            way["highway"="unclassified"]( {bbox});
            way["highway"="residential"]( {bbox});
            way["highway"="living_street"]( {bbox});
            way["highway"="service"]( {bbox});
            way["service"="parking_aisle"]( {bbox});
            way["highway"="escape"]( {bbox});
            way["highway"="road"]( {bbox});
            way["highway"="construction"]( {bbox});
            way["junction"="roundabout"]( {bbox});
            way["junction"="circular"]( {bbox});
            
        );
        (._;>;);
        out body;""")

    features = overpass_to_geojson(result)["features"]
    print(len(features))
    return gpd.GeoDataFrame.from_features(features)