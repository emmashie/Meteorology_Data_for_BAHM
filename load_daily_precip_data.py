import numpy as np 
import matplotlib.pyplot as plt
plt.ion() 
import pandas as pd 
from datetime import date, timedelta, datetime

path = '/mnt/c/Google_Drive/1_Nutrient_Share/1_Projects_NUTRIENTS/Modeling/SF_Bay_DFM/Meteorology_Data_for_BAHM/Precipitation/daily/'
daily_precip_files = ["USC00040693.xlsx", "USC00042934.xlsx", "USC00044500.xlsx", "USC00044997.xlsx",
                      "USC00045123.xlsx", "USC00045378.xlsx", "USC00045933.xlsx", "USC00046074.xlsx",
                      "USC00046144.xlsx", "USC00046646.xlsx", "USC00046826.xlsx", "USC00047339.xlsx",
                      "USC00047643.xlsx", "USC00047880.xlsx", "USC00048351.xlsx", "USC00049185.xlsx"]

# set up dictionaries for file name, station name, adjust factor, 

stations = {
    "USC00040693.xlsx": dict(name="Berkeley",
                             daily_fill=["USC00049185.xlsx"],
                             adjust_factor=1.03,
                             hourly=["047772.xlsx","23230.xlsx"]),
    "USC00042934.xlsx": dict(name="Fairfield",
                             daily_fill=[],
                             adjust_factor=1,
                             hourly=["042935.xlsx", "93227.xlsx"]),
    "USC00044500.xlsx": dict(name="Kentfield",
                             daily_fill=[],
                             adjust_factor=1,
                             hourly=["046826.xlsx", "047772.xlsx", "93227.xlsx"]),
    "USC00044997.xlsx": dict(name="Livermore",
                             daily_fill=[],
                             adjust_factor=1,
                             hourly=["044995.xlsx", "93228.xlsx"]),
    "USC00045123.xlsx": dict(name="Los Gatos",
                             daily_fill=["USW00023293.xlsx"],
                             adjust_factor=1.43,
                             hourly=["047821.xlsx"]),
    "USC00045378.xlsx": dict(name="Martinez",
                             daily_fill=[],
                             adjust_factor=0.98,
                             hourly=["042935.xlsx", "23254.xlsx"]),
    "USC00045933.xlsx": dict(name="Mount Hamilton",
                             daily_fill=["USW00023293.xlsx"],
                             adjust_factor=1.51,
                             hourly=["047821.xlsx"]),
    "USC00046074.xlsx": dict(name="Napa",
                             daily_fill=[],
                             adjust_factor=1.01,
                             hourly=["046826.xlsx", "042935.xlsx", "93227.xlsx"]),
    "USC00046144.xlsx": dict(name="Newark",
                             daily_fill=[],
                             adjust_factor=0.98,
                             hourly=["047821.xlsx", "23244.xlsx", "93228.xlsx"]),
    "USC00046646.xlsx": dict(name="Palo Alto",
                             daily_fill=[],
                             adjust_factor=0.81,
                             hourly=["047821.xlsx", "047769.xlsx", "23244.xlsx"]),
    "USC00046826.xlsx": dict(name="Petaluma",
                             daily_fill=[],
                             adjust_factor=1,
                             hourly=["046826.xlsx", "93227.xlsx"]),
    "USC00047339.xlsx": dict(name="Redwood City",
                             daily_fill=[""],
                             adjust_factor=1.24,
                             hourly=["047769.xlsx", "23244.xlsx"]),
    "USC00047643.xlsx": dict(name="Saint Helena",
                             daily_fill=["USC00047646.xlsx"],
                             adjust_factor=0.82,
                             hourly=["047646.xlsx", "046826.xlsx", "93227.xlsx"]),
    "USC00047880.xlsx": dict(name="San Rafael",
                             daily_fill=["USC00044500.xlsx"],
                             adjust_factor=0.85,
                             hourly=["046826.xlsx", "047772.xlsx"]),
    "USC00048351.xlsx": dict(name="Sonoma",
                             daily_fill=["USC00046826.xlsx"],
                             adjust_factor=1.17,
                             hourly=["046826.xlsx", "047646.xlsx", "93227.xlsx"]),
    "USC00049185.xlsx": dict(name="San Leandro",
                             daily_fill=["USC00049185.xlsx"],
                             adjust_factor=1,
                             hourly=["047772.xlsx", "23230.xlsx", "93228.xlsx"])
}


for files in daily_precip_files:
    file = path+files
    f = open(path+file[-16:-5]+"_missing_dates.txt", "w")
    dat = pd.read_excel(file)
    dates = dat["DATE"]
    precip = dat["PRCP"]

    # date strings to datetimes
    datet = [datetime.strptime(str(dates[i]), '%Y-%m-%d %H:%M:%S') for i in range(len(dates))]
    dated = [datet[i].date() for i in range(len(datet))]

    # find missing dates
    date_set = set(dated[0] + timedelta(x) for x in range((dated[-1] - dated[0]).days))
    missing = sorted(date_set - set(dated))
    f.write("missing dates")
    f.write('\n')
    for m in missing:
        f.write(str(m))
        f.write('\n')
    f.close()

  