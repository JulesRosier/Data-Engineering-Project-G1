import mysql.connector as mysql
from datetime import date, timedelta
import shutil
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# .env aanpassen naar eigen onedrive in volgend formaat: # ONEDRIVE_PATH= "C:\\Users\\WardD\\OneDrive - Hogeschool Gent\\AirFares\\"
ONEDRIVE_PATH = os.environ.get("ONEDRIVE_PATH")
# REPO_PATH = os.environ.get('REPO_PATH') #.env aanpassen naar eigen repo in volgend formaat:# REPO_PATH = "C:\\Users\\WardD\\Documents\\School\\22-23\\SEMESTER 2\\Project\\Repo\\Data-Engineering-Project-G1\\src\\csv\\"
REPO_PATH = "./oltp/csv/"


# choose a specific start_date
start_date = date(2023, 4, 6)
end_date = date.today()
delta = timedelta(days=1)

if not os.path.exists(REPO_PATH):
    os.makedirs(REPO_PATH)

for file in os.listdir(ONEDRIVE_PATH):
    if "info_flightnumber" in file:
        print(f"copying {file}... ", end='')
        df = pd.read_csv(f"{ONEDRIVE_PATH}{file}")
        df.to_csv(f"{REPO_PATH}{file}", index=False)
        # shutil.copy(f"{ONEDRIVE_PATH}{file}", REPO_PATH)
        print("DONE")

while start_date <= end_date:

    date_format = start_date.strftime("%Y_%m_%d")

    repo_All = REPO_PATH + "All" + "_" + date_format + ".csv"
    repo_All_Recent = REPO_PATH + "All" + ".csv"
    repo_All_Onedrive = ONEDRIVE_PATH + "All" + "_" + date_format + ".csv"

    if os.path.exists(repo_All):
        os.remove(repo_All)

    # if os.path.exists(repo_All_Recent):
    #     os.remove(repo_All_Recent)

    if os.path.exists(repo_All_Onedrive):
        print(f"copying {repo_All_Onedrive}... ", end='')
        df = pd.read_csv(repo_All_Onedrive)
        df.to_csv(repo_All, index=False)
        # shutil.copy(repo_All_Onedrive, repo_All)
        print('DONE')

    # if os.path.exists(repo_All_Onedrive):
    #     shutil.copy(repo_All_Onedrive, repo_All_Recent)

    start_date += delta
