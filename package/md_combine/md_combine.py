import glob
import pandas as pd

df_csv_append = pd.DataFrame()

csv_files = glob.glob('.\\Outputs\\*.{}'.format('csv'))
print(csv_files)

df_csv = pd.concat([pd.read_csv(file) for file in csv_files ], ignore_index=True)

df_csv.to_csv('./Outputs/indonesia2018.csv')