import numpy as np 
import pandas as pd 
from datetime import date, timedelta, datetime

path = '/mnt/c/Google_Drive/1_Nutrient_Share/1_Projects_NUTRIENTS/Modeling/SF_Bay_DFM/Meteorology_Data_for_BAHM/CIMIS/'
files = ["CIMIS47.csv", "CIMIS144.csv", "CIMIS170.csv", "CIMIS171.csv", "CIMIS213.csv"]

# set up dictionaries for file name, station name, adjust factor, 
station_info = {
    "CIMIS47": dict(zone="zone14",
                    fill_name="CIMIS144.csv",
                    fill_zone="zone4"),
    "CIMIS144": dict(zone="zone5",
                     fill_name="CIMIS47.csv",
                     fill_zone="zone14"),
    "CIMIS170": dict(zone="zone8",
                     fill_name="CIMIS47.csv",
                     fill_zone="zone14"),
    "CIMIS171": dict(zone="zone6",
                     fill_name="CIMIS47.csv",
                     fill_zone="zone14"),
    "CIMIS213": dict(zone="zone1",
                     fill_name="CIMIS47.csv",
                     fill_zone="zone14")
}

def write_processed(filename, date, eto):
    """ write out data into processed format
    """
    f1 = open(filename, "w")
    f1.write("Year,Month,Day,Hour,ETo (in)\n")
    for d in range(len(date)):
        f1.write("%d,%d,%d,%d,%f\n" % (date[d].year, date[d].month, date[d].day, date[d].hour, eto[d]))
    f1.close()

def clean_up_hrmn(hrmn):
    hrmn = [str(h) for h in hrmn]
    for i in range(len(hrmn)):
        hrmn[i]=str(int(hrmn[i])-100)
        if len(hrmn[i])==1:
            hrmn[i] ='0'+hrmn[i]+'00'
        if len(hrmn[i])==2:
            hrmn[i] = '00' + hrmn[i]
        if len(hrmn[i])==3:
            hrmn[i] = '0' + hrmn[i]
    return hrmn 


def fill_adjust(station, fill_file, month, ind):
    zone1 = np.array([0.93, 1.40, 2.48, 3.30, 4.03, 4.50, 4.65, 4.03, 3.30, 2.48, 1.20, 0.62])
    zone5 = np.array([0.93, 1.68, 2.79, 4.20, 5.58, 6.30, 6.51, 5.89, 4.50, 3.10, 1.50, 0.93])
    zone6 = np.array([1.86, 2.24, 3.41, 4.80, 5.58, 6.30, 6.51, 6.20, 4.80, 3.72, 2.40, 1.86])
    zone8 = np.array([1.24, 1.68, 3.41, 4.80, 6.20, 6.90, 7.44, 6.51, 5.10, 3.41, 1.80, 0.93])
    zone14 = np.array([1.55, 2.24, 3.72, 5.10, 6.82, 7.80, 8.68, 7.75, 5.70, 4.03, 2.10, 1.24])
    fill_dat = pd.read_csv(fill_file)
    fill = fill_dat["ETo (in)"].values[ind]
    if station=="CIMIS47":
        ratio = zone14/zone5 
    if station=="CIMIS144":
        ratio = zone5/zone14
    if station=="CIMIS170":
        ratio = zone8/zone14
    if station=="CIMIS171":
        ratio = zone6/zone14
    if station=="CIMIS213":
        ratio = zone1/zone14
    return fill*ratio[month-1]


def write_missing(missing, dates, filename):
    """ write missing dates to a txt file
    """
    f0 = open(filename, "w")
    f0.write("missing dates")
    f0.write('\n')
    for m in missing:
        f0.write(str(dates[m]))
        f0.write('\n')
    f0.close()


for file in files:
    dat = pd.read_csv(path+file)
    dates = dat["Date"].values
    hrmn = dat["Hour (PST)"].values
    hrmn = clean_up_hrmn(hrmn)
    datestr = [str(dates[i])+" "+str(hrmn[i]) for i in range(len(dates))]
    dates = [datetime.strptime(d,"%m/%d/%Y %H%M") for d in datestr]
    eto = dat["ETo (in)"].values
    missing = np.where(np.isnan(eto)==True)[0]
    if len(missing)>0:
        write_missing(missing, datestr, path+file[:-4]+".txt")
        for i in range(len(missing)):
            eto[missing[i]] = fill_adjust(file[:-4], path+station_info[file[:-4]]['fill_name'], dates[missing[i]].month, missing[i])
    write_processed(path+"processed/"+file, dates, eto)