from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# Connect to a database. Will create one if not already available.


# from flask import Flask, render_template, redirect

# # Import our pymongo library, which lets us connect our Flask app to our Mongo database.
# import pymongo

# # Create an instance of our Flask app.
# app = Flask(__name__)

# # Create connection variable
# conn = 'mongodb://localhost:27017'

# # Pass connection to the pymongo instance.
# client = pymongo.MongoClient(conn)

# # Connect to a database. Will create one if not already available.
# db = client.mars_db


# Set route
# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    m_data = mongo.db.collection.find_one()
# Return template and data
    return render_template("index.html", mars_data=m_data)

@app.route('/scrape')
def scrape_info():
    
    m_data = scrape_mars.scrape()

    
    mongo.db.collection.update({}, m_data, upsert=True)


    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
