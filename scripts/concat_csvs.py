import os
import glob
import pandas as pd

#set working directory
os.chdir("/Users/vivianjin/Documents/mobi_bike_share_project")

#find all csv files in the folder
#use glob pattern matching -> extension = 'csv'
#save result in list -> all_filenames
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#print(all_filenames)

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f, skiprows=1) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "Mobi_System_Data_Combined.csv", index=False, encoding='utf-8-sig')