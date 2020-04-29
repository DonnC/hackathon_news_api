# scrape covid-19 news from openparly
'''
   @author: Donald C
   @github: @DonnC
'''
from flask import Flask, jsonify
from bs4 import BeautifulSoup as bs
import requests as req

BASE_URL = "https://www.openparly.co.zw/category/corona-virus/"
PAGE_2 = "https://www.openparly.co.zw/category/corona-virus/page/2/"
PAGE_3 = "https://www.openparly.co.zw/category/corona-virus/page/3/"

app = Flask(__name__)


def getPosts(url=BASE_URL):
   # get all posts on covid-19
   print("[INFO] requesting page url: ", url)

   resp = req.get(url)

   # release connection obj
   resp.close()

   webpage = resp
   page = webpage.content
   #soup = bs(page, 'html5lib')
   soup = bs(page)
   posts = soup.find_all('ul', class_='posts-items')

   covid_posts = posts[0]
   # each page , contains 10 posts
   all_posts = covid_posts.find_all('li')

   return all_posts


def getPostDetail(post):
   # get individual post details
   POST = {}

   print('[INFO] getting post data..')

   image = post.find('img')['src']
   image = image.split('?resize')[0]
   author_meta = post.find('div', class_='post-meta')
   author_profile = author_meta.find('a')['href']
   author = author_meta.find('a').text
   posted = post.find('span', class_='date meta-item').text
   title = post.find('h3', class_='post-title').text
   summary = post.find('p', class_='post-excerpt').text
   url = post.find('a', class_='more-link button')['href']

   POST['image'] = image.strip()
   POST['author'] = author.strip()
   POST['posted'] = posted.strip()
   POST['title'] = title.strip()
   POST['summary'] = summary.strip()
   POST['url'] = url.strip()

   return POST


def getNews():
   # get all news
   news = []
   posts = getPosts()

   count = 1
   for post in posts:
      news.append(getPostDetail(post))

      count += 1

   return news


@app.route('/v1/hackathon/news')
def news():
   try:
      result = {
            'status': 'OK',
            'news': getNews()
        }

   except Exception as e:
      print('error: ', e)
      result = {
            'status': 'ERR',
            'news': [None]
            }

   return jsonify(result)

if __name__ == '__main__':
   app.run(debug=False)
