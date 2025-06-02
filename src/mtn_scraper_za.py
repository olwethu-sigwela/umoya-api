from bs4 import BeautifulSoup
import json
from datetime import date
import os
import requests

script_dir = os.path.dirname(__file__)


filename = script_dir + "/../prepaid_bundles.json"


carrier_name = "MTN"

def get_prepaid():
    
    #TODO: Figure out how to access the data that the loading section is accessing

    data = [
        {"Name": "MTN Personalised Weekly- 50MB", "Validity (# of days)": 7, "Size (MB)": 50, "Price (ZAR)": 10},
        {"Name": "MTN Personalised Weekly- 70MB", "Validity (# of days)": 7, "Size (MB)": 70, "Price (ZAR)": 12},
        {"Name": "MTN Personalised Weekly- 100MB", "Validity (# of days)": 7, "Size (MB)": 100, "Price (ZAR)": 12},
        {"Name": "MTN Personalised Weekly- 100MB", "Validity (# of days)": 7, "Size (MB)": 100, "Price (ZAR)": 15},
        {"Name": "MTN Personalised Weekly- 120MB", "Validity (# of days)": 7, "Size (MB)": 120, "Price (ZAR)": 17},
        {"Name": "MTN Personalised Weekly- 200MB", "Validity (# of days)": 7, "Size (MB)": 200, "Price (ZAR)": 25},
        {"Name": "MTN Personalised Weekly- 350MB", "Validity (# of days)": 7, "Size (MB)": 350, "Price (ZAR)": 40},
         {"Name": "MTN Personalised Weekly- 500MB", "Validity (# of days)": 7, "Size (MB)": 500, "Price (ZAR)": 55},
          {"Name": "MTN Personalised Monthly- 40MB", "Validity (# of days)": 30, "Size (MB)": 40, "Price (ZAR)": 5},
          {"Name": "MTN Personalised Monthly- 40MB", "Validity (# of days)": 30, "Size (MB)": 40, "Price (ZAR)": 10},
          {"Name": "MTN Personalised Monthly- 100MB", "Validity (# of days)": 30, "Size (MB)": 100, "Price (ZAR)": 10},
          {"Name": "MTN Personalised Monthly- 100MB", "Validity (# of days)": 30, "Size (MB)": 100, "Price (ZAR)": 15},
          {"Name": "MTN Personalised Monthly- 150MB", "Validity (# of days)": 30, "Size (MB)": 150, "Price (ZAR)": 20},
          {"Name": "MTN Personalised Monthly- 150MB", "Validity (# of days)": 30, "Size (MB)": 150, "Price (ZAR)": 25},
          {"Name": "MTN Personalised Monthly- 200MB", "Validity (# of days)": 30, "Size (MB)": 200, "Price (ZAR)": 25},
          {"Name": "MTN Personalised Monthly- 200MB", "Validity (# of days)": 30, "Size (MB)": 200, "Price (ZAR)": 29},
          {"Name": "MTN Personalised Monthly- 200MB", "Validity (# of days)": 30, "Size (MB)": 200, "Price (ZAR)": 35},
          {"Name": "MTN Personalised Monthly- 200MB", "Validity (# of days)": 30, "Size (MB)": 200, "Price (ZAR)": 39},
          {"Name": "MTN Personalised Monthly- 350MB", "Validity (# of days)": 30, "Size (MB)": 350, "Price (ZAR)": 39},
          {"Name": "MTN Personalised Monthly- 350MB", "Validity (# of days)": 30, "Size (MB)": 350, "Price (ZAR)": 55},
          {"Name": "MTN Personalised Monthly- 200MB", "Validity (# of days)": 30, "Size (MB)": 200, "Price (ZAR)": 60},
          {"Name": "MTN Personalised Monthly- 500MB", "Validity (# of days)": 30, "Size (MB)": 500, "Price (ZAR)": 60},
          {"Name": "MTN Personalised Monthly- 750MB", "Validity (# of days)": 30, "Size (MB)": 750, "Price (ZAR)": 89},
          {"Name": "MTN Personalised Monthly- 1GB", "Validity (# of days)": 30, "Size (MB)": 1024, "Price (ZAR)": 89},
          {"Name": "MTN Personalised Monthly- 1.5GB", "Validity (# of days)": 30, "Size (MB)": 1524, "Price (ZAR)": 149},
          {"Name": "MTN Personalised Monthly- 2GB", "Validity (# of days)": 30, "Size (MB)": 2048, "Price (ZAR)": 149},
          {"Name": "MTN Personalised Monthly- 2GB", "Validity (# of days)": 30, "Size (MB)": 2048, "Price (ZAR)": 169}     
    ]

    

    data_dict = json.load(open(filename, "r"))
    today_date = date.today()
    
    full_data_entry = {"Date": str(today_date), "Data": data}

    data_list_length = len(data_dict[carrier_name])

    if data_list_length == 0:
        data_dict[carrier_name].append(full_data_entry)
    else:
        most_recent_date_string = data_dict[carrier_name][-1]["Date"]
        year, month, day = [int(i) for i in most_recent_date_string.split("-")]
        most_recent_date = date(year, month, day)

        if most_recent_date < today_date:
            data_dict[carrier_name].append(full_data_entry)
        
    dump = json.dumps(data_dict)
    out_file = open(filename, "w")
    out_file.write(dump)
    out_file.close()


def main():
    get_prepaid()


if __name__ == "__main__":
    main()
    





