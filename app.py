from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars_scraped

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find all record of data from the mongo database
    mars_data = mongo.db.mars_table.find_one()
    news_title = mars_data['news_title']
    news_body = mars_data['news_body']
    image_url = mars_data['image_url']
    featured_image_url = mars_data['featured_image_url']
    mars_weather = mars_data['mars_weather']
    list_url = mars_data['list_url']
    hemisphere_range_urls = mars_data['hemisphere_range_urls']
    
    # Return template and data
    return render_template("index.html", news_title=news_title,
                            news_body=news_body,
                            image_url=image_url,
                            featured_image_url=featured_image_url,
                            mars_weather=mars_weather,
                            list_url=list_url,
                            hemisphere_range_urls=hemisphere_range_urls
    )


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    news_title, news_body, image_url, featured_image_url, mars_weather, list_url, hemisphere_range_urls = mission_to_mars_scraped.scrape_info()

    mars_data = {
        'news_title':news_title, 
        'news_body':news_body,
        'image_url':image_url,
        'featured_image_url':featured_image_url,
        'mars_weather':mars_weather,
        'list_url':list_url,
        'hemisphere_range_urls':hemisphere_range_urls

    }
    # Update the Mongo database using update and upsert=True
    mongo.db.mars_table.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)


   # return news_title, news_body, 