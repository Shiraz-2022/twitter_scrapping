from flask import Flask, jsonify
from scraping_script import scrapping_script
from db import get_mongo_client, get_mongo_db, get_trends_collection
import uuid
import datetime
from flask_cors import CORS
from bson import json_util
import json
import uuid
from datetime import datetime


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/runscript")
def run_script():
    client = get_mongo_client()  
    db = get_mongo_db(client)    
    trends_collection = get_trends_collection(db)  
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


    result = scrapping_script()
    print(result)
    top_trends = result.get("trends")
    proxy_ip = result.get("ip_address")

    if isinstance(top_trends, list):
        trend_data = {
            "unique_id": uuid.uuid4().hex,
            "trends": top_trends,
            "date": dt_string,
            "ip_address": proxy_ip ,
        }


        inserted_id = trends_collection.insert_one(trend_data).inserted_id

        print(inserted_id)

        return json.loads(json_util.dumps({
            "message": "Script executed and data saved to MongoDB",
            "trends": top_trends,
            "trend_data": trend_data,
            "id": str(inserted_id)
        }))
    else:
        return json.loads(json_util.dumps({
            "error": "Failed to fetch trending topics",
            "details": top_trends
        }))

@app.route("/gettrends")
async def get_trends():
    client = get_mongo_client()
    db = get_mongo_db(client)
    trends_collection = get_trends_collection(db)

    # Fetch the latest trend record
    latest_trend = trends_collection.find_one(sort=[("date", -1)])
    if latest_trend:
        return json.loads(json_util.dumps(latest_trend))
    else:
        return jsonify({"error": "No trend data found in MongoDB"})
    
if __name__ == "__main__":
    app.run(debug=True)
