import numpy as np 
import matplotlib.pyplot as plt
plt.ion() 
import pandas as pd 
from datetime import date, timedelta, datetime

path = '/mnt/c/Google_Drive/1_Nutrient_Share/1_Projects_NUTRIENTS/Modeling/SF_Bay_DFM/Meteorology_Data_for_BAHM/Precipitation/daily/'
file = "precipitation_data_all.csv"

# set up dictionaries for file name, station name, adjust factor, 
stations = {
    "USC00040693": dict(name="Berkeley",
                        daily_fill=["USC00049185"],
                        daily_fill_name="Upper San Leandro Fltr",
                        adjust_factor=1.03),
    "USC00042934": dict(name="Fairfield",
                        daily_fill=[],
                        daily_fill_name="",
                        adjust_factor=1),
    "USC00044500": dict(name="Kentfield",
                        daily_fill=[],
                        daily_fill_name="",
                        adjust_factor=1),
    "USC00044997": dict(name="Livermore",
                        daily_fill=["USW00023285"],
                        daily_fill_name="Livermore Municipal Airport",
                        adjust_factor=1),
    "USC00045933": dict(name="Mount Hamilton",
                        daily_fill=["US1CASC0007"],
                        daily_fill_name="San Jose 4.6 NE",
                        daily_fill2=["US1CASC0012"],
                        daily_fill_name2="San Jose 3.5 ENE",
                        adjust_factor=1.51),
    "USC00045123": dict(name="Los Gatos",
                        daily_fill=["US1CASC0018"],
                        daily_fill_name="San Jose 3.0 WSW",
                        daily_fill2=["US1CASC0011"],
                        daily_fill_name2="Cambrian Park 2.2",
                        adjust_factor=1.43),
    "USC00045378": dict(name="Martinez Water Plant",
                        daily_fill=["US1CACC0001"],
                        daily_fill_name="Martinez 0.8 SSE",
                        adjust_factor=0.98),
    "USC00046074": dict(name="Napa State Hospital",
                        daily_fill=["USC00046826"],
                        daily_fill_name="Petaluma Airport",
                        adjust_factor=1.01),
    "USC00046144": dict(name="Newark",
                        daily_fill=["USC00043244"],
                        daily_fill_name="Fremont",
                        adjust_factor=0.98),
    "USC00046646": dict(name="Palo Alto",
                        daily_fill=["USC00047339"],
                        daily_fill_name="Redwood City",
                        adjust_factor=0.81),
    "USC00046826": dict(name="Petaluma Airport",
                        daily_fill=["US1CASN0039"],
                        daily_fill_name="Petaluma 1.8 WSW",
                        adjust_factor=1),
    "USC00047339": dict(name="Redwood City",
                        daily_fill=["USC00046646"],
                        daily_fill_name="Palo Alto",
                        adjust_factor=1.24),
    "USC00047643": dict(name="Saint Helena",
                        daily_fill=["USC00047646"],
                        daily_fill_name="Saint Helena 4 WSW",
                        adjust_factor=0.82),
    "US1CASC0018": dict(name="San Jose",
                        daily_fill=["US1CASC0032"],
                        daily_fill_name="San Jose 6.2 W",
                        daily_fill2=["US1CASC0052"],
                        daily_fill_name2="SAN JOSE 1.9 SW",
                        adjust_factor=1),
    "USC00047880": dict(name="San Rafael Civic Center",
                        daily_fill=["USC00044500"],
                        daily_fill_name="Kentfield",
                        adjust_factor=0.85),
    "USW00023272": dict(name="San Francisco Downtown",
                        daily_fill=["US1CASF0004"],
                        daily_fill_name="San Francisco 1.1 SW",
                        adjust_factor=1),
    "USW00023234": dict(name="San Francisco International Airport",
                        daily_fill=[],
                        daily_fill_name="",
                        adjust_factor=1),
    "USC00048351": dict(name="Sonoma",
                        daily_fill=["USC00046826"],
                        daily_fill_name="Petaluma Airport",
                        adjust_factor=1.17),
    "USC00049185": dict(name="San Leandro",
                        daily_fill=["US1CAAL0030"],
                        daily_fill_name="Oakland 1.2 ENE",
                        adjust_factor=1),
    "US1CASM0022": dict(name="Woodside",
                        daily_fill=["USC00047339"],
                        daily_fill_name="Redwood City",
                        adjust_factor=1.46)
}

station_keys = list(stations.keys())

def load_data(dat, station):
    """ load precipitation data from full file of all stations
    """
    ind = np.where(dat["STATION"]==station)[0]
    dates = dat["DATE"][ind].values
    precip = dat["PRCP"][ind].values
    datet = [datetime.strptime(str(dates[i]), '%Y-%m-%d') for i in range(len(dates))]
    dated = [datet[i].date() for i in range(len(datet))]
    return datet, dated, precip 

def find_missing_dates(dates, dstart=date(2017,1,1), dend=date(2018,1,1)):
    """ find missing dates 
    """
    date_set = set(dstart + timedelta(x) for x in range((dend - dstart).days+1))
    missing = sorted(date_set - set(dates))
    return missing

