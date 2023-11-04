from flask import Flask, render_template
from main import topKeywordsQuery, countArticlesByMonthQuery, articlesWithImageQuery, countAllDocuments

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/top-keywords')
def topKeywords():
    res = topKeywordsQuery()
    # print(res)
    return res


@app.route('/count-articles-by-month')
def countArticlesByMonth():
    res = countArticlesByMonthQuery()
    # print(res)
    return res


@app.route('/articles-with-image')
def articlesWithImage():
    res = articlesWithImageQuery()
    # print(res)
    return res


@app.route('/count')
def countDocuments():
    res = countAllDocuments()
    print(res)
    return res


if __name__ == '__main__':
    app.run()
