from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

MONGO_URL = os.environ.get("MONGODB_URI")
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/mars_app"

app = Flask(__name__)

app.config["MONGO_URI"] = MONGO_URL
mongo = PyMongo(app)


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrapper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run()