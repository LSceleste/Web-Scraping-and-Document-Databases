# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import pandas as pd

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

get_ipython().system('which chromedriver')

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://mars.nasa.gov/news/'
browser.visit(url)

html = browser.html

soup = BeautifulSoup(html, 'html.parser')

news_title = soup.find('div', class_= 'content_title').text
news_title

news_body = soup.find('div', class_='article_teaser_body').text
news_body


#browser.quit()

url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url2)


html2 = browser.html

soup2 = BeautifulSoup(html2, 'html.parser')

block1 = soup2.find('section', class_='grid_gallery')
block1.prettify()

block2 = block1.find('a', class_='fancybox')
print(block2)


image_url = block2['data-fancybox-href']
image_url

featured_image_url = 'https://www.jpl.nasa.gov' + image_url
featured_image_url


url3 = 'https://twitter.com/marswxreport?lang=en'


browser.visit(url3)

html3 = browser.html

soup3 = BeautifulSoup(html3, 'html.parser')

block3 = soup3.find('p', class_='js-tweet-text').text
print(block3)

mars_weather = block3
mars_weather

url4 = 'https://space-facts.com/mars/'


table = pd.read_html(url4)
table

html_table = table[0].to_html()
html_table

url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(url5)

html5 = browser.html

soup5 = BeautifulSoup(html5, 'html.parser')


list_links = soup5.find_all('a', class_="product-item")
list_url = []
for l in list_links:
    list_url.append(l["href"])
list_url   

list_url = list_url[::2]
list_url


hemisphere_range_urls = []
for item in list_url: 
    html6 = 'https://astrogeology.usgs.gov' + item
    soup6 = BeautifulSoup(requests.get(html6).text, 'html.parser')
    hemisphere_title = soup6.find('h2').text[:-9]
    hemisphere_url = soup6.find('a', target='_blank')['href']
    hemisphere_range_urls.append({'title': hemisphere_title, 'img_url': hemisphere_url})
hemisphere_range_urls


browser.quit()
