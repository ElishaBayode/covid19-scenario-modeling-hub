import io
import requests
from datetime import datetime
import pandas as pd
import glob
import os


def request_get_link(link, output_dtype=None):
    df = None
    try:
        result = requests.get(link, timeout=30)
        if result.status_code == 200:
            df = pd.read_csv(io.StringIO(result.text), dtype=output_dtype)
        else:
            print("Error getting page; HTTP status " + str(result.status_code))
    except Exception as e:
        print("Error for link: " + link)
        print(e)
    return df


print("Archiving past file")
files = glob.glob("auxiliary-data/vaccination-coverage/vax_cov/*.csv")
if len(files) > 0:
    for i in files:
        os.rename(i, "auxiliary-data/vaccination-coverage/vax_cov/archive/" + os.path.basename(i))

print("Downloading ...")

# COVID-19 Vaccination Coverage, Overall and by Selected Demographics and Jurisdiction, 
# Among Adults 18 Years and Older, by Season
df_cov_vax_adult = request_get_link("https://data.cdc.gov/api/views/ksfb-ug5d/rows.csv?accessType"
                                    "=DOWNLOAD")
print("COVID-19 Vax Coverage - Adult _ Downloaded")
df_cov_vax_adult.to_csv("auxiliary-data/vaccination-coverage/vax_cov/" +
                        datetime.today().strftime("%Y-%m-%d") +
                        "-vax_coverage_adult.csv")

# Weekly Parental Intent for Vaccination and Cumulative Percentage of Children 6 Months -17
# Years Who are Up to date with the COVID-19 Vaccines by Season
df_cov_vax_child = request_get_link("https://data.cdc.gov/api/views/ker6-gs6z/rows.csv?accessType"
                                    "=DOWNLOAD")
print("COVID-19 Vax Coverage - Child _ Downloaded")
df_cov_vax_child.to_csv("auxiliary-data/vaccination-coverage/vax_cov/" +
                        datetime.today().strftime("%Y-%m-%d") +
                        "-vax_coverage_children.csv")
