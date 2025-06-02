from flask import Flask, jsonify, request, make_response, render_template, url_for, flash, redirect, send_from_directory, session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import json


load_dotenv("../.env")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

script_dir = os.path.dirname(__file__)

prepaid_filename = script_dir + "/../prepaid_bundles.json"




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