import numpy as np 
import matplotlib.pyplot as plt
plt.ion() 
import pandas as pd 
from datetime import date, timedelta, datetime

path = "/mnt/c/Google_Drive/1_Nutrient_Share/1_Projects_NUTRIENTS/Modeling/SF_Bay_DFM/Meteorology_Data_for_BAHM/Precipitation/hourly/"
files = ["WBAN00320.csv", "WBAN23244.csv", "WBAN23293.csv", "WBAN23213.csv", "WBAN23254.csv",
         "WBAN93227.csv", "WBAN23230.csv", "WBAN23272.csv", "WBAN93228.csv", "WBAN23234.csv",
         "WBAN23285.csv", "WBAN99999.csv"]

def write_processed(filename, date, precip):
    """ write out data into processed format
    """
    f1 = open(filename, "w")
    f1.write("Year,Month,Day,Hour,HOURLYPrecip\n")
    for d in range(len(date)):
        f1.write("%d,%d,%d,%d,%f\n" % (date[d].year, date[d].month, date[d].day, date[d].hour, precip[d]))
    f1.close()

def clean_up_hrmn(hrmn):
    hrmn = [str(h) for h in hrmn]
    for i in range(len(hrmn)):
        hrmn[i]=str(hrmn[i])
        if len(hrmn[i])==1:
            hrmn[i] ='0'+hrmn[i]+'00'
        if len(hrmn[i])==2:
            hrmn[i] = '00' + hrmn[i]
        if len(hrmn[i])==3:
            hrmn[i] = '0' + hrmn[i]
    return hrmn 


def process_data(path, file, dstart = datetime(2016,8,1), dend = datetime(2017,10,1)):
    dat = pd.read_csv(path+file)
    date = dat["Date"].values
    date = [int(d) for d in date]
    hrmn = dat["HrMn"].values
    hrmn = [int(h) for h in hrmn]
    hrmn = clean_up_hrmn(hrmn)
    precip = dat["Amt"].values
    datehrmn = [str(date[i])+str(hrmn[i]) for i in range(len(date))]
    dates = [datetime.strptime(d,"%Y%m%d%H%M") for d in datehrmn]
    valid_dates = [date for date in dates if date >= dstart and date <= dend]
    valid_precip = [precip[i] for i in range(len(precip)) if dates[i] >= dstart and dates[i] <= dend]
    write_processed(path+"processed/"+file, valid_dates, valid_precip)
    return 

for file in files:
    process_data(path, file)


