# News Dashboard using Flask

## Introduction
This is a web scraping project that scrapes articles off News websites, stores them into a MongoDB Database, performs queries, connecting the results with a Flask dashboard

## Used Tech Stack

- **FrontEnd**: HTML, CSS, JavaScript
- **BackEnd**: Flask
- **DataBase**: MongoDB
- **Charts Resources**: HighCharts

## File Guide

### app.py
The python file holding the flask application, and connection
### main.py
The main Python file that you need to run will return the local URL link, and after opening it, it will present the dashboard page.
### crawler.py
This is the main file responsible for crawling and scraping the news from the websites
### static/
This folder holds the static images for the favicon and logo
### templates/home.html
This is the main HTML file used by the Flask application to build the website with the charts visualization
### almayadeen_sitemap.json
The News website holds a main sitemap, listing child sitemaps by month, Al-Mayadeen separates them into sitemaps by month
### almayadeen_news_sample.jsonl
This is a JSON Lines file holding 100 samples of the news scraped from the child sitemaps
### .env / .envexample
This file holds the environment variable for the MongoDB connection for security reasons, copy the .envexample and rename it to .env, then add the connection string

## Screenshots

![Dashboard](https://imgur.com/wDfDbQl)
![Wordcloud of Top Keywords in News Articles](https://imgur.com/NJA3ceS)
![Line Chart of Number of Articles Published Per Month](https://imgur.com/vfJG3HQ)
![Pie Chart of Articles With Image Attachment VS. Articles Without Image Attachment](https://imgur.com/H5yna8w)
