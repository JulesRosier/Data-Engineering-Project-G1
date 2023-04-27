import glob
import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
MYSQL_UPLOADS = "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\"
CSV_PATH = os.environ.get("ONEDRIVE_PATH")

print('Making All.csv... ', end='')
all_data = glob.glob(os.path.join(CSV_PATH, "All_*.csv"))
df = pd.concat(map(pd.read_csv, all_data), ignore_index=True)
df.to_csv(os.path.join(MYSQL_UPLOADS, "All.csv"), index=False)
print('DONE')

print('Making LoadInfo.csv... ', end='')
all_info = glob.glob(os.path.join(CSV_PATH, "info_flightnumber*.csv"))
df = pd.concat(map(pd.read_csv, all_info), ignore_index=True)
df.to_csv(os.path.join(MYSQL_UPLOADS, "LoadInfo.csv"), index=False)
print('DONE')
