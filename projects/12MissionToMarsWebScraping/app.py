# Dependencies: import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__) 

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db") 

# Route to render index.html template using data from Mongo
@app.route("/")
def home():    
    marsdata_mgl = mongo.db.mars.find_one() 
    return render_template("index.html", marsdata_html = marsdata_mgl) 

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():    
    marsdata_scrp = scrape_mars.scrape()      
    # overwrite the existing document 
    mongo.db.mars.update({}, marsdata_scrp, upsert=True)  
    # Redirect back to home page
    return redirect("/") 
    
if __name__ == "__main__":
    app.run(debug=True)
