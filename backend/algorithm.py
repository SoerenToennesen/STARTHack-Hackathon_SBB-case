# If you're coming from scratch, please install the libraries imported below
# pip install matplotlib
# pip install datetime
# pip install pytz
# pip install pyowm
# pip install meteomatics

from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import pytz
from pyowm import OWM
import requests
import urllib3
import os

def add_element(dict, key, value):
    if key not in dict:
        dict[key] = []
    dict[key].append(value)

# Dictionary that encapsulates all relevant data corresponding to the stations under unique stations
# Data format dictionary: {(str)station name : [[(str)parking time start 1, (str)parking time end 1], ... , (int)total parking spaces}
myDict = {}

# Extract data from present app database and put it in the dictionary myDict
data0 = json.loads(urlopen('https://data.sbb.ch/api/records/1.0/search/?dataset=parkrail-sale-app&q=&rows=100&sort=-start&facet=start&facet=end&facet=facility_name&facet=created&facet=booking_status').read())
for i in data0['records']:
    try:
        temp_start = datetime.datetime.strptime(i['fields']['start'], "%Y-%m-%dT%H:%M:%S.%f%z")
    except:
        temp_start = datetime.datetime.strptime(i['fields']['start'], "%Y-%m-%dT%H:%M:%S%z")
    try:
        temp_end = datetime.datetime.strptime(i['fields']['end'], "%Y-%m-%dT%H:%M:%S.%f%z")
    except:
        temp_end = datetime.datetime.strptime(i['fields']['end'], "%Y-%m-%dT%H:%M:%S%z")
    add_element(myDict, i['fields']['facility_name'], [temp_start, temp_end])

# Extract data from historical app database and put it in the dictionary myDict
data1 = json.loads(urlopen('https://data.sbb.ch/api/records/1.0/search/?dataset=parkrail-sale-app-history&q=&rows=100&facet=start&facet=end&facet=facility_name&facet=created&facet=booking_status').read())
for i in data1['records']:
    try:
        temp_start = datetime.datetime.strptime(i['fields']['start'], "%Y-%m-%dT%H:%M:%S.%f%z")
    except:
        temp_start = datetime.datetime.strptime(i['fields']['start'], "%Y-%m-%dT%H:%M:%S%z")
    try:
        temp_end = datetime.datetime.strptime(i['fields']['end'], "%Y-%m-%dT%H:%M:%S.%f%z")
    except:
        temp_end = datetime.datetime.strptime(i['fields']['end'], "%Y-%m-%dT%H:%M:%S%z")
    add_element(myDict, i['fields']['facility_name'], [temp_start, temp_end])

# Extract data from historical app database 2018 and put it in the dictionary myDict
data2 = json.loads(urlopen('https://data.sbb.ch/api/records/1.0/search/?dataset=parkrail-sale-app-2018&q=&rows=100&facet=start&facet=end&facet=facility_name&facet=created&facet=booking_status').read())
for i in data2['records']:
    try:
        temp_start = datetime.datetime.strptime(i['fields']['start'], "%Y-%m-%dT%H:%M:%S.%f%z")
    except:
        temp_start = datetime.datetime.strptime(i['fields']['start'], "%Y-%m-%dT%H:%M:%S%z")
    try:
        temp_end = datetime.datetime.strptime(i['fields']['end'], "%Y-%m-%dT%H:%M:%S.%f%z")
    except:
        temp_end = datetime.datetime.strptime(i['fields']['end'], "%Y-%m-%dT%H:%M:%S%z")
    add_element(myDict, i['fields']['facility_name'], [temp_start, temp_end])

# Extract data from another database and put it in the dictionary myDict
data3 = json.loads(urlopen("https://data.sbb.ch/api/records/1.0/search/?dataset=parkrail-sale-backend&q=&rows=100&facet=start&facet=end&facet=sales_channel&facet=created_at").read())
for i in data3['records']:
    try:
        temp_start = datetime.datetime.strptime(i['fields']['start'], "%Y-%m-%dT%H:%M:%S.%f%z")
    except:
        temp_start = datetime.datetime.strptime(i['fields']['start'], "%Y-%m-%dT%H:%M:%S%z")
    try:
        temp_end = datetime.datetime.strptime(i['fields']['end'], "%Y-%m-%dT%H:%M:%S.%f%z")
    except:
        temp_end = datetime.datetime.strptime(i['fields']['end'], "%Y-%m-%dT%H:%M:%S%z")
    add_element(myDict, i['fields']['bezeichnung_offiziell'], [temp_start, temp_end])

