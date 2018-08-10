import numpy as np 
import pandas as pd 
from datetime import date, timedelta, datetime

path = '/mnt/c/Google_Drive/1_Nutrient_Share/1_Projects_NUTRIENTS/Modeling/SF_Bay_DFM/Meteorology_Data_for_BAHM/CIMIS/'
files = ["CIMIS47.csv", "CIMIS144.csv", "CIMIS170.csv", "CIMIS171.csv", "CIMIS213.csv"]

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

def find_missing_dates(dates, dstart=datetime(2017,1,1,1,0), dend=datetime(2018,1,1,1,0)):
    """ find missing dates 
    """
    date_set = set(dstart + timedelta(hours=x) for x in range((dend - dstart).days*24+1))
    missing = sorted(date_set - set(dates))
    return missing

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

for file in files:
    dat = pd.read_csv(path+file)
    dates = dat["Date"].values
    hrmn = dat["Hour (PST)"].values
    hrmn = clean_up_hrmn(hrmn)
    datestr = [str(dates[i])+" "+str(hrmn[i]) for i in range(len(dates))]
    dates = [datetime.strptime(d,"%m/%d/%Y %H%M") for d in datestr]
    missing = find_missing_dates(dates)
    if len(missing)>0:
        write_missing(missing, path+file[:-4]+".txt")
    eto = dat["ETo (in)"].values
    write_processed(path+"processed/"+file, dates, eto)