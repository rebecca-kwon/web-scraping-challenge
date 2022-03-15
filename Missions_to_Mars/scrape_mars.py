from splinter import Browser
import requests
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_info():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # #### NASA Mars News
    # - Scrape the Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(2)

    # #### HTML 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # #### Assign Title & Paragraph Text to variables 
    title = soup.find('div', class_='content_title').text
    paragraph= soup.find('div', class_='article_teaser_body').text


    # #### JPL Image URL
    # - Visit the url for the Featured Space Image site here.
    # 
    # - Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    # 
    # - Make sure to find the image url to the full size .jpg image.
    # 
    # - Make sure to save a complete url string for this image.
    jplurl='https://spaceimages-mars.com/'
    browser.visit(jplurl)
    time.sleep(2)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    featured_image_url=soup2.findAll('img', class_='headerimage fade-in')[0]['src']
    featured_image_url=jplurl+featured_image_url

    print(featured_image_url)


    # #### Mars Facts
    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # 
    # Use Pandas to convert the data to a HTML table string.

    marsfactsurl='https://galaxyfacts-mars.com/'
    tables = pd.read_html(marsfactsurl)
    time.sleep(2)
    mars_df = tables[0]
    mars_df.columns=mars_df.iloc[0]
    mars_df=mars_df.iloc[1: , :]
    mars_df.head()


    marshtml_table = mars_df.to_html(index=False).replace('\n', '')
    marshtml_table


    # #### Mars Hemispheres
    # - Visit the astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    # 
    # - You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # 
    # - Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    # 
    # - Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.


    pic_url='https://marshemispheres.com/'
    browser.visit(pic_url)
    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')


    items=soup3.find_all('div', class_='item')

    hemisphere_image_urls=[]


    for item in items:
        imagelink=pic_url+item.find('a')['href']
        browser.visit(imagelink)
        html4 = browser.html
        soup4 = BeautifulSoup(html4, 'html.parser')
        imagelink2=pic_url+soup4.find('img',class_='wide-image')['src']
        hemname=item.find('div',class_='description').find('a').text.replace('\n','')[:-9]
        itemdict={"title":hemname,
            "img_url":imagelink2}
        hemisphere_image_urls.append(itemdict)

    hemisphere_image_urls

    mars_data={
        "recentTitle": title,
        "recentParagraph":paragraph,
        "imageURL":featured_image_url,
        "table":marshtml_table,
        "hemispheres":hemisphere_image_urls
    }

    browser.quit()

    return mars_data