# Extract total parking space and put it in the dictionary myDict
data4 = json.loads(urlopen("https://data.sbb.ch/api/records/1.0/search/?dataset=mobilitat&q=&rows=832&facet=stationsbezeichnung&facet=parkrail_anzahl&facet=parkrail_preis_tag&facet=parkrail_preis_monat&facet=parkrail_pflichtig_zeit1&facet=parkrail_bemerkung&facet=railtaxitext&facet=mietvelo_bezeichnung&facet=veloparking_status_d&facet=veloparking_abschliessbar").read())
for i in data4['records']:
    if 'parkrail_anzahl' in i['fields']:
        add_element(myDict, i['fields']['bezeichnung_offiziell'], i['fields']['parkrail_anzahl'])

for key in myDict:
    while isinstance(myDict[key][:-2], float):
        temp_keyvalue = myDict[key]
        del temp_keyvalue[-2]
        myDict[key] = temp_keyvalue

# Save the number of Burgdorf tickets bought before the Burgdorf acquiring info from the Burgdorf specific database
# This allows us to roughly calculate how many tickets were bought through the "parking meter", which is the estimation we will use everywhere
val_before = myDict["Burgdorf"]
bought_online = len(val_before) - 1

# Extract data from the Burgdorf database and put it in the dictionary myDict
data5 = json.loads(urlopen("https://data.sbb.ch/api/records/1.0/search/?dataset=parkrail-burgdorf&q=&rows=100").read())
for i in data5['records']:
    try:
        temp_start = datetime.datetime.strptime(i['fields']['arrival_in_local_time'], "%Y-%m-%dT%H:%M:%S.%f%z")
    except:
        try:
            temp_start = datetime.datetime.strptime(i['fields']['arrival_in_local_time'], "%Y-%m-%dT%H:%M:%S%z")
        except:
            temp_start = datetime.datetime.strptime(i['fields']['arrival_in_local_time'], "%Y-%m-%dT%H:%M:%S")
    try:
        temp_end = datetime.datetime.strptime(i['fields']['departure_in_local_time'], "%Y-%m-%dT%H:%M:%S.%f%z")
    except:
        try:
            temp_end = datetime.datetime.strptime(i['fields']['departure_in_local_time'], "%Y-%m-%dT%H:%M:%S%z")
        except:
            try:
                temp_end = datetime.datetime.strptime(i['fields']['departure_in_local_time'], "%Y-%m-%dT%H:%M:%S")
            except:
                print("Weird error which I don't know why to handle so I just hardcode the date")
                temp_end = datetime.datetime.strptime("2021-02-20T12:36:48", "%Y-%m-%dT%H:%M:%S")
    add_element(myDict, "Burgdorf", [temp_start, temp_end])
add_element(myDict, "Burgdorf", 115)

# Calculating the factor of difference of what the offline parking-meter yeilds. diff_in_buy will multiplication factor.
val_after = myDict["Burgdorf"]
bought_total = len(val_after) - 1
diff_in_buy = bought_total / bought_online
if diff_in_buy < 1:
    diff_in_buy = 1

def check_date_in_range(station, date):
    x = 0
    for i in myDict[station][:-1]:
        if isinstance(i, float):
            continue
        try:
            if i[0] <= pytz.UTC.localize(date) <= i[1]:
                x = x + 1
        except:
            if pytz.UTC.localize(i[0]) <= pytz.UTC.localize(date) <= pytz.UTC.localize(i[1]):
                x = x + 1
    return x

