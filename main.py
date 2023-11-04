from crawler import extract_news
import os

from bson.son import SON
from bson.json_util import dumps, loads
from dotenv import load_dotenv, find_dotenv
from flask import jsonify
from pymongo import MongoClient

load_dotenv(find_dotenv())

connection_string = os.environ.get("MONGODB_CONNECTION_STRING")
client = MongoClient(connection_string)

db = client["dgPadProjectDB"]
collection = db["MayadeenNews"]


"""This function is the one in which we insert our pipeline to aggregate, it's created to avoid redundant repetitive code"""
def aggregationQuery(pipeline):
    cursor = collection.aggregate(
        pipeline,
        allowDiskUse=True
    )

    try:
        cursorList = list(cursor)
        jsonData = dumps(cursorList, indent=2)
        return jsonData
    finally:
        cursor.close()


def countArticlesByMonthPipeline():
    return [
        {
            '$project': {
                'year': {
                    '$toInt': {
                        '$substr': [
                            '$publication_date', 0, 4
                        ]
                    }
                },
                'month': {
                    '$toInt': {
                        '$substr': [
                            '$publication_date', 5, 2
                        ]
                    }
                }
            }
        }, {
            '$group': {
                '_id': {
                    'year': '$year',
                    'month': '$month'
                },
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                '_id.year': 1,
                '_id.month': 1
            }
        }
    ]


def topKeywordsPipeline(limit: int):
    return [
        {
            '$project': {
                'keyword': {
                    '$split': [
                        '$keywords', ','
                    ]
                }
            }
        }, {
            '$unwind': {
                'path': '$keyword'
            }
        }, {
            '$group': {
                '_id': '$keyword',
                'keywordCount': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                'keywordCount': -1
            }
        }, {
            '$limit': limit
        }
    ]


def articlesWithImagePipeline():
    return [
        {
            '$match': {
                'image': {
                    '$ne': None
                }
            }
        }, {
            '$count': 'count'
        }
    ]


def countArticlesByMonthQuery():
    return aggregationQuery(countArticlesByMonthPipeline())


def topKeywordsQuery():
    return aggregationQuery(topKeywordsPipeline(100))


def articlesWithImageQuery():
    return aggregationQuery(articlesWithImagePipeline())


def countAllDocuments():
    count = collection.count_documents({})
    return jsonify(count)

"""Calls to crawl the news off news website"""
# extract_news('https://www.aljazeera.com/sitemap.xml', 'aljazeera_sitemap.json', 'aljazeera_news.jsonl')
# extract_news('https://www.almayadeen.net/sitemaps/news.xml', 'almayadeen_sitemap.json', 'almayadeen_news.jsonl')
