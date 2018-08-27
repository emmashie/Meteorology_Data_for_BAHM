import numpy as np 
import matplotlib.pyplot as plt
plt.ion() 
import pandas as pd 
from datetime import date, timedelta, datetime

path = "/Users/emmashienuss/Google_Drive/1_Nutrient_Share/1_Projects_NUTRIENTS/Modeling/SF_Bay_DFM/Meteorology_Data_for_BAHM/Precipitation/hourly/"
#path = "/mnt/c/Google_Drive/1_Nutrient_Share/1_Projects_NUTRIENTS/Modeling/SF_Bay_DFM/Meteorology_Data_for_BAHM/Precipitation/hourly/"
files = ["WBAN00228.csv", "WBAN00320.csv", "WBAN23202.csv", "WBAN23230.csv",
         "WBAN23234.csv", "WBAN23237.csv", "WBAN23244.csv", "WBAN23254.csv", 
         "WBAN23272.csv", "WBAN93227.csv", "WBAN93228.csv", "WBAN93231.csv",
         "WBAN93241.csv"]

def write_processed(filename, date, precip):
    """ write out data into processed format
        and convert mm precip to inches 
    """
    f1 = open(filename, "w")
    f1.write("Year,Month,Day,Hour,HOURLYPrecip\n")
    for d in range(len(date)):
        f1.write("%d,%d,%d,%d,%f\n" % (date[d].year, date[d].month, date[d].day, date[d].hour, precip[d]/25.4))
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


def check_doubles(valid_dates, valid_precip, dstart = datetime(2017,1,1), dend = datetime(2018,1,1)):
    delta = dend - dstart 
    valid_dates = np.asarray(valid_dates)
    valid_days = np.asarray([d.date() for d in valid_dates])
    for i in range(delta.days):
        day = dstart + timedelta(days=i)
        ind = np.where(valid_days==day.date())[0]
        valid_day = valid_dates[ind]
        hours = np.asarray([d.hour for d in valid_day])
        double = np.where((hours[1:]-hours[:-1])==0)
        if len(double)>0:
            valid_dates = np.delete(valid_dates, ind[double])
            valid_precip = np.delete(valid_precip, ind[double])
            valid_days = np.delete(valid_days, ind[double])
    return valid_dates, valid_precip

def find_missing_dates(dates, dstart=datetime(2017,1,1), dend=datetime(2018,1,1)):
    """ find missing dates 
    """
    date_set = set(dstart + timedelta(hours=x) for x in range((dend-dstart).days*24+1))
    missing = sorted(date_set - set(dates))
    return missing

def process_data(path, file, dstart = datetime(2017,1,1), dend = datetime(2018,1,1)):
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
    valid_dates, valid_precip = check_doubles(valid_dates, valid_precip, dstart, dend)
    h_dates = np.asarray([datetime(vd.year, vd.month, vd.day, vd.hour) for vd in valid_dates])
    m_dates = np.asarray(find_missing_dates(h_dates))
    m_precip = np.zeros(len(m_dates))
    dates_all = np.concatenate((h_dates, m_dates))
    precip_all = np.concatenate((valid_precip, m_precip))
    Adates = sorted(dates_all)
    Aprecip = np.asarray([p for _,p in sorted(zip(dates_all, precip_all))])
    write_processed(path+"processed/"+file, Adates, Aprecip)
    return 


for file in files:
    process_data(path, file)


