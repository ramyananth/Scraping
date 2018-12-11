# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 14:52:42 2018

@author: ramya.ananth
"""

import geopy
import pandas as pd

from geopy.geocoders import GoogleV3
geolocator = GoogleV3()

#location = geolocator.geocode("175 5th Avenue NYC")
#print(location.address)


def geocode(address):
    try:
        location = geolocator.geocode(address)
        return location.raw['place_id']
    except:
        return 'Failed'

#address='Tredence Analytics Solutions Pvt. Ltd., EPIP Zone, Whitefield, Bengaluru, Karnataka, India'

addresses = pd.read_excel('C:\\Users\\ramya.ananth\\Documents\\Adhoc\\Listing of Oldest Stores with Opening Date.xlsx')
addresses.head()
#addresses['search_term'] = addresses['Addresses']+','+ addresses['DHC Zip'].astype(str)

addresses['placeId'] = addresses['AddressFinal'].apply(geocode)

#results = []
#
#for idx, address in enumerate(add_list):
#    print('Address: '+address)
#    x = geocode(address)
#    results.append(x)
#    print("Result: "+ str(x))