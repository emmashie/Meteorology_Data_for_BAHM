import numpy as np 
import matplotlib.pyplot as plt
plt.ion() 
import pandas as pd 
from datetime import date, timedelta, datetime

path = '/mnt/c/Google_Drive/1_Nutrient_Share/1_Projects_NUTRIENTS/Modeling/SF_Bay_DFM/Meteorology_Data_for_BAHM/Precipitation/daily/'
file = "precipitation_data_all.csv"
station_keys = ["USC00040693", "USC00042934", "USC00044500", "USC00044997",
                "USC00045123", "USC00045378", "USC00045933", "USC00046074",
                "USC00046144", "USC00046646", "USC00046826", "USC00047339",
                "USC00047643", "USC00047880", "USC00048351", "USC00049185"]


# set up dictionaries for file name, station name, adjust factor, 
stations = {
    "USC00040693": dict(name="Berkeley",
                        daily_fill=["USC00049185"],
                        daily_fill_name="Upper San Leandro Fltr",
                        adjust_factor=1.03,
                        hourly=["047772.xlsx","23230.xlsx"]),
    "USC00042934": dict(name="Fairfield",
                        daily_fill=[],
                        daily_fill_name="",
                        adjust_factor=1,
                        hourly=["042935.xlsx", "93227.xlsx"]),
    "USC00044500": dict(name="Kentfield",
                        daily_fill=[],
                        daily_fill_name="",
                        adjust_factor=1,
                        hourly=["046826.xlsx", "047772.xlsx", "93227.xlsx"]),
    "USC00044997": dict(name="Livermore",
                        daily_fill=[],
                        daily_fill_name="",
                        adjust_factor=1,
                        hourly=["044995.xlsx", "93228.xlsx"]),
    "USC00045123": dict(name="Los Gatos",
                        daily_fill=["US1CASC0018"],
                        daily_fill_name="San Jose 3.0 WSW",
                        adjust_factor=1.43,
                        hourly=["047821.xlsx"]),
    "USC00045378": dict(name="Martinez",
                        daily_fill=["US1CACC0001"],
                        daily_fill_name="Martinez 0.8 SSE",
                        adjust_factor=0.98,
                        hourly=["042935.xlsx", "23254.xlsx"]),
    "USC00045933": dict(name="Mount Hamilton",
                        daily_fill=["US1CASC0007"],
                        daily_fill_name="San Jose 4.6 NE",
                        adjust_factor=1.51,
                        hourly=["047821.xlsx"]),
    "USC00046074": dict(name="Napa",
                        daily_fill=["USC00046826"],
                        daily_fill_name="Petaluma Airport",
                        adjust_factor=1.01,
                        hourly=["046826.xlsx", "042935.xlsx", "93227.xlsx"]),
    "USC00046144": dict(name="Newark",
                        daily_fill=["USC00043244"],
                        daily_fill_name="Freemont",
                        adjust_factor=0.98,
                        hourly=["047821.xlsx", "23244.xlsx", "93228.xlsx"]),
    "USC00046646": dict(name="Palo Alto",
                        daily_fill=["USC00047339"],
                        daily_fill_name="Redwood City",
                        adjust_factor=0.81,
                        hourly=["047821.xlsx", "047769.xlsx", "23244.xlsx"]),
    "USC00046826": dict(name="Petaluma Airport",
                        daily_fill=["US1CASN0039"],
                        daily_fill_name="Petaluma 1.8 WSW",
                        adjust_factor=1,
                        hourly=["046826.xlsx", "93227.xlsx"]),
    "USC00047339": dict(name="Redwood City",
                        daily_fill=["USC00046646"],
                        daily_fill_name="Palo Alto",
                        adjust_factor=1.24,
                        hourly=["047769.xlsx", "23244.xlsx"]),
    "USC00047643": dict(name="Saint Helena",
                        daily_fill=["USC00047646"],
                        daily_fill_name="Saint Helena 4 WSW",
                        adjust_factor=0.82,
                        hourly=["047646.xlsx", "046826.xlsx", "93227.xlsx"]),
    "USC00047880": dict(name="San Rafael",
                        daily_fill=["USC00044500"],
                        daily_fill_name="Kentfield",
                        adjust_factor=0.85,
                        hourly=["046826.xlsx", "047772.xlsx"]),
    "USC00048351": dict(name="Sonoma",
                        daily_fill=["USC00046826"],
                        daily_fill_name="Petaluma Airport",
                        adjust_factor=1.17,
                        hourly=["046826.xlsx", "047646.xlsx", "93227.xlsx"]),
    "USC00049185": dict(name="San Leandro",
                        daily_fill=[],
                        daily_fill_name="",
                        adjust_factor=1,
                        hourly=["047772.xlsx", "23230.xlsx", "93228.xlsx"])
}

def load_data(dat, station):
    ind = np.where(dat["STATION"]==station)[0]
    dates = dat["DATE"][ind].values
    precip = dat["PRCP"][ind].values
    datet = [datetime.strptime(str(dates[i]), '%Y-%m-%d') for i in range(len(dates))]
    dated = [datet[i].date() for i in range(len(datet))]
    return datet, dated, precip 

def find_missing_dates(dates):
    date_set = set(dates[0] + timedelta(x) for x in range((dates[-1] - dates[0]).days))
    missing = sorted(date_set - set(dates))
    return missing

def fill_data(datetimes1, datetimes2, precip1, precip2, missing, ratio):
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

dat = pd.read_csv(path+file)
i=0
for key in station_keys:
    datet, dated, precip = load_data(dat, key)
    missing = find_missing_dates(dated)
    if len(missing)>0:
        # write missing dates to file
        f0 = open(path+key+"_missing_dates0.txt", "w")
        f0.write("missing dates")
        f0.write('\n')
        for m in missing:
            f0.write(str(m))
            f0.write('\n')
        f0.close()
        mstation = stations[key]["daily_fill"][0] 
        ratio = stations[key]["adjust_factor"]
        mdatet, mdated, mprecip = load_data(dat, mstation)
        datet, precip = fill_data(datet, mdatet, precip, mprecip, missing, ratio)
    f1 = open(path+key+".csv", "w")
    f1.write("Year,Month,Day,PRCP \n")
    for d in range(len(datet)):
        f1.write("%d, %d, %d, %f \n" % (datet[d].year, datet[d].month, datet[d].day, precip[d]))
    f1.close()
    i+=1

### add check if all data missing data has been filled
for key in station_keys:
    dat = pd.read_csv(path+key+".csv")
    dates = [datetime(dat["Year"][i], dat["Month"][i], dat["Day"][i]).date() for i in range(len(dat["Year"]))]
    missing = find_missing_dates(dates)
    if len(missing)>0:
        f0 = open(path+key+"_missing_dates1.txt", "w")
        f0.write("missing dates")
        f0.write('\n')
        for m in missing:
            f0.write(str(m))
            f0.write('\n')
        f0.close()