# Simple prediction that just checks the similarity in hours of every week day
def simple_prediction(station, date):
    date_pattern = '%Y-%m-%d %H:%M'
    date = datetime.datetime.strptime(date, date_pattern)
    avg = 0
    averaging_list = []
    date_temp = date
    #input date has to be after this date (chronologically)
    while True:
        date_temp -= datetime.timedelta(days = 7)
        if station == "Burgdorf":
            if date_temp < datetime.datetime(2021, 1, 1):
                break
        else:
            if date_temp < datetime.datetime(2018, 4, 4):
                break
        # Check occupancy of specified time slot at station
        test_cars_parked = check_date_in_range(station, date_temp)
        test_occupancy = test_cars_parked / myDict[station][-1]
        #print("{}% | {} out of {} cars.".format(round(test_occupancy*100, 2), test_cars_parked, int(myDict[station][-1])))
        averaging_list.append(test_occupancy)

    if station == "Burgdorf":
        percentile = len(averaging_list) / 3
        for i in range(len(averaging_list)):
            if i <= percentile:
                avg_one = averaging_list[:int(percentile)]
            elif i <= percentile*2:
                avg_two = averaging_list[int(percentile+1):int(percentile*2)]
            elif i <= percentile*3:
                avg_three = averaging_list[int(percentile*2+1):int(percentile*3)]
        avg = (sum(avg_one)/len(avg_one))*(0.6) + (sum(avg_two)/len(avg_two))*(0.3) + (sum(avg_three)/len(avg_three))*(0.1)

    else:
        percentile = len(averaging_list) / 8
        for i in range(len(averaging_list)):
            if i <= percentile:
                avg_one = averaging_list[:int(percentile)]
            elif i <= percentile*2:
                avg_two = averaging_list[int(percentile+1):int(percentile*2)]
            elif i <= percentile*3:
                avg_three = averaging_list[int(percentile*2+1):int(percentile*3)]
            elif i <= percentile*4:
                avg_four = averaging_list[int(percentile*3+1):int(percentile*4)]
            elif i <= percentile*5:
                avg_five = averaging_list[int(percentile*4+1):int(percentile*5)]
            elif i <= percentile*6:
                avg_six = averaging_list[int(percentile*5+1):int(percentile*6)]
            elif i <= percentile*7:
                avg_seven = averaging_list[int(percentile*6+1):int(percentile*7)]
            elif i <= percentile*8:
                avg_eight = averaging_list[int(percentile*7+1):]
        # Based on the Fibonacci Sequence (8 numbers from 1 to 34 scaled to 100%), extracting 8 percentiles with these weights (diminishing with time)
        avg = (sum(avg_one)/len(avg_one))*((34 * (100 / 87)) / 100) + (sum(avg_two)/len(avg_two))*((21 * (100 / 87)) / 100) + (sum(avg_three)/len(avg_three))*((13 * (100 / 87)) / 100) + (sum(avg_four)/len(avg_four))*((8 * (100 / 87)) / 100) + (sum(avg_five)/len(avg_five))*((5 * (100 / 87)) / 100) + (sum(avg_six)/len(avg_six))*((3 * (100 / 87)) / 100) + (sum(avg_seven)/len(avg_seven))*((2 * (100 / 87)) / 100) + (sum(avg_eight)/len(avg_eight))*((1 * (100 / 87)) / 100)
    
    # Result is in decimal (and not in percentage)
    return avg

def prediction(city, date):
    test_prediction = simple_prediction(city, date)

    owm = OWM('d1b8b51eb3502b063421f95b1e8cc893')
    mgr = owm.weather_manager()
    obs = mgr.weather_at_place('Uruguaiana')
    w = obs.weather

    if w.rain == {}:
        rain_temp = 0
    else:
        rain_temp = w.rain['1h']
    if rain_temp > 5:
        rain_temp = 100
    elif 3 < rain_temp <= 5:
        rain_temp = 90
    elif 1 < rain_temp <= 3:
        rain_temp = 70
    elif 0 < rain_temp <= 1:
        rain_temp = 40
    else:
        rain_temp = 0

    temperature_temp = w.temperature('celsius')['feels_like']
    if 40 < temperature_temp:
        temperature_temp = 90
    elif 35 < temperature_temp <= 40:
        temperature_temp = 60
    elif 25 < temperature_temp <= 35:
        temperature_temp = 20
    elif 20 < temperature_temp <= 25:
        temperature_temp = 0
    elif 15 < temperature_temp <= 20:
        temperature_temp = 30
    elif 5 < temperature_temp <= 15:
        temperature_temp = 70
    elif 0 < temperature_temp <= 5:
        temperature_temp = 80
    elif -10 < temperature_temp <= 0:
        temperature_temp = 90
    elif temperature_temp <= -10:
        temperature_temp = 100

    # Extendable with sunny
    weather_weight = w.humidity*0.2 + rain_temp*0.5 + temperature_temp*0.3
    weather_weight = ((weather_weight - 50) * (-1)) / 100


    # this is probably super biased based on my culture :) + this can be detailed much better
    date_pattern = '%Y-%m-%d %H:%M'
    date = datetime.datetime.strptime(date, date_pattern)
    seasonalDict = {"winterbreak" : [datetime.date(year=date.year, month=12, day=23), datetime.date(year=date.year, month=12, day=31)] , "summerbreak" : [datetime.date(year=date.year, month=7, day=12), datetime.date(year=date.year, month=7, day=25)], "springbreak" : [datetime.date(year=date.year, month=3, day=29), datetime.date(year=date.year, month=4, day=4)], "autumnbreak" : [datetime.date(year=date.year, month=10, day=18), datetime.date(year=date.year, month=10, day=24)]}

    holiday_date = 1
    for key in seasonalDict:
        if seasonalDict[key][0] <= date.date() <= seasonalDict[key][1]:
            holiday_date = 1.2
            break

    global weather_response
    global weather_url
    token_url = "https://sso-int.sbb.ch/auth/realms/SBB_Public/protocol/openid-connect/token"
    client_id = 'df3fa736'
    client_secret = '15a45c13f35913d407d3a3faef9cda5e'
    data = {'grant_type': 'client_credentials'}
    access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
    tokens = json.loads(access_token_response.text)
    api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
    var1 = pytz.UTC.localize(date)
    var1 = str(var1).replace('+00:00', 'Z')
    var1 = var1.replace(' ', 'T')
    var2 = pytz.UTC.localize(date + datetime.timedelta(hours=1))
    var2 = str(var2).replace('+00:00', 'Z')
    var2 = var2.replace(' ', 'T')
    weather_url = f'https://weather-int.api.sbb.ch/{var1}--{var2}:PT1H/fresh_snow_6h:cm,fresh_snow_1h:cm/46.50389,8.30325/json'
    #weather_url = f'https://weather-int.api.sbb.ch/2021-02-15T00:00:00Z--2021-03-4T00:00:00Z:PT1H/fresh_snow_6h:cm,fresh_snow_1h:cm/46.50389,8.30325/csv'
    #print (weather_url)
    weather_response = requests.get(weather_url,headers=api_call_headers)
    print(weather_response)

    # based on simple_algo and weather_conditions and if the date is during a holiday
    if city == "Burgdorf":
        final_prediction = (test_prediction) * (1 + weather_weight) * holiday_date
    else:
        final_prediction = (test_prediction * diff_in_buy) * (1 + weather_weight) * holiday_date
    if final_prediction > 1:
        final_prediction = 1
    
    return final_prediction * 100, int(myDict[city][-1])

