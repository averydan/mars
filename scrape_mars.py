import pandas as pd
import os
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape_nasa():
    nasa_news_site_url = 'https://mars.nasa.gov/news/'
    html = urlopen(nasa_news_site_url)
    nasa_news_data = bs(html, 'lxml')
    nasa_news = {
        'title': nasa_news_data.find_all("div", {"class": "content_title"})[0].text.strip('\n'),
        'paragraph': nasa_news_data.find_all("div", {"class": "rollover_description_inner"})[0].text.strip('\n')
    }
    return nasa_news

def scrape_featured_image():
    browser=init()
    featured_image_site_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(featured_image_site_url)
    html = browser.html
    featured_image_data = bs(html, 'html.parser')
    imgLinkString=featured_image_data.find_all("a",{"class": "showimg fancybox-thumbs"})
    browser.quit()
    featured_image_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"+imgLinkString[0]['href']
    return featured_image_url

def scrape_mars_facts():
    mars_facts_site_url = 'https://space-facts.com/mars/'
    mars_facts = pd.DataFrame(pd.read_html(mars_facts_site_url)[0])
    html_table = mars_facts.to_html()
    return html_table


def scrape_hemispheres():
    image_urls=[]
    browser=init()
    hemisphere_images_site_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    for i in range(0,4):
        browser.visit(hemisphere_images_site_url)
        browser.find_by_css("a.product-item h3")[i].click()
        html = browser.html
        hemisphere_data = bs(html, "html.parser")
        title = hemisphere_data.find('h2').text
        image_url = hemisphere_data.find_all('a','target'=='_blank')[4]["href"]
        image_url = {
            "title": title,
            "img_url": image_url}
        image_urls.append(image_url)
    browser.quit()
    return image_urls


def testing():
    test_mars_facts_site_url = 'https://space-facts.com/mars/'
    test_mars_facts = pd.read_html(test_mars_facts_site_url)[0]
    fact_list = []
    count = 0
    for i in test_mars_facts[0]:
        fact_list.append([i,test_mars_facts[1][count]])
        count +=1
    return(fact_list)


def scrape_all():
    scraped_data = {
        'nasa_news': scrape_nasa(),
        'featured_image': scrape_featured_image(),
        'mars_facts': testing(),
        'hemispheres': scrape_hemispheres(),
        'if_blank': ''
    }
    return scraped_data
    
blank_data = {
    'nasa_news': {'title':'No Value', 'title':'No Value'},
    'featured_image': 'broken_img.jpeg',
    'mars_facts': [['No', 'Value']],
    'hemispheres': [{'title': 'No Value','img_url': 'broken_img.jpeg'},{'title': 'No Value','img_url': 'broken_img.jpeg'},{'title': 'No Value','img_url': 'broken_img.jpeg'},{'title': 'No Value','img_url': 'broken_img.jpeg'}],
    'if_blank': "Oh no, you don't have any data! Try scraping some below!"
}