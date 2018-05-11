from bs4 import BeautifulSoup
import requests
import urllib.parse as urlparse

root_url = 'https://www.youtube.com'

# get a youtube website
url = 'https://www.youtube.com/watch?v=oTPZWpQ9pbA'
parsed = urlparse.urlparse(url)

page = requests.get(url)

# parse the website with beautiful soup
soup = BeautifulSoup(page.content, "html.parser")

# print video id
print('video ID: ' + str(urlparse.parse_qs(parsed.query)['v'][0]) + '\n')

# print video title
title = soup.find('span', attrs={'class':'watch-title'}).text
print('video title: '+title + '\n')

# print video description
description = soup.find('p', attrs={'id':'eow-description'}).text
print('video description: \n'+ description + '\n')
# give url of next video
next_video = root_url+ soup.find('div', attrs={'class':'content-wrapper'}).a['href']
print('link of another video: \n' + next_video)




