import jsonlines as jsonlines
import requests
from bs4 import BeautifulSoup
import json


def parse_sitemap(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        print(f"Failed to fetch data from {url}")
        return None


def extract_news_child(sitemap_url, output_file):
    news_source = 0  # defaults to mayadeen
    if sitemap_url.startswith('https://www.aljazeera.com/'):
        news_source = 1
    sitemap = parse_sitemap(sitemap_url)
    if sitemap:
        # Find all <url> elements in the sitemap
        url_elements = sitemap.find_all('url')
        # print(url_elements)

        for url_element in url_elements:
            # print(url_element)
            loc = url_element.find('loc')
            lastmod = url_element.find('lastmod')
            name = url_element.find('news:name')
            language = url_element.find('news:language')
            publication_date = url_element.find('news:publication_date')
            title = url_element.find('news:title')
            keywords = url_element.find('news:keywords')
            if news_source == 0:
                image_loc = url_element.find('image:loc')
            else:
                image = url_element.find('image')
                print(image.string)
                image_loc = image.find('loc')
                # print(image_loc)

            if loc and loc.text:
                url = loc.text
            else:
                url = None

            if lastmod and lastmod.text:
                last_modified = lastmod.text
            else:
                last_modified = None

            if name and name.text:
                name = name.text
            else:
                name = None

            if language and language.text:
                language = language.text
            else:
                language = None

            if publication_date and publication_date.text:
                publication_date = publication_date.text
            else:
                publication_date = None

            if title and title.text:
                title = title.text
            else:
                title = None

            if keywords and keywords.text:
                keywords = keywords.text
            else:
                keywords = None

            if image_loc and image_loc.text:
                image_loc = image_loc.text
            else:
                image_loc = None

            with jsonlines.open(output_file, mode='a') as writer:
                writer.write({'url': url, 'last_modified': last_modified, 'name': name, 'language': language,
                              'publication_date': publication_date, 'title': title, 'keywords': keywords,
                              'image': image_loc})

        print(f"Data extracted from {sitemap_url} and saved in {output_file}")


def extract_news(sitemap_url, sitemap_file, news_file):
    sitemap = parse_sitemap(sitemap_url)
    if sitemap:
        # Find all <sitemap> elements in the sitemap
        sitemap_elements = sitemap.find_all('sitemap')
        # print(sitemap_elements)

        data = []
        for sitemap_element in sitemap_elements:
            # print(sitemap_element)
            loc = sitemap_element.find('loc')
            lastmod = sitemap_element.find('lastmod')

            if loc and loc.text:
                url = loc.text
            else:
                url = None

            if lastmod and lastmod.text:
                last_modified = lastmod.text
            else:
                last_modified = None

            extract_news_child(url, news_file)

            data.append({'url': url, 'last_modified': last_modified})

        # Save the extracted data in a JSON file
        with open(sitemap_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Data extracted from {sitemap_url} and saved in {sitemap_file}")
