from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import pytz

def add_element(dict, key, value):
    if key not in dict:
        dict[key] = []
    dict[key].append(value)



# Dictionary that encapsulates all relevant data corresponding to the stations under unique stations
# Data format dictionary: {(str)station name : [[(str)parking time start 1, (str)parking time end 1], ... , (int)total parking spaces}
myDict = {}

# Extract data from one of the databases and put it in the dictionary myDict
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

# Extract data from another database and put it in the dictionary myDict
data2 = json.loads(urlopen("https://data.sbb.ch/api/records/1.0/search/?dataset=parkrail-sale-backend&q=&rows=100&facet=start&facet=end&facet=sales_channel&facet=created_at").read())
for i in data2['records']:
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
data3 = json.loads(urlopen("https://data.sbb.ch/api/records/1.0/search/?dataset=mobilitat&q=&rows=832&facet=stationsbezeichnung&facet=parkrail_anzahl&facet=parkrail_preis_tag&facet=parkrail_preis_monat&facet=parkrail_pflichtig_zeit1&facet=parkrail_bemerkung&facet=railtaxitext&facet=mietvelo_bezeichnung&facet=veloparking_status_d&facet=veloparking_abschliessbar").read())
for i in data3['records']:
    if 'parkrail_anzahl' in i['fields']:
        add_element(myDict, i['fields']['bezeichnung_offiziell'], i['fields']['parkrail_anzahl'])

# Examples of extracting data (assuming data is correct and valid)
#print(myDict['Zug']) #Shows all relevant information pertaining to the specified station
#print(myDict['Zug'][0]) #Shows one entry of a occupied time slot in the specified station
#print(myDict['Zug'][0][0]) #Shows one entry's start or end time of a specified time slot in the specified station
#print(myDict['Zug'][-1]) #Shows the total parking spaces at the specified station

def check_date_in_range(station, date):
    x = 0
    for i in myDict[station][:-1]:
        if isinstance(i, float):
            continue
        if i[0] <= pytz.UTC.localize(date) <= i[1]:
            x = x + 1
    return x

# Check occupancy of specified time slot at station
test_station1 = 'Zug'
test_date1 = '2019-10-12 22:14'
date_pattern1 = '%Y-%m-%d %H:%M'
test_date1 = datetime.datetime.strptime(test_date1, date_pattern1)
cars_parked = check_date_in_range(test_station1, test_date1)

occupancy = cars_parked / myDict[test_station1][-1]
print("{}% | {} out of {} cars.".format(round(occupancy*100, 2), cars_parked, int(myDict[test_station1][-1])))

def allweekdays(year, weekday):
    d = datetime.datetime(year, 1, 1, 0, 0, 0)
    d += datetime.timedelta(days = weekday - d.weekday())
    if d.month == 12:
        d += datetime.timedelta(days = 7)
    while d.year == year:
        yield d
        d += datetime.timedelta(days = 7)

# Simple prediction that just checks the similarity in hours of every week day
def simple_prediction(station, date):
    date_pattern = '%Y-%m-%d %H:%M'
    date = datetime.datetime.strptime(date, date_pattern)
    weekday = date.weekday()
    hour = date.hour
    year = date.year
    avg = 0
    x = 0
    
    sameyear = []
    oneyearago = []
    twoyearsago = []
    #threeyearsago = []
    #fouryearsago = []
    #fiveyearsago = []

    for dates in allweekdays(year, weekday):
        sameyear.append(dates)
    for dates in allweekdays(year - 1, weekday):
        oneyearago.append(dates)
    for dates in allweekdays(2017, 5):
        twoyearsago.append(dates)
    #for dates in allweekdays(year - 3, weekday):
    #    threeyearsago.append(dates)
    #for dates in allweekdays(year - 4, weekday):
    #    fouryearsago.append(dates)
    #for dates in allweekdays(year - 5, weekday):
    #    fiveyearsago.append(dates)

    for weekdays in sameyear:
        if (weekdays < date):
            test_time = weekdays + datetime.timedelta(hours=hour)
            test_cars_parked = check_date_in_range(station, test_time)
            test_occupancy = test_cars_parked / myDict[station][-1]
            avg = avg + test_occupancy
            x = x + 1
        else:
            break
    for weekdays in oneyearago:
        test_time = weekdays + datetime.timedelta(hours=hour)
        test_cars_parked = check_date_in_range(station, test_time)
        test_occupancy = test_cars_parked / myDict[station][-1]
        avg = avg + test_occupancy
        x = x + 1
    for weekdays in twoyearsago:
        test_time = weekdays + datetime.timedelta(hours=hour)
        test_occupancy = check_date_in_range(station, test_time) / myDict[station][-1]
        avg = avg + test_occupancy
        x = x + 1
    avg = avg / x

    return avg #Take note, this isn't multiplied by 100 to convert to percentage



test_prediction = simple_prediction('Zug', '2019-10-12 22:14')


print(test_prediction)
print(myDict['Zug'][-1])







#Step 1:
#figure out occupancy at any given time
#input any time return occupany

#Step 2:
#passenger frequency, number of trains
#passenger frequency, number of parking solds (what is the percentage of people travelling who need parking)

#Step 3:
#form the simple model so we can tweak weights

#Step 4:
#weather data
#seasonal data


# Only shows in the more detailed databases for the stations of SOME (we only have for Rapperswil)

