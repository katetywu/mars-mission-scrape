from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt


# Set the executable path and initialize the chrome browser
# ------------------------- Windows -------------------------------
# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)

# ------------------------- MAC -----------------------------------
# executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
# browser = Browser('chrome', **executable_path, headless=False)


# NASA Mars News Site
def mars_news(browser):
    marsNews = "https://mars.nasa.gov/news/"
    browser.visit(marsNews)

    # Get the first list item and wait for half a second, if not immediately present
    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=0.5)
    
    html = browser.html
    soupNews = BeautifulSoup(html, 'html.parser')

    try:
        # Get everything about slide element
        slideElement = soupNews.select_one('ul.item_list li.slide')
        
        # Use the parent element to find the first <a> tag and save it as news title and paragraph
        newsTitle = slideElement.find('div', class_='content_title').get_text()
        newsPara = slideElement.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return newsTitle, newsPara


# JPL Space Featured Image
def mars_image(browser):
    JPLImage = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(JPLImage)

    # Ask splinter to click a button on the site with class name full_image
    # <button class="full_image">Full Image</button>
    fullImgButton = browser.find_by_id('full_image')
    fullImgButton.click()    

    # Find the more button and click it
    # wait_time: giving splinter 1s to delay
    browser.is_element_present_by_text('more info', wait_time=1)
    moreInfoElement = browser.links.find_by_partial_text('more info')
    moreInfoElement.click()

    html = browser.html
    soupImage = BeautifulSoup(html, 'html.parser')

    img = soupImage.select_one('figure.lede a img')
    try:
        imgURL = img.get('src')
    except AttributeError:
        return None

    imgURL = f"https://www.jpl.nasa.gov{imgURL}"

    return imgURL


# Mars Hemisphere
def mars_hemis(browser):
    marsHemis = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(marsHemis)
    hemisImageURL = []

    # Get a list of all the hemispheres
    links = browser.find_by_css("a.itemLink h3")
    for item in range(len(links)):
        hemis = {}
        
        # Find the element on each loop to avoid a stale element exception
        browser.find_by_css('a.itemLink h3')[item].click()
        
        # Find sample image anchor tag and extract the href
        sampleElement = browser.links.find_by_text('Sample').first
        hemis['img_url'] = sampleElement['href']
        
        # Get hemisphere titles
        hemis['title'] = browser.find_by_css('h2.title').text
        
        # Append hemisphere object to list
        hemisImageURL.append(hemis)
        
        # Navigate backwards
        browser.back()

    return hemisImageURL


# Create a helper function for hemis
# def scrape_hemis(html_text):
#     soupHemis = BeautifulSoup(html_text, 'html.parser')
    
#     try:
#         titleElement = soupHemis.find('h2', class_="title").get_text()
#         sampleElement = soupHemis.find('a', text="Sample").get('href')
#     except AttributeError:
#         titleElement = None
#         sampleElement = None
#     hemisphere = {
#         "title": titleElement,
#         "img_url": sampleElement
#     }
#     return hemisphere
 

# Mars Facts
def mars_facts():
    try:
        marsFacts = "https://space-facts.com/mars/"
        df = pd.read_html(marsFacts)[0]
    except BaseException:
        return None
    df.columns=['Description', 'Value']
    df.set_index('Description', inplace=True)

    return df.to_html(classes="table table-striped")


# Mars Weather
# def mars_weather(browser):
#     urlWeather = "https://twitter.com/marswxreport?lang=en"
#     browser.visit(urlWeather)

#     html = browser.html
#     soupWeather = BeautifulSoup(html, 'html.parser')

#     # Find a tweet with the data-name 'Mars Weather'
#     marsWeatherTweet = soupWeather.find('div', 
#                                 attrs={"class": "tweet", 
#                                         "data-name": "Mars Weather"})

#     # Search within the tweet for <p> tag containing the tweet text
#     marsWeather = marsWeatherTweet.find('p', 'tweet-text').get_text()
    
#     return marsWeather


def scrape_all():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    newsTitle, newsPara = mars_news(browser)
    image = mars_image(browser)
    hemisImage = mars_hemis(browser)
    facts = mars_facts()
    timestamp = dt.datetime.now()
    # marsWeather = mars_weather(browser)

    marsData = {
        "news_title" : newsTitle,
        "news_paragraph" : newsPara,
        "featured_image": image,
        "hemispheres" : hemisImage,
        "facts": facts,
        "last_modified" : timestamp
        # "weather" : marsWeather
    }
    browser.quit()
    return marsData


if __name__ == "__main__":
    print(scrape_all())



