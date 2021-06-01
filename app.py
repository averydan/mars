from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars as sm
app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

@app.route("/")
def home():
        mars_data = mongo.db.collection.find_one()
        if mars_data == None:
            return render_template("index.html", mars=sm.blank_data)
        else:
            return render_template("index.html", mars=mars_data)
@app.route("/scrape")
def scrape():
    mars_data = sm.scrape_all()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")
@app.route("/erase")
def erase():
    mars_data = mongo.db.collection.drop()
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)
