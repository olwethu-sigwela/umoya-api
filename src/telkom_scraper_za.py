from bs4 import BeautifulSoup
import json
from datetime import date
import os
import requests
import locale
script_dir = os.path.dirname(__file__)


locale.setlocale(locale.LC_ALL, '')


filename = script_dir + "/../prepaid_bundles.json"


carrier_name = "Telkom"


def get_freeme():

    data = []

    response = requests.get("https://www.telkom.co.za/prepaid-services/free-me-bundle")
    soup = BeautifulSoup(response.content, "html.parser")

    data_table = soup.select(".BundleTable_tab__c4iyg")[0]
    data_table_rows = soup.select("tr")
    data_table_rows_text = [row.get_text("|").split("|") for row in data_table_rows]

    
    for row in data_table_rows_text:
        if row == ['Bundle', 'Validity', 'Price']: #skips headers
            continue

        data_item = {}
        data_item["Name"] = ' '.join([row[0], row[1]])

        data_amount_container = row[1].split(" ")
        data_amount = locale.atof(data_amount_container[0])
        data_magnitude = data_amount_container[1]
        
        if data_magnitude == "GB":
            data_amount *= 1024
        validity = float(row[2].split(" ")[0])
        data_item["Validity (# of days)"] = validity
        data_item["Size (MB)"] = data_amount
        data_item["Price (ZAR)"] = float(row[3][1:])

        data.append(data_item)

    return data

def get_flexon():

    data = []

    response = requests.get("https://www.telkom.co.za/prepaid-services/flexon")
    soup = BeautifulSoup(response.content, "html.parser")
    
    data_table = soup.select(".BundleTable_tab__c4iyg")[0]
    data_table_rows = soup.select("tr")
    data_table_rows_text = [row.get_text("|").split("|") for row in data_table_rows]

    
    for row in data_table_rows_text:

   
        if row == ['Bundle', 'Validity', 'Price']: #skips headers
            continue

        data_item = {}
        data_item["Name"] = row[0]


        data_amount_container = row[0].split(" ")
    
        numbers = "0123456789"
        magnitude_letters = "MGB"
        data_amount_list = [i  for i in data_amount_container[-1] if i in numbers]
        data_magnitude_list = [i  for i in data_amount_container[-1] if i in magnitude_letters]
        # print(f"{data_amount_list=}")
        data_amount = float(''.join(data_amount_list))
        data_magnitude = ''.join(data_magnitude_list)
       

        
        if data_magnitude == "GB":
            data_amount *= 1024
        validity = float(row[1].split(" ")[0])
        data_item["Validity (# of days)"] = validity
        data_item["Size (MB)"] = data_amount
        data_item["Price (ZAR)"] = float(row[-1][1:])

        data.append(data_item)

      

   
    return data

def get_hourly():
    data = [
  {"Name":"Hourly Data bundle 150MB - Once-off","Validity (# of days)":0.042,"Size (MB)":150,"Price (ZAR)":5.5},
  {"Name":"Hourly Data bundle 300MB - Once-off","Validity (# of days)":0.042,"Size (MB)":300,"Price (ZAR)":9},
  {"Name":"Hourly Data bundle 250MB - Once-off","Validity (# of days)":0.125,"Size (MB)":250,"Price (ZAR)":11},
  {"Name":"Hourly Data bundle 400MB - Once-off","Validity (# of days)":0.125,"Size (MB)":400,"Price (ZAR)":13},
  {"Name":"Hourly Data bundle 500MB - Once-off","Validity (# of days)":0.5,"Size (MB)":500,"Price (ZAR)":16}
]
    
    return data


def get_daily():

    data = [
  {"Name":"Daily Data Bundle 30MB - Once-off","Validity (# of days)":1,"Size (MB)":30,"Price (ZAR)":5.5},
  {"Name":"Daily Data Bundle 500MB - Once-off","Validity (# of days)":1,"Size (MB)":500,"Price (ZAR)":16},
  {"Name":"Daily Data Bundle 150MB - Once-off","Validity (# of days)":1,"Size (MB)":150,"Price (ZAR)":12},
  {"Name":"Daily Data Bundle 1GB - Once-off","Validity (# of days)":1,"Size (MB)":1024,"Price (ZAR)":31},
  {"Name":"Daily Data Bundle 2GB - Once-off","Validity (# of days)":1,"Size (MB)":2048,"Price (ZAR)":52}
]

    return data

