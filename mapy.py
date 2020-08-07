import geopandas as gpd
from os import listdir

ruta="/home/uribarrix/Datos de Mapas/Mapas Completos/"

def ls(ruta):
    return listdir(ruta)

lista=ls(ruta)
numlist = 0
for x in lista:
    numlist += 1
     
numlist = len(lista)

rutas=[
    ruta + x + "/" + x + ".geojson"
    for x in lista
]

rrutas=[
    'r"' + x + '"'
    for x in rutas
]

rrutas0=sorted(rrutas)      

lista0=sorted(lista)

dicdates=[
    {'date': x
        
    }for x in lista0
]

dicruta=[
    {"ruta": x
        
    }for x in rrutas0
]

import ast

poligonos=[]

for x in dicdates:
    ddr = gpd.read_file(ruta+x['date']+"/"+x['date']+".geojson")

    for i in ddr['Facción']:
        geom  = str(ddr[ddr['Facción'] == i].unary_union)
        dende = geom.find("(")
        coord1 = geom[dende:]
        coord2 = coord1.replace(")), ((",")),((")
        coord3 = coord2.replace(", ","),(")
        coord4 = str([coord3.replace(" ", ", ")]).replace("'(","(").replace(")'", ")")
        coord5 = coord4.replace("[(((", "[((").replace(")))]", "))]")
        coord = ast.literal_eval(coord5.replace("[((", "[(((").replace("))]",")))]"))
        coordgrup = {'date': x['date']+'-01', 'coordinates': coord, 'color': 'green', 'faccion': i}

        poligonos.append(coordgrup)
        
features = [
    {
        'type': 'Feature',
        'geometry': {
            'type': 'MultiPolygon',
            'coordinates': pol['coordinates'],
        },
        'properties': {
            'faccion': pol['faccion'],
            'time': pol['date'],
            'style': {
                'color': pol['color']
        },
            }
    } for pol in poligonos
]

import pandas as pd
data=pd.read_csv(r"/home/uribarrix/Datos de Mapas/mais datos siria/fotos.csv")

cols = ['SITUACION', 'popup', 'name', 'LUGAR', 'TIPO']

for i, row in data.iterrows():
    foto = {'type':'Feature','properties':{},'geometry':{'type':'Point','coordinates':[]}}
    foto['geometry']['coordinates'] = [row.X,row.Y]
    foto['properties']['icon'] = 'marker'
    foto['properties']['iconstyle'] = {}
    foto['properties']['times'] = [row.start,row.end]
    for prop in cols:
        foto['properties'][prop] = row[prop]
        for icost in prop:
            foto['properties']['iconstyle']['iconUrl'] = row.iconUrl
            foto['properties']['iconstyle']['iconSize'] = [45,45]
            foto['properties']['iconstyle']['shadowUrl'] = 'https://i.ibb.co/7z6p6z5/shadow.png'
            foto['properties']['iconstyle']['shadowSize'] = [85,45]
            foto['properties']['iconstyle']['iconAnchor'] = [25,45]
            foto['properties']['iconstyle']['shadowAnchor'] = [45,45]
    features.append(foto)
    
import folium
from folium.plugins import TimestampedGeoJson
from folium.plugins import MeasureControl

#token = "pk.eyJ1IjoidXJpYmFycml4IiwiYSI6ImNqczF6bHlrMDAxajk0M29lNTFjZXBxaWQifQ.eBXrC0QHSe-H4lh_7qul2g" # your mapbox token
#tileurl = 'https://api.mapbox.com/styles/v1/uribarrix/cjs6taxrd2t1f1fl346o883v4/tiles/256/{z}/{x}/{y}@2x?access_token=' + str(token)

mapa = folium.Map(location=[34.8,39.00],
  zoom_start=7, control_scale = True,
  tiles="openstreetmap")

TimestampedGeoJson(
    {'type': 'FeatureCollection', 'features': features},
    period='P3M',
    duration='P2M',
    auto_play=False,
    add_last_point=True,
    min_speed=0.5,
    max_speed=1,
    loop=False,
    loop_button=True,
    date_options='YYYY/MM/DD',
).add_to(mapa)

mapa.save('mapa.html')