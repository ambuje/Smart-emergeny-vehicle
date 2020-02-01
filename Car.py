import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('pragmatic-star-266013-ce5923bb9343.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
dbV = firestore.client()
db_car = firestore.client()

#################################### Check ambulance request ############################

while(True):
  users_ref_car = db.collection(u'req_car')
  docs = users_ref_car.stream()
  for doc in docs:
    pass
  lat=doc.to_dict()['req']
  if lat == 1:
    break

#################################### GET HOSPITAL LOCATION ############################

users_ref = db.collection(u'amb')
docs = users_ref.stream()
for doc in docs:
  pass
lat=doc.to_dict()['dest'].latitude
longi=doc.to_dict()['dest'].longitude


hospital_long = round(longi,4)
hospital_lat = round(lat,4)

#################################### GET AMBULANCE LOCATION ############################

users_ref = db.collection(u'amb')
docs = users_ref.stream()
for doc in docs:
  pass
lat=doc.to_dict()['location'].latitude
longi=doc.to_dict()['location'].longitude


long_amb = round(longi,4)
lat_amb = round(lat,4)

#################################### GET WAYPOINTS ############################

import googlemaps
from datetime import datetime
import polyline

def lat(a,b):
    gmaps = googlemaps.Client(key='AIzaSyAZQl0TRenJIoCbKNjDKmT2LN9Y94um9qs')
    now = datetime.now()
    directions_result = gmaps.directions(a, b,
                                         mode="driving",
                                         departure_time=now)
    final=list()
    for i in directions_result:
        #print(i.keys())
       # print(i['legs'])
        for j in i['legs']:
            #print(j.keys())
            for k in j['steps']:
                final.append(k['polyline'])
    
    finall=[]
    for p in final:
        #print(p)
        #print(p['points'])
        finall.extend(polyline.decode(p['points']))
    finall=[(round(item[0],4),round(item[1],4))for item in finall]
    return finall

a = list(lat((lat_amb,long_amb),(hospital_lat,hospital_long)))

#################################### GET CAR LOCATION ############################

car_locationusers_ref = dbV.collection(u'vehicle')
docs = car_locationusers_ref.stream()
for doc in docs:
  if doc.id == 'TKUkXIRSthSuLhXs3a8ZAbHvBH83':
    lat_car=(doc.to_dict()['point'].latitude)
    long_car=(doc.to_dict()['point'].longitude)

#################################### CALCULATE DISTANCE BETWEEN CAR AND AMBULANCE ############################

from math import radians, sin, cos, acos

slat = radians(float(lat_amb))
slon = radians(float(long_amb))
elat = radians(float(lat_car))
elon = radians(float(long_car))

dist = 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
dist

#################################### Update the firebase if car in path ############################

if (lat_car, long_car) in a and dist <= 5:
  print("Emergency Vehicle Approaching")
  data = {
    u'inpath': u'true'
  }
  db.collection(u'in_way').document(u'xvMjLM9OeMboSjuoqrbu').set(data)
else:
  data = {
    u'inpath': u'hakunamatata'
  }
  db.collection(u'in_way').document(u'xvMjLM9OeMboSjuoqrbu').set(data)



