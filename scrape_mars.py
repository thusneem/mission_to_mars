

# import necessary libraries
from flask import Flask, render_template
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import re


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {'executable_path': 'C:\chromedriver_win32\chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    # Initialize browser
    browser = init_browser()
    output_file = {}


    #Scrape the(https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text.
    url='https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    output_file['news_title'] = soup.find('div',class_='content_title').get_text()
    output_file['news_paragraphs'] = soup.find('div',class_='article_teaser_body').get_text()


    #Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    url1='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url1)
    html1 = browser.html
    soup1 = bs(html1, 'html.parser')

    mars_image=soup1.find('article',class_='carousel_item')
    mars_url=mars_image['style'].strip()
    extract_url= re.sub('[(){}<>]', '', mars_url)
    result = re.search('background-image: url(.*);',extract_url)
    mars_image_url=result.group(1).strip('\'')
    output_file['featured_img_url']='https://www.jpl.nasa.gov'+ mars_image_url





    # Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page.
    url2='https://twitter.com/marswxreport?lang=en'
    browser.visit(url2)
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')
    output_file['mars_weather']=soup2.find('p',class_='tweet-text').text





    #visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use Pandas to scrape the table containing facts
    url3='http://space-facts.com/mars/'
    browser.visit(url3)
    html3 = browser.html
    soup3 = bs(html3, 'html.parser')

    tables = pd.read_html(url3)
    type(tables)
    df=tables[0]
    df.columns=['description','measurement'] 
    html_table = df.to_html()
    html_table.replace('\n', '')
    output_file['tables']=html_table



    #url4='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    url4='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    html4 = browser.html
    soup4 = bs(html4, 'html.parser')
    hemi_url = soup4.find_all('div', class_='item')
    url_list=[]
    link_title=[]
    dicts_title_link = {}

    for element in hemi_url: 
        link = element.find('a')
        url_list.append('https://astrogeology.usgs.gov'+link['href'])
            
    for url in url_list:
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        elements = soup.find('div',class_='downloads')
        a = elements.find('a')  
        dicts_title_link['image_url'] = a['href']

        title_url=soup.find('h2',class_='title').text 
        title=(' '.join(title_url.split()[:-1])) 
        dicts_title_link['title']=title
               
        link_title.append(dicts_title_link)
        dicts_title_link ={}

    output_file['hemisphere_img_url']=link_title    
    return output_file

