import requests
import pandas as pd
from tabulate import tabulate
from flask import Flask, render_template, redirect, session, request
from flask_session import Session
import os
from dotenv import load_dotenv

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Globals
load_dotenv() # gets the API key from the .env file
api_key = os.environ.get("SCRAPE_API_KEY")
# url for testing: https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-122.17040010111008%2C%22east%22%3A-122.0699781955925%2C%22south%22%3A37.39634394555346%2C%22north%22%3A37.44542356875894%7D%2C%22mapZoom%22%3A14%2C%22usersSearchTerm%22%3A%223444%20Ashton%20Ct%20Palo%20Alto%2C%20CA%2094306%22%2C%22customRegionId%22%3A%221e42866394X1-CR8uzkls0vwlfr_13lqr1%22%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sche%22%3A%7B%22value%22%3Afalse%7D%2C%22schm%22%3A%7B%22value%22%3Afalse%7D%2C%22schh%22%3A%7B%22value%22%3Afalse%7D%2C%22schp%22%3A%7B%22value%22%3Afalse%7D%2C%22schr%22%3A%7B%22value%22%3Afalse%7D%2C%22schc%22%3A%7B%22value%22%3Afalse%7D%2C%22schu%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D

# Documentation for Scrapeak APIs used: https://docs.scrapeak.com/zillow-scraper/endpoints/propertydetails

# Gets zpids (unique zillow property ids) given a zillow search
def get_zpids(url):
    # Uses the 'listing' api from scrapeak to get zpids
    api_url = "https://app.scrapeak.com/v1/scrapers/zillow/listing"

    # Call api on url given
    params = {"api_key": api_key, "url": url}
    response = requests.get(api_url, params=params)

    # Format responses
    zpids = {}
    status_code = response.status_code
    response_json = response.json()

    # Quit early if we didn't successfully get info from the url
    if status_code != 200 or not response_json:
        return zpids, status_code
    
    # Loop over returned data and store the zpids and associated more details urls
    data = response_json["data"]
    for i in data["cat1"]["searchResults"]["listResults"]:
        zpids[i["zpid"]] = {
            "price": i.get("price", "null"),
            "area": i.get("area", "null"),
            "beds": i.get("beds", "null"),
            "baths": i.get("baths", "null"),
            "address": i.get("address", "null"),
            "detailUrl": i.get("detailUrl", "null")
        }
    return zpids, status_code

# Gets price history for each given zpid
def price_history(zpids):
    # Uses 'property' api from scrapeak
    api_url = "https://app.scrapeak.com/v1/scrapers/zillow/property"
    price_history = []
    for zpid in zpids:
        params = {"api_key": api_key, "zpid": zpid}
        price_history.append({
            "zpid": zpid,
            "detailUrl": zpids[str(zpid)]["detailUrl"],
            "priceHistory": requests.get(api_url, params=params).json()["data"]["priceHistory"]
        })
    return price_history

@app.route("/", methods = ["POST", "GET"])
def main():
    if request.method == "POST":
        # Get zillow search url from user    
        listing_url = request.form.get("listing_url")
        if "zillow.com" not in listing_url:
            return render_template("index.html", errorMessage="Please enter a url that contains 'zillow.com'")
        
        # Get zpids of properties returned by user search
        zpids, status_code = get_zpids(listing_url)
        if status_code != 200:
            return render_template("index.html", errorMessage=f"Received status code {status_code} from the url provided")
        elif not zpids:
            return render_template("index.html", errorMessage="Reached the URL but no properties were returned by the search")
        
        # Get price history for each zpid returned
        pricehistory = price_history(zpids)
        return render_template("data.html", zpids=zpids, price_history=pricehistory)
    else:
        return render_template("index.html")
