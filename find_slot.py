import datetime
import json
import requests
import pandas as pd
from copy import deepcopy
import logging
import pywhatkit

logging.basicConfig(level=logging.INFO)

def load_mapping():
    df = pd.read_csv("district_mapping.csv")
    return df

def filter_column(df, col, value):
    df_temp = deepcopy(df.loc[df[col] == value, :])
    return df_temp


mapping_df = load_mapping()

mapping_dict = pd.Series(mapping_df["district id"].values,
                         index = mapping_df["district name"].values).to_dict()

rename_mapping = {
    'date': 'Date',
    'min_age_limit': 'Minimum Age Limit',
    'available_capacity': 'Available Capacity',
    'pincode': 'Pincode',
    'name': 'Hospital Name',
    'state_name' : 'State',
    'district_name' : 'District',
    'block_name': 'Block Name',
    'fee_type' : 'Fees'
    }

unique_districts = list(mapping_df["district name"].unique())
unique_districts.sort()

base = datetime.datetime.todap;y()
date_list = [base + datetime.timedelta(days=x) for x in range(2)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]

def run():
    final_df = None
    for dist_inp in unique_districts[:10]:
        logging.info(dist_inp)
        DIST_ID = mapping_dict[dist_inp]
        for INP_DATE in date_str:
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(DIST_ID, INP_DATE)
            response = requests.get(URL)
            if response.ok:
                resp_json = json.loads(response.text)['centers']
                df = pd.DataFrame(resp_json)
                final_df = deepcopy(df)
            if final_df:
                final_df.drop_duplicates(inplace=True)
                final_df.rename(columns=rename_mapping, inplace=True)
                age_inp = 18
                final_df = filter_column(final_df, "Minimum Age Limit", age_inp)
                # pay_inp = "Free"
                # final_df = filter_column(final_df, "Fees", pay_inp)
                table = deepcopy(final_df)
                table.reset_index(inplace=True, drop=True)
                for ind,row in table.iterrows():
                    if row["Available Capacity"]>0:
                        return "Slots are available"
    pywhatkit.sendwhatmsg('+918959159066', "Slots not available", 21, 45)