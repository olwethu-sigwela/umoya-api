from flask import Flask, jsonify, request, make_response, render_template, url_for, flash, redirect, send_from_directory, session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import json
from helpers import median, price_per_mb, get_price_per_mb_list, get_price_list, get_cheapest_bundle, get_carrier_names, get_price_per_mb_vs_size, get_median_price_per_mb_vs_size




app = Flask(__name__)


script_dir = os.path.dirname(__file__)

prepaid_filename = script_dir + "/../prepaid_bundles.json"
load_dotenv(script_dir + "/../.env")
app.secret_key = os.getenv("SECRET_KEY")



CORS(app, supports_credentials=True)



"""
Planned API calls:

/prepaid (GET): Returns prepaid bundle data

    params:
        carrier = Mobile carrier (e.g. MTN)



/contract (GET): Returns contract bundle data

    params:
        carrier = Mobile carrier (e.g. MTN)

"""


@app.route("/prepaid", methods=["GET"])
def prepaid():

    carrier = request.args.get("carrier")
    status = "Successful"
    reason = ""
    status_code = 200

    if carrier is None:
        status = "Unsuccessful"
        reason = "Please provide a carrier name"
        status_code = 422


    response_dict = {}

    if status_code == 200:

        data_dict = json.load(open(prepaid_filename, "r"))
        key_found = True
        
        try:
            data_len = len(data_dict[carrier])
        except KeyError:
            key_found = False

        if key_found: 
            if data_len > 0:
                response_dict["Data"] = data_dict[carrier][-1]

                for item in response_dict["Data"]["Data"]:
                    item["Price per MB (ZAR/MB)"] = round(price_per_mb(item["Price (ZAR)"], item["Size (MB)"]), 2) 
            else:
                status = "Unsuccessful"
                status_code = 404
                reason = "Requested data not found"
        
        else:
            status = "Unsuccessful"
            status_code = 404
            reason = "Selected carrier is unavailable"


    response_dict["Message"] =  f"{status}. {reason}." if status_code != 200 else f"{status}."

    response = jsonify(response_dict)

    return response, status_code


@app.route("/prepaid-price-per-mb-vs-size", methods=["GET"])
def prepaid_price_per_mb_vs_size():

    carrier = request.args.get("carrier")
    data_type = request.args.get("data-type")
    status = "Successful"
    reason = ""
    status_code = 200

    if carrier is None:
        status = "Unsuccessful"
        reason = "Please provide a carrier name"
        status_code = 422


    response_dict = {}

    if status_code == 200:

        data_dict = json.load(open(prepaid_filename, "r"))
        key_found = True
        
        try:
            data_len = len(data_dict[carrier])
        except KeyError:
            key_found = False

        if key_found: 
            if data_len > 0:
                sizes, prices_per_mb = get_median_price_per_mb_vs_size(data_dict, carrier)
                if data_type == "objects":
                    response_dict["Data"] = [{"Size (MB)": s, "Price per MB (ZAR/MB)": p_p_mb} for s, p_p_mb in zip(sizes, prices_per_mb)]

                else:
                    response_dict["Data"] = {"Size (MB)": sizes, "Price per MB (ZAR/MB)": prices_per_mb}


                

            else:
                status = "Unsuccessful"
                status_code = 404
                reason = "Requested data not found"
        
        else:
            status = "Unsuccessful"
            status_code = 404
            reason = "Selected carrier is unavailable"


    response_dict["Message"] =  f"{status}. {reason}." if status_code != 200 else f"{status}."

    response = jsonify(response_dict)

    return response, status_code



@app.route("/prepaid-median-price-per-mb", methods=["GET"])
def prepaid_median_price_per_mb():
    
    carrier = request.args.get("carrier")
    status = "Successful"
    reason = ""
    status_code = 200

    if carrier is None:
        status = "Unsuccessful"
        reason = "Please provide a carrier name"
        status_code = 422


    response_dict = {}

    if status_code == 200:

        data_dict = json.load(open(prepaid_filename, "r"))
        key_found = True
        carriers = []
      
        if carrier != "all":
            try:
                data_len = len(data_dict[carrier])
            except KeyError:
                key_found = False

            if key_found: 
                if data_len > 0:
                    bundle_list = data_dict[carrier][-1]["Data"]
                    prices_per_mb = get_price_per_mb_list(bundle_list)
                   
                    median_price_per_mb = median(prices_per_mb)
                    response_dict["Carrier"] = carrier
                    response_dict["Median Price per MB"] = round(median_price_per_mb, 2)

                else:
                    status = "Unsuccessful"
                    status_code = 404
                    reason = "Requested data not found"
            
            else:
                status = "Unsuccessful"
                status_code = 404
                reason = "Selected carrier is unavailable"
        
        else:
            carriers = get_carrier_names(data_dict)
            response_dict["Carriers"] = []

            for c in carriers:
                data_len = len(data_dict[c])

                if data_len > 0:
                    bundle_list = data_dict[c][-1]["Data"]
                    prices_per_mb = get_price_per_mb_list(bundle_list)
                  
                    median_price_per_mb = median(prices_per_mb)

                    carrier_dict = {}
                    carrier_dict["Carrier"] = c
                    carrier_dict["Median Price per MB"] = round(median_price_per_mb, 2)
                    response_dict["Carriers"].append(carrier_dict)

    response_dict["Message"] =  f"{status}. {reason}." if status_code != 200 else f"{status}."

    response = jsonify(response_dict)

    return response, status_code