def fill_data(datetimes1, datetimes2, precip1, precip2, missing, ratio):
    """ takes datetimes and precipitation 
        data from two different stations
        and fills in the daily data 
    """
    dated2 = [datetimes2[i].date() for i in range(len(datetimes2))]
    dind = np.where(np.in1d(dated2, missing)==True)[0]
    dates_all = np.zeros(len(datetimes1)+len(dind)).tolist()
    precip_all = np.zeros(len(datetimes1)+len(dind))
    j=0
    for i in range(len(precip_all)):
        if i < len(datetimes1):
            dates_all[i]=datetimes1[i]
            precip_all[i]=precip1[i]
        if i >= len(datetimes1):
            dates_all[i]=datetimes2[dind[j]]
            precip_all[i]=precip2[dind[j]]*ratio
            j+=1
    dates = sorted(dates_all)
    precip = np.asarray([p for _,p in sorted(zip(dates_all, precip_all))])
    return dates, precip

def write_missing(missing, filename):
    """ write missing dates to a txt file
    """
    f0 = open(filename, "w")
    f0.write("missing dates")
    f0.write('\n')
    for m in missing:
        f0.write(str(m))
        f0.write('\n')
    f0.close()

def write_processed(filename, date, precip):
    """ write out data into processed format
    """
    f1 = open(filename, "w")
    f1.write("Year,Month,Day,PRCP\n")
    for d in range(len(date)):
        f1.write("%d,%d,%d,%f\n" % (date[d].year, date[d].month, date[d].day, precip[d]))
    f1.close()

def process_precip_data(filepath, station_keys, station_dict):
    """ completes full processing of data 
         -- fills in daily data and writes out to csv
    """
    dat = pd.read_csv(filepath)
    for key in station_keys:
        datet, dated, precip = load_data(dat, key) 
        missing = find_missing_dates(dated)
        if len(missing)>0:
            write_missing(missing, path+station_dict[key]["name"]+" Missing0.txt")
            mstation = station_dict[key]["daily_fill"][0] 
            ratio = station_dict[key]["adjust_factor"]
            mdatet, mdated, mprecip = load_data(dat, mstation)
            datet, precip = fill_data(datet, mdatet, precip, mprecip, missing, ratio)
        write_processed(path+"processed/"+station_dict[key]["name"]+".csv", datet, precip)
        #write_processed(path+"processed/"+key+".csv", datet, precip)

process_precip_data(path+file, station_keys, stations)

### add check if all data missing data has been filled
for key in station_keys:
    #datet, dated, precip = load_data(data, key)
    dat = pd.read_csv(path+"processed/"+stations[key]["name"]+".csv")
    dates = [datetime(dat["Year"][i], dat["Month"][i], dat["Day"][i]).date() for i in range(len(dat["Year"]))]
    datet = [datetime.combine(dates[i], datetime.min.time()) for i in range(len(dates))]
    precip = dat["PRCP"].values
    missing = find_missing_dates(dates)
    if len(missing)>0:
        write_missing(missing, path+stations[key]["name"]+" Missing1.txt")

def process_precip_file(file, fill_file, key, station_dict):
    data = pd.read_csv(fill_file)
    dat = pd.read_csv(file)
    dates = [datetime(dat["Year"][i], dat["Month"][i], dat["Day"][i]).date() for i in range(len(dat["Year"]))]
    datet = [datetime.combine(dates[i], datetime.min.time()) for i in range(len(dates))]
    precip = dat["PRCP"].values
    missing = find_missing_dates(dates)
    if len(missing)>0:
        write_missing(missing, path+station_dict[key]["name"]+" Missing1.txt")
        mstation = station_dict[key]["daily_fill2"][0] 
        ratio = station_dict[key]["adjust_factor"]
        mdatet, mdated, mprecip = load_data(data, mstation)
        datet, precip = fill_data(datet, mdatet, precip, mprecip, missing, ratio)
    write_processed(file, datet, precip)
 
#process_precip_file(path+"processed/"+"USC00045123.csv", path+file, "USC00045123", stations)
#process_precip_file(path+"processed/"+"USC00045933.csv", path+file, "USC00045933", stations)
#process_precip_file(path+"processed/"+"US1CASC0018.csv", path+file, "US1CASC0018", stations)
process_precip_file(path+"processed/"+"Los Gatos.csv", path+file, "USC00045123", stations)
process_precip_file(path+"processed/"+"Mount Hamilton.csv", path+file, "USC00045933", stations)
process_precip_file(path+"processed/"+"San Jose.csv", path+file, "US1CASC0018", stations)

### add check if all data missing data has been filled
for key in station_keys:
    #datet, dated, precip = load_data(data, key)
    dat = pd.read_csv(path+"processed/"+stations[key]["name"]+".csv")
    dates = [datetime(dat["Year"][i], dat["Month"][i], dat["Day"][i]).date() for i in range(len(dat["Year"]))]
    datet = [datetime.combine(dates[i], datetime.min.time()) for i in range(len(dates))]
    precip = dat["PRCP"].values
    missing = find_missing_dates(dates)
    if len(missing)>0:
        write_missing(missing, path+stations[key]["name"]+" Missing2.txt")
