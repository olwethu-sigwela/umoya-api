from bs4 import BeautifulSoup
import json
from datetime import date
import os

script_dir = os.path.dirname(__file__)


filename = script_dir + "/../prepaid_bundles.json"


carrier_name = "Cell C"

def get_prepaid():
    
    #TODO: Figure out how to access the data that the loading section is accessing

    data = [
            {"Name":"Cell C 30MB Anytime + 30MB Nite Data","Validity (# of days)":1,"Size (MB)":60,"Price (ZAR)":5},
            {"Name":"Cell C 120MB Anytime + 120MB Nite Data","Validity (# of days)":14,"Size (MB)":240,"Price (ZAR)":15},
            {"Name":"Cell C 300MB Anytime + 300MB Nite Data","Validity (# of days)":14,"Size (MB)":600,"Price (ZAR)":35},
            {"Name":"Cell C 450MB Anytime + 450MB Nite Data","Validity (# of days)":30,"Size (MB)":900,"Price (ZAR)":50},
            {"Name":"Cell C 1GB Anytime + 1GB Nite Data","Validity (# of days)":30,"Size (MB)":2048,"Price (ZAR)":95},
            {"Name":"Cell C 2.5GB Anytime + 2.5GB Nite Data","Validity (# of days)":30,"Size (MB)":5120,"Price (ZAR)":195},
            {"Name":"Cell C 5GB Anytime + 5GB Nite Data + Free 500MB Social Bundle","Validity (# of days)":30,"Size (MB)":10500,"Price (ZAR)":359},
            {"Name":"Cell C 10GB Anytime + 10GB Nite Data + Free 1GB Social Bundle","Validity (# of days)":30,"Size (MB)":21504,"Price (ZAR)":669},
            {"Name":"Cell C 20GB Anytime + 20GB Nite Data + Free 2GB Social Bundle","Validity (# of days)":30,"Size (MB)":43008,"Price (ZAR)":1249},
            {"Name":"Cell C 30MB Anytime + 30MB Facebook + 30MB Video Streaming","Validity (# of days)":0.5,"Size (MB)":90,"Price (ZAR)":5},
            {"Name":"Cell C 50MB Anytime + 50MB Facebook + 50MB Video Streaming","Validity (# of days)":0.5,"Size (MB)":150,"Price (ZAR)":10},
            {"Name":"Cell C 150MB Anytime + 150MB Facebook + 150MB Video Streaming","Validity (# of days)":0.5,"Size (MB)":450,"Price (ZAR)":20},
            {"Name":"Cell C 100MB Anytime + 100MB Facebook + 100MB Video Streaming","Validity (# of days)":7,"Size (MB)":300,"Price (ZAR)":20},
            {"Name":"Cell C 374MB Anytime + 350MB Facebook + 300MB Video Streaming","Validity (# of days)":7,"Size (MB)":1024,"Price (ZAR)":49},
            {"Name":"Cell C 1GB Anytime + 1GB Facebook + 1GB Video Streaming","Validity (# of days)":7,"Size (MB)":3072,"Price (ZAR)":79},
            {"Name":"Cell C 2GB Anytime + 2GB Facebook + 2GB Video Streaming","Validity (# of days)":7,"Size (MB)":6144,"Price (ZAR)":129},
            {"Name":"Cell C 424MB Anytime + 400MB Facebook + 200MB Video Streaming","Validity (# of days)":30,"Size (MB)":1024,"Price (ZAR)":50},
            {"Name":"Cell C 1GB Anytime + 500MB Facebook + 500MB Video Streaming","Validity (# of days)":30,"Size (MB)":2048,"Price (ZAR)":99},
            {"Name":"Cell C 1.5GB Anytime + 750MB Facebook + 750MB Video Streaming","Validity (# of days)":30,"Size (MB)":3072,"Price (ZAR)":149}
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
    





