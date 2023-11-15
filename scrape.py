# Importing modules and libraries
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import pandas as pd
import time

LOADMORE = (By.XPATH, '//*[@id="load-more-trigger"]')

def scrape_title(id):
    title_list = []
    rating_list = []
    text_list = []

    num_review = 25

    url = f"https://www.imdb.com/title/{id}/reviews?ref_=tt_urv"
    r = requests.get(url)
    
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    browser.get(url)

    for page in range(num_review):
        try: 
            browser.execute_script("window.scrollTo(0, window.scrollY + 200)")
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable(LOADMORE)).click()
            time.sleep(1)
        except:
            break

    bs = BeautifulSoup(browser.page_source, 'html.parser')

    useful_loop_count = 0

    review = bs.findAll()
    
    for review in bs.findAll('div', {'class': 'review-container'}):
            title = review.a.contents
            try:
                title = ''.join(title)
            except:
                title = "No Title Given"

            date = str(review.find("span", {"class": "review-date"}).contents)
            rating = str(review.findAll('span')[1].contents)

            if date == rating:
                rating = "No Rating given"
            else:
                rating = review.findAll('span')[1].contents
                rating = ''.join(rating)
        
            
            text = review.find("div", {"class": "text" })
            text = text.text


            useful_loop_count += 1

            title_list.append(title)
            rating_list.append(rating)
            text_list.append(text)
    
    review_data = pd.DataFrame(
        {
            'Title': title_list,
            'Rating (out of 10)': rating_list,
            'Review Text': text_list,
        }
    )

    review_data.to_csv(f"{id}_review.csv")
    browser.quit()

scrape_title("tt0060666")