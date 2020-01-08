# Dependencies: import necessary libraries
from selenium import webdriver  ## Web Scraping Framework # selenium webdriver API
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():
    return webdriver.Chrome("windows/chromedriver")

def scrape():
    browser = init_browser()
    marsdata_scrp_dict = {}

    # # <1>NASA Mars News:
    # Use Selenium to navigate the site and Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text 

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.get(url)
    html = browser.page_source

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')

    # Examine the results, then determine element that contains sought info
    # print(soup.body.prettify())

    # Access the latest news with CSS selectors
    news_list = soup.find_all('div', class_ = 'list_text')
    latestnews_title = news_list[0].find('div', class_ = 'content_title').a.text
    latestnews_p = news_list[0].find('div', class_ = 'article_teaser_body').text
    
    # Add scraped data into the dictionary return variable 
    marsdata_scrp_dict["latestnews_title"] = latestnews_title
    marsdata_scrp_dict["latestnews_p"] = latestnews_p




    # # <2> JPL Mars Space Images - Featured Image :
    # Use Selenium to navigate the site and Scrape the image url for the current Featured Mars Image

    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.get(url)
    html = browser.page_source

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')

    # Examine the results, then determine element that contains sought info
    # print(soup.body.prettify())

    # Access the image url with CSS selectors
    imageurl_list = soup.find_all('footer')
    featured_image_url = 'https://www.jpl.nasa.gov' + imageurl_list[0].find('a', class_='button fancybox')['data-fancybox-href']        
 
    # Add scraped data into the dictionary return variable 
    marsdata_scrp_dict["featured_image_url"] = featured_image_url

    # <3> Mars Weather
    # Use Selenium to navigate the site and Scrape the latest Mars weather tweet from the page

    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.get(url)
    html = browser.page_source

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')

    # Examine the results, then determine element that contains sought info
    # print(soup.body.prettify())

    # Access the latest Mars weather tweet with CSS selectors
    tweet_list = soup.find_all('div',class_ = 'js-tweet-text-container')
    latestmarsweather_tweet = tweet_list[0].find('p').text    

    # Add scraped data into the dictionary return variable 
    marsdata_scrp_dict["latestmarsweather_tweet"] = latestmarsweather_tweet


    # # <4> Mars Facts
    # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc

    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    # Save data from the table containing facts into Panda DataFrame
    df = tables[0] # tables[1]: Error: ValueError: Length mismatch: Expected axis has 3 elements, new values have 2 elements
    df.columns = ['fact', 'value']  
    df.set_index('fact', inplace = True)

    # Use Pandas to convert the data to a HTML table string
    html_table = df.to_html()
    html_table.replace('\n', '')

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html_table, 'html.parser').tbody

    tablerow_list = soup.find_all('tr')
    tablerowth_list = soup.find_all('th')
    tablerowtd_list = soup.find_all('td')

    tablerowthvl_list = []
    tablerowtdvl_list = []
    tablerowthvlvl_list = []
    tablerowtdvlvl_list = []

    for r in tablerowth_list:
        n = str(r)[4:]
        tablerowthvl_list.append(n)
    for r in tablerowthvl_list:
        n = str(r)[:-6]
        tablerowthvlvl_list.append(n)    

    for r in tablerowtd_list:
        n = str(r)[4:]
        tablerowtdvl_list.append(n)
    for r in tablerowtdvl_list:
        n = str(r)[:-6]
        tablerowtdvlvl_list.append(n)    

    th_and_td = zip(tablerowthvlvl_list,tablerowtdvlvl_list)

    thtd_dict = {}
    thtd_dictlist = []

    for i in th_and_td:
        l = list(i)
        thtd_dict["fact"] = l[0]
        thtd_dict["value"] = l[1]
        thtd_dictlist.append(thtd_dict.copy()) 

    # Add scraped data into the dictionary return variable 
    marsdata_scrp_dict["thtd_dictlist"] = thtd_dictlist


    # # <5> Mars Hemispheres
    # Use Selenium to navigate the site and Scrape high resolution images for each of Mar's hemispheres

    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.get(url)
    html = browser.page_source

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')

    # Examine the results, then determine element that contains sought info
    # print(soup.body.prettify())

    hemisphere_dictlist = []
    hemisphere_dict = {}
    item_list = soup.find_all('div', class_ = "item")
    # print(soup.body.prettify() ) 

    # Access the high resolution images for each of Mar's hemispheres with CSS selectors
    for m in item_list:
        hemisphere_dict["title"] = m.div.a.h3.text
        pageurlstr = "https://astrogeology.usgs.gov" + m.div.a["href"] 
        browser.get(pageurlstr)   
        htmlnew = browser.page_source
        soup = bs(htmlnew, 'html.parser').body
        imageurlstr = "https://astrogeology.usgs.gov" + soup.find('img', class_ = "wide-image")["src"]
        hemisphere_dict["img_url"] = imageurlstr
        hemisphere_dictlist.append(hemisphere_dict.copy())
        
    # Add scraped data into the dictionary return variable 
    marsdata_scrp_dict["hemisphere_dictlist"] = hemisphere_dictlist                                             
    

    # Close the browser after scraping
    browser.close() 
   
    # Return scapting result dictionary to the caller in Flask server app.py for later be passed to Index.html Jinja template 
    return marsdata_scrp_dict 