#result is in the format (prediction (%), total spaces in parking lot (int)) | Technically: (float, int)
ans = prediction('Zug', '2021-02-27 12:00')
print("Zug @ 2021-02-27 12:00")
print(ans)
ans = prediction('Zürich Tiefenbrunnen', '2021-02-27 12:00')
print("Zürich Tiefenbrunnen @ 2021-02-27 12:00")
print(ans)
ans = prediction('Burgdorf', '2021-02-27 12:00')
print("Burgdorf @ 2021-02-27 12:00")
print(ans)

# REMEMBER TO CHANGE THE ROW EXTRACT VALUES FROM THE DATASET FETCHES (CURRENTLY ONLY 100).
# THIS IS REQUIRED TO GET ANY MEANINGFUL DATA

# Examples of extracting data (assuming data is correct and valid) from the created dictionary
# - print(myDict['Zug']) #Shows all relevant information pertaining to the specified station
# - print(myDict['Zug'][0]) #Shows one entry of a occupied time slot in the specified station
# - print(myDict['Zug'][0][0]) #Shows one entry's start or end time of a specified time slot in the specified station
# - print(myDict['Zug'][-1]) #Shows the total parking spaces at the specified station

# WHICH PARAMETERS DOES THE ALGORITHM TAKE INTO ACCOUNT?
# - Same hour of the previous weeks up until the earliest data point (can be limited in case of massive datasets, but that isn't a problem here).
#   Here it takes an average of all the weeks, and puts a larger weight on averages that lie closer to the date (split up as 8 percentiles)
#   The diminishing effect less recent data points have follow the Fibonnacci sequence, because why not
# - Weather with parameters and respective weights of humidity(0.2), rain(0.5), temperature(0.3)
#   Temperature can be too hot and too cold (at extreme temperatures) - a close temperature to room temperature (25 degrees Celsius) has the most influence on occupancy predictions (nice weather = more people go out and travelling)
#   Currently, because we have no API, we rely on the Open Weather Map, which provides limited information and future forecasts in the free version. Thus we don't look into the future here currently (a fixable issue)
# - Seasons, currently 4 seasons implemented; (1) winterbreak / christmas, (2) springbreak / easter, (3) summerbreak (the most busy week (29)), and (4) autumnbreak
#   If a requested date prediction falls under a season, a 20% occupancy increase of the current prediction will be added, as more people travel during the holidays.
#   More seasons and weights can be implemented, but this is a simply model that also encapsulates this parameter
# - We estimated the tickets bought from the parking meter (offline) from the amount of tickets in the Bergdorf before and after the Bergdorf specific dataset was included.
#   We thus estimated the parking meter multiplier to be 13.625 which we used on other stations as well.
# THE ALGORITHM IS NOT PERFECT DUE TO INSUFFICIENT DATA, ALTHOUGH IF A MORE REALISTIC PREDICTION SHOULD BE TAKEN, THEN BURGDORF HAS PLENTIFUL DATA FOR THE FIRST 2 MONTHS OF 2021, AND CAN BE USED FOR PREDICTION FOR THIS PARTICULAR STATION.
# (remember to increase the API feeds - currently they are all set at 100, but should be increased to the max avaliable or the max possible (10000))... alternatively the datasets can be downloaded so all rows can be used and seen in action

#TODO: Specify date for the weather parameter