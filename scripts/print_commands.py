years = ['2018', '2019', '2020', '2021']
dates = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

for year in years:
    for i in dates:
        print("""load data local infile '/Users/vivianjin/Documents/mobi_bike_share_project/Mobi_System_Data_{year}-{date}.csv' into table Mobi_System_Data FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\\n' IGNORE 1 LINES \
        (departure_time, return_time, bike, departure_station, return_station, formula, covered_distance_m, duration_sec, departure_battery_voltage_mV, return_battery_voltage_mV, departure_temperature_C, return_temperature_C, stopover_duration_sec, num_stopovers);""".format(year=year.replace('"', ''), date=i.replace('"', '')))
