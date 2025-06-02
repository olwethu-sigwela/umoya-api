from bs4 import BeautifulSoup
import json
from datetime import date
import os
import requests

script_dir = os.path.dirname(__file__)


filename = script_dir + "/../prepaid_bundles.json"


carrier_name = "Rain"

def get_prepaid():
    
    #TODO: Figure out how to access the data that the loading section is accessing

    data = [
        {"Name": "Rain Prepaid 1GB", "Validity (# of days)": 30, "Size (MB)": 1024, "Price (ZAR)": 10} 
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
    





