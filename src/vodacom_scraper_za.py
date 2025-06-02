from bs4 import BeautifulSoup
import json
from datetime import date
import os
import requests

script_dir = os.path.dirname(__file__)


filename = script_dir + "/../prepaid_bundles.json"


carrier_name = "Vodacom"


def get_from_container(soup, container_id, validity):
    data = []

 

   
    bundles_container = soup.select(f"#{container_id}")[0]

   
    header = bundles_container.select("h4")[0].get_text()
    header = header.split(" ")[0]
    bundles = bundles_container.select(".field__item")
  

    for i in range(len(bundles)):
        item = bundles[i].get_text()

        if "Available" in item or "Data" in item: #skips the headers
            continue
        
        split_item = bundles[i].get_text().split("-")
        split_item = [s_i.strip(" ") for s_i in split_item]
        data_item = {}

        data_item["Name"] = f"Vodacom {header} {split_item[0]}"
        data_item["Validity (# of days)"] = validity
        
        if "MB" in split_item[0]:
            
            split_item[0] = float(split_item[0][:split_item[0].index("M")])


        elif "GB" in split_item[0]:
            split_item[0] = 1024*float(split_item[0][:split_item[0].index("G")])
        
        split_item[1] = float(split_item[1][1:])

        data_item["Size (MB)"] = split_item[0]
        data_item["Price (ZAR)"] = split_item[1]

        data.append(data_item)

    return data




def get_prepaid():
    
    response = requests.get("https://www.vodacom.co.za/vodacom/shopping/data/prepaid-data#ae486950-tabs-vertical--item-wrapper-3304977692-3304977692")

    soup = BeautifulSoup(response.content, "html.parser")

    data = []

    monthly_data = get_from_container(soup, "field__item--field_plain_card_elements--20976-1", 30)
   
 
    
    weekly_data = get_from_container(soup, "field__item--field_plain_card_elements--20981-0", 7)


    night_owl_weekly_data = get_from_container(soup, "field__item--field_plain_card_elements--20981-1", 7)

 
    
    daily_data = get_from_container(soup, "field__item--field_plain_card_elements--20986-0", 1)
 

    night_owl_daily_data = get_from_container(soup, "field__item--field_plain_card_elements--20986-1", 1)
  

    hourly_data = get_from_container(soup, "field__item--field_plain_card_elements--20986-2", 1/24)
   

    
    data = monthly_data + weekly_data + night_owl_weekly_data + daily_data + night_owl_daily_data + hourly_data




    

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
    





