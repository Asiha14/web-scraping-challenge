from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser

def scrape():

    scrape_dict={}

    # Scrape the  NASA Mars News Site 
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    url = "https://mars.nasa.gov/news/"
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    response = browser.html
    soup = BeautifulSoup(response, 'html.parser')
    news_t = soup.find('li', class_='slide').find('div',class_="content_title").find('a').text
    news_p = soup.find('li', class_='slide').find('div', class_="rollover_description_inner").text
    browser.quit()
    scrape_dict.update({'news_t':str(news_t)})
    scrape_dict.update({'news_p':str(news_p)})

    # Scrape for JPL Mars Space Images - Featured Image
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False) 
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)     
    browser.find_link_by_partial_text('FULL IMAGE').first.click()
    browser.find_link_by_partial_text('more info').first.click()
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    f_image = image_soup.select_one("figure.lede a img").get("src")
    featured_image_url = 'https://www.jpl.nasa.gov' +f_image
    scrape_dict.update({'featured_image_url':featured_image_url})
    browser.quit()

    # Scrape for Mars Facts
    table_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(table_url)
    df = tables[0]
    df.columns = ['Index', 'Info']
    df.set_index('Index', inplace=True) 
    df.index.name = None
    df.columns=['']

    scrape_dict.update({'table_df':df.to_html()})

    # Scrape for Mars Hemispheres
    hem_list=[]
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hem_response = requests.get(hem_url)
    hem_soup = BeautifulSoup(hem_response.text, 'html.parser')
    for item in hem_soup.find_all('h3'):
        hem_list.append(item.text)
    hem_browser = Browser('chrome', **executable_path, headless=False)
    h_image_url = [] 
    for item in hem_list:
        hem_browser.visit(hem_url)
        hem_browser.find_link_by_partial_text(item).click()
        hem_browser.find_link_by_partial_text('Open').click()
        hem_html = hem_browser.html
        hem_soup = BeautifulSoup(hem_html, 'html.parser')
        h_image = hem_soup.select_one("div.wide-image-wrapper img.wide-image").get("src")
        h_image_url.append({"title":item, "img_url":'https://astrogeology.usgs.gov'+ h_image})


    scrape_dict.update({'h_image_url':h_image_url})
    hem_browser.quit()

    return scrape_dict
    