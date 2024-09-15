# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 23:53:04 2024

@author: adity
"""

import requests
from bs4 import BeautifulSoup
from time import sleep
from threading import Thread
import schedule
from models import db, NewsArticle  # Your database models

# Function to scrape news articles
def scrape_news():
    url = "https://news.ycombinator.com/"  # Replace with your news source
    response = requests.get(url)
    
    # Parse the content (replace with your specific parsing logic)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('a', class_='storylink')  # Example from Hacker News

    for article in articles:
        title = article.text
        link = article['href']

        # Check if article already exists
        existing_article = NewsArticle.query.filter_by(link=link).first()
        if not existing_article:
            # Add to the database
            new_article = NewsArticle(title=title, link=link)
            db.session.add(new_article)
            db.session.commit()

# Schedule scraper to run periodically (every hour)
def schedule_scraper():
    schedule.every(1).hours.do(scrape_news)

    while True:
        schedule.run_pending()
        sleep(1)

# Start the scraper in a background thread
def start_scraper():
    thread = Thread(target=schedule_scraper)
    thread.daemon = True  # This ensures the thread will exit when the main program does
    thread.start()
