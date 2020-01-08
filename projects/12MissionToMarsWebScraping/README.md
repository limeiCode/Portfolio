
# Mission to Mars Web Scraping

This project used <span style="color:purple;">**HTML, CSS, Bootstrap Table, Flask, Selenium, Beautiful Soup**</span> and <span style="color:purple;">**MongoDB**</span> to scrape from various websites for data related to the Mission to Mars then render the templates with the scraped data by using <span style="color:purple;">**Jinja Template**</span> library on a HTML page. 

- - -

![mission_to_mars1.jpg](static/images/mission_to_mars1.jpg)

- - -



## Scraping source websites and contents

* Scrape the [**NASA Mars site**](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. 

* Scrape the [**NASA JPL site**](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars) and collect the current Featured Mars Image.

* Scrapte [**Twitter site**](https://twitter.com/marswxreport?lang=en) and collect the latest Mars weather tweet. 

* Scrape [**Space Facts site**](https://space-facts.com/mars/) and collect the facts about the planet including Diameter, Mass, etc.

* Scrape [**USGS Astrogeology site**](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) and collect high resolution images for each of Mar's hemispheres.

## Technologies Used

*  **Bootstrap Table** is used to set the layout of the webpage and it can makes a *Responsive Tables* by using `table-responsive` class. It scrolls horizontally up to small devices (under 768px) and when viewing on anything larger than 768px wide no any difference.

* Web Scraping Framework **Selenium** and it's API **Webdriver** are used to connect with the browser and navigate the sites.

* Third party Python library **Beautiful Soup** is used to parse out the necessary data from HTML documents using the parse tree created by Beautiful Soup.

* Python data manipulation and analysis library **Pandas** is used for importing table data from a webpage adn convert the data to a HTML table string. 

* Python web framework **Flask** and it's extensions **Render_Template** and **Redirect** are used to establish database connection,  to render templates with specific data by using Jinja template library, redirect route back to home page.

* Python distribution **PyMongo** is used in this *CRUD* application for working with MongoDB through **Flask-PyMongo**'s bridging Flask and PyMongo. MongoDB stores flexible JSON-like documents which is a searchable repository of Python dictionaries. 

## Project Files:

* **scrape_mars.py**: This file works as a scraper, it has a function called `scrape` that will execute all scraping code from five websites and return one Python dictionary containing all of the scraped data. 

* **app.py**: It is the Flask Server which has two routes. The root route `/` that will query Mongo database and pass the current mars data into an HTML template to display the data. The other route called `/scrape` that will import `scrape_mars.py` script and call `scrape` function and store new mars data - the return value in Mongo as a Python dictionary. 

* **index.html**: It is `Jinja` template HTML file structured by using `bootstrap`, it takes the mars data dictionary and displays all of the data in the appropriate HTML elements.

* **mars.db**: It is created when it is connected by `PyMongo`. And it holds only one document which is the *most recent* scrapped data.

## Final Results

By sending requests from **Brower** to the **Flask Server** can get below results: 

- - -

![result_1.png](static/images/12run.gif)


- - -