def get_weekend():

    data = [
  {"Name": "Weekend Data Bundle 500MB - Once-off", "Validity (# of days)": 2, "Size (MB)": 500, "Price (ZAR)": 31},
  {"Name": "Weekend Data Bundle 1GB - Once-off", "Validity (# of days)": 2, "Size (MB)": 1024, "Price (ZAR)": 52},
  {"Name": "Weekend Data Bundle 100MB - Once-off", "Validity (# of days)": 2, "Size (MB)": 100, "Price (ZAR)": 12},
  {"Name": "Weekend Data Bundle 200MB - Once-off", "Validity (# of days)": 2, "Size (MB)": 200, "Price (ZAR)": 20}
]

    return data

def get_weekly():
    data = [
  { "Name": "Weekly Data Bundle - 50MB", "Validity (# of days)": 7, "Size (MB)": 50.0, "Price (ZAR)": 6.0 },
  { "Name": "Weekly Data Bundle - 100MB", "Validity (# of days)": 7, "Size (MB)": 100.0, "Price (ZAR)": 16.0 },
  { "Name": "Weekly Data Bundle - 250MB", "Validity (# of days)": 7, "Size (MB)": 250.0, "Price (ZAR)": 32.0 },
  { "Name": "Weekly Data Bundle - 500MB", "Validity (# of days)": 7, "Size (MB)": 500.0, "Price (ZAR)": 53.0 },
  { "Name": "Weekly Data Bundle - 1GB", "Validity (# of days)": 7, "Size (MB)": 1024.0, "Price (ZAR)": 79.0 },
  { "Name": "Weekly Data Bundle - 2GB", "Validity (# of days)": 7, "Size (MB)": 2048.0, "Price (ZAR)": 105.0 }
]
    
    return data

def get_all_network():

    data = [{"Name":"All Networks Data Bundles - 35MB + 35MB - Once-off","Validity (# of days)":180,"Size (MB)":70,"Price (ZAR)":7.5},{"Name":"All Networks Data Bundles - 75MB + 75MB - Once-off","Validity (# of days)":180,"Size (MB)":150,"Price (ZAR)":15},{"Name":"All Networks Data Bundles - 150MB + 150MB - Once-off","Validity (# of days)":180,"Size (MB)":300,"Price (ZAR)":31},{"Name":"All Networks Data Bundles - 300MB + 300MB - Once-off","Validity (# of days)":180,"Size (MB)":600,"Price (ZAR)":52},{"Name":"All Networks Data Bundles - 500MB + 500MB - Once-off","Validity (# of days)":180,"Size (MB)":1000,"Price (ZAR)":72},{"Name":"All Networks Data Bundles - 1.5GB + 1.5GB - Once-off","Validity (# of days)":60,"Size (MB)":3072,"Price (ZAR)":89},{"Name":"All Networks Data Bundles - 1GB + 1GB - Once-off","Validity (# of days)":60,"Size (MB)":2048,"Price (ZAR)":79},{"Name":"All Networks Data Bundles - 2GB + 2GB - Once-off","Validity (# of days)":60,"Size (MB)":4096,"Price (ZAR)":146},{"Name":"All Networks Data Bundles - 3GB + 3GB - Once-off","Validity (# of days)":60,"Size (MB)":6144,"Price (ZAR)":209},{"Name":"All Networks Data Bundles - 5GB + 5GB - Once-off","Validity (# of days)":60,"Size (MB)":10240,"Price (ZAR)":314},{"Name":"All Networks Data Bundles - 10GB + 10GB - Once-off","Validity (# of days)":60,"Size (MB)":20480,"Price (ZAR)":493},{"Name":"All Networks Data Bundles - 20GB - Once-off","Validity (# of days)":60,"Size (MB)":20480,"Price (ZAR)":734},{"Name":"All Networks Data Bundles - 50GB - Once-off","Validity (# of days)":180,"Size (MB)":51200,"Price (ZAR)":1574}]

    return data






 

    


def get_prepaid():
    
    #TODO: Figure out how to access the data that the loading section is accessing

    data = []


    freeme_data = get_freeme()

    flexon_data = get_flexon()

    daily_data = get_daily()

    hourly_data = get_hourly()

    weekend_data = get_weekend()

    weekly_data = get_weekly()

    all_network_data = get_all_network()

    data = freeme_data + flexon_data + daily_data + hourly_data + weekend_data + weekly_data + all_network_data


    

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
    





