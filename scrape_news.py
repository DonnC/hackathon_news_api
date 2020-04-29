# main news scraper
from bs4 import BeautifulSoup as bs
import requests as req

def getPosts(url):
   # get all posts on covid-19
   #print("[INFO] requesting page url: ", url)

   resp = req.get(url)

   # release connection obj
   resp.close()

   webpage = resp
   page = webpage.content
   soup = bs(page, 'html5lib')
   posts = soup.find_all('ul', class_='posts-items')

   covid_posts = posts[0]
   # each page , contains 10 posts
   all_posts = covid_posts.find_all('li')

   return all_posts

def getPostDetail(post):
   # get individual post details
   POST = {}

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

def getNews(url):
   # get all news
   news = []
   posts = getPosts(url)

   count = 1
   for post in posts:
      news.append(getPostDetail(post))

      count += 1

   return news

'''
BASE_URL = "https://www.openparly.co.zw/category/corona-virus/"
PAGE_2   = "https://www.openparly.co.zw/category/corona-virus/page/2/"
PAGE_3   = "https://www.openparly.co.zw/category/corona-virus/page/3/"

print('getting page 1..')
covid_posts_page_1 = news(BASE_URL)
print('getting page 2..')
covid_posts_page_2 = news(PAGE_2)
page_2_posts = covid_posts_page_2[0]

for post in page_2_posts:
   #if type(post) == dict:
   covid_posts_page_1.append(post)

from pprint import pprint

print('total posts = ', len(covid_posts_page_1))
pprint(covid_posts_page_1)
'''