@app.route("/prepaid-cheapest-bundle", methods=["GET"])
def prepaid_cheapest_bundle():
    
    carrier = request.args.get("carrier")
    
    status = "Successful"
    reason = ""
    status_code = 200

    if carrier is None:
        status = "Unsuccessful"
        reason = "Please provide a carrier name"
        status_code = 422


    response_dict = {}

    if status_code == 200:

        data_dict = json.load(open(prepaid_filename, "r"))
        key_found = True
        carriers = []
      
        if carrier != "all":
            try:
                data_len = len(data_dict[carrier])
            except KeyError:
                key_found = False

            if key_found: 
                if data_len > 0:

                    bundle_list = data_dict[carrier][-1]["Data"]
                   
                  
                    cheapest_bundle, cheapest_bundle_size, cheapest_bundle_price = get_cheapest_bundle(bundle_list)
                    response_dict["Bundle Name"] = cheapest_bundle
                    response_dict["Size (MB)"] = cheapest_bundle_size
                    response_dict["Price (ZAR)"] = cheapest_bundle_price
                    response_dict["Price per MB (ZAR/MB)"] = round(price_per_mb(cheapest_bundle_price, cheapest_bundle_size), 2)


                else:
                    status = "Unsuccessful"
                    status_code = 404
                    reason = "Requested data not found"
            
            else:
                status = "Unsuccessful"
                status_code = 404
                reason = "Selected carrier is unavailable"
        
        else:
            carriers = get_carrier_names(data_dict)
            response_dict["Carriers"] = []

            for c in carriers:
                data_len = len(data_dict[c])

                if data_len > 0:

                    bundle_list = data_dict[c][-1]["Data"]
                 
                  
                    cheapest_bundle, cheapest_bundle_size, cheapest_bundle_price = get_cheapest_bundle(bundle_list)
                    carrier_dict = {}
                    carrier_dict["Carrier"] = c
                    carrier_dict["Bundle Name"] = cheapest_bundle
                    carrier_dict["Price (ZAR)"] = cheapest_bundle_price
                    carrier_dict["Size (MB)"] = cheapest_bundle_size
                    carrier_dict["Price per MB (ZAR/MB)"] = round(price_per_mb(cheapest_bundle_price, cheapest_bundle_size), 2)
                    response_dict["Carriers"].append(carrier_dict)


    response_dict["Message"] =  f"{status}. {reason}." if status_code != 200 else f"{status}."

    response = jsonify(response_dict)

    return response, status_code



@app.route("/prepaid-lowest-prices", methods=["GET"])
def prepaid_lowest_prices():
    
    carrier = request.args.get("carrier")
    
    status = "Successful"
    reason = ""
    status_code = 200

    if carrier is None:
        status = "Unsuccessful"
        reason = "Please provide a carrier name"
        status_code = 422


    response_dict = {}

    if status_code == 200:

        data_dict = json.load(open(prepaid_filename, "r"))
        key_found = True
        carriers = []
      
        if carrier != "all":
            try:
                data_len = len(data_dict[carrier])
            except KeyError:
                key_found = False

            if key_found: 
                if data_len > 0:

                    bundle_list = data_dict[carrier][-1]["Data"]
                   
                  
                    cheapest_bundle, cheapest_bundle_size, cheapest_bundle_price = get_cheapest_bundle(bundle_list)
                   
                    response_dict["Price (ZAR)"] = cheapest_bundle_price
                    


                else:
                    status = "Unsuccessful"
                    status_code = 404
                    reason = "Requested data not found"
            
            else:
                status = "Unsuccessful"
                status_code = 404
                reason = "Selected carrier is unavailable"
        
        else:
            carriers = get_carrier_names(data_dict)
            response_dict["Carriers"] = []

            for c in carriers:
                data_len = len(data_dict[c])

                if data_len > 0:

                    bundle_list = data_dict[c][-1]["Data"]
                 
                  
                    cheapest_bundle, cheapest_bundle_size, cheapest_bundle_price = get_cheapest_bundle(bundle_list)
                    carrier_dict = {}
                    carrier_dict["Carrier"] = c
                  
                    carrier_dict["Price (ZAR)"] = cheapest_bundle_price
                  
                    response_dict["Carriers"].append(carrier_dict)


    response_dict["Message"] =  f"{status}. {reason}." if status_code != 200 else f"{status}."

    response = jsonify(response_dict)

    return response, status_code



@app.route("/contract", methods=["GET"])
def contact():

    

    carrier = request.args.get("carrier")
    status = "Successful"
    reason = ""
    status_code = 200

    if carrier is None:
        status = "Unsuccessful"
        reason = "Please provide a carrier name"
        status_code = 422


    response_dict = {"Message": f"{status}. {reason}." if status_code != 200 else f"{status}."}

    response = jsonify(response_dict)

    return response, status_code


localhost = "0.0.0.0"
port = 8080


def main():

    app.run(host=localhost, port=port)

if __name__ == "__main__":
    main()