#!/usr/bin/env python
import requests
import lxml
from bs4 import BeautifulSoup
# 測站 ID 查詢： https://e-service.cwa.gov.tw/wdps/obs/state.htm
stations = ['C0AJ80','C0AD40','C0A520']
tmp_str=''
for ele in stations:
    tmp_str = ele + ',' +tmp_str
print(tmp_str)
# using CWA API url [ O-A0001-001無人自動測站 ]:
# https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=CWB-F130194A-3405-4E95-902E-60B61FCB661F&format=XML&StationId=C0AJ80
# return as XML format.

f=open("cwa.token.txt",'r')
get_token_from_file = f.readlines()[0].strip("\n").split("=")[1]
print(get_token_from_file)
f.close()

print(tmp_str)
api_url="https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization={}&format=XML&StationId={}".format(get_token_from_file,tmp_str)
result = requests.get(api_url)
soup = BeautifulSoup(result.text,"xml")
# print(soup)

fields=[]
for ele in soup.select("fields id"):
    print(ele.text)
    fields.append(ele.text)
    print(soup.select("records")[0].select(ele.text))
# print(fields)

for station in stations:
    CountyName = soup.select("stations")[stations.index(station)].select("CountyName")[0].text
    StationName = soup.select("stations")[stations.index(station)].select("StationName")[0].text
    StationId = soup.select("stations")[stations.index(station)].select("StationId")[0].text
    print("{} 測站名= {}, id= {}".format(CountyName, StationName, StationId))

    WGS84_StationLatitude = soup.select("stations")[stations.index(station)].select("GeoInfo")[0].select("Coordinates")[1].select("StationLatitude")[0].text
    WGS84_StationLongitude = soup.select("stations")[stations.index(station)].select("GeoInfo")[0].select("Coordinates")[1].select("StationLongitude")[0].text
    print("測站經緯度 [WGS84]",WGS84_StationLatitude, WGS84_StationLongitude)

    StationAltitude = soup.select("stations")[stations.index(station)].select("GeoInfo")[0].select("StationAltitude")[0].text
    print("測站高度 {}m".format(StationAltitude))

    AirTemperature = soup.select("stations")[stations.index(station)].select("AirTemperature")[0].text
    RelativeHumidity = soup.select("stations")[stations.index(station)].select("RelativeHumidity")[0].text
    AirPressure = soup.select("stations")[stations.index(station)].select("AirPressure")[0].text

    print("測站氣壓 {}hPa, 溫度 {}DEG C, 濕度 {}%".format(AirPressure, AirTemperature, RelativeHumidity))

    DateTime = soup.select("stations")[stations.index(station)].select("ObsTime")[0].select("DateTime")[0].text
    print("觀測時間 {}".format(DateTime))
    print("="*32)