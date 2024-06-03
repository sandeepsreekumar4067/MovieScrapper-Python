from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
from dotenv import load_dotenv
import os
import random
import string 

from dotenv import load_dotenv

load_dotenv() 
URL = os.getenv("URL")

start_time = time.time()
def insideMovies(link, driver):
    driver.get(link)
    try:
        # Wait for the audience score element to be present, if available
        try:
            audience_score_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "rt-button[slot='audienceScore'] rt-text"))
            )
            audience_score = audience_score_element.text.strip()
        except TimeoutException:
            audience_score = "N/A"

        # Wait for the ratings element to be present, if available
        try:
            ratings_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "rt-link[slot='audienceReviews']"))
            )
            ratings = ratings_element.text.strip()
        except TimeoutException:
            ratings = "N/A"

        # Wait for the description element to be present
        description_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "drawer-more[slot='description'] rt-text[slot='content']"))
        )
        description = description_element.text.strip()
        
    except TimeoutException:
        audience_score = "N/A"
        ratings = "N/A"
        description = "N/A"
    
    return audience_score, ratings, description


movie = input("Enter the Movie : ")
#initialise the necessary things to run chrome headless
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('window-size=1920x1080')
#initialise the webdriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

driver.get(URL)


try:
    searchField = WebDriverWait(driver,10).until(
        EC.visibility_of_element_located((By.CLASS_NAME,"search-text"))
    )
    print("found the search field")
except:
    print("something err happened")
searchField.clear()
searchField.send_keys(movie)
searchField.send_keys(Keys.RETURN)

try:
    WebDriverWait(driver,15).until(
        EC.presence_of_element_located((By.CLASS_NAME,"search__main"))
    )
    print("found the title")
except:
    print("something happened")
result_page = BeautifulSoup(driver.page_source,"html.parser")
movie_entries = result_page.select('search-page-media-row[data-qa="data-row"]')

# Extract details for each movie
relatedMovies = []
movieDetails=[]
for entry in movie_entries:
    title_tag = entry.select_one('a[data-qa="info-name"]')
    title = title_tag.get_text(strip=True) if title_tag else "N/A"
    
    year = entry.get('releaseyear', "N/A")
    if(title==movie):
        movieyear=year
        movieCast=cast
    cast = entry.get('cast', "N/A")
    link = title_tag.get('href', "N/A") if title_tag else "N/A"
    movie_data = {
        "title": title,
        "year": year,
        "cast": cast,
        "link": link,
    }
    relatedMovies.append(movie_data)


if relatedMovies:
    first_movie_link = relatedMovies[0]['link']
    first_movie_details = insideMovies(first_movie_link, driver)
    audience_score, ratings, description = first_movie_details
    movie_data = {
        "title": relatedMovies[0]['title'],
        "year": relatedMovies[0]['year'],
        "cast": relatedMovies[0]['cast'],
        "audience_score": audience_score,
        "ratings": ratings,
        "description": description
    }
    movieDetails.append(movie_data)


movieJson = json.dumps(movieDetails,indent=4)


print("searched movie details : \n")
print(movieJson)

relatedMoviesJson = json.dumps(relatedMovies,indent=4)
print("\n\nrelated Movie Suggestions : \n")
print(relatedMoviesJson)



driver.quit()