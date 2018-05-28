from bs4 import BeautifulSoup as bs
import urllib.parse as urlparse
import requests
import re

'''
Video to be used here:
"SpiegelMining – Reverse Engineering von Spiegel-Online (33c3)"

This video is from a talk from the 33rd Chaos Communication Congress.
The topic is Data Mining, and how much information can be gathered
by meta data from articles on Spiegel Online
'''

# Download the page and parse it
url = 'https://www.youtube.com/watch?v=-YpwsdRKt8Q'
raw_page = requests.get(url).content
page = bs(raw_page, 'html.parser')

# Find video title using html tag and id, crop unnecessary characters
title = page.find('span', id="eow-title").text
title = title[5:-3]
print("Video title: "+title )

# Parse the video URL to get the video ID
parsed_url = urlparse.urlparse(url)        # This is a 6-tuple, we need to get 'query' for GET params
query = parsed_url.query
video_id = urlparse.parse_qs(query)['v'][0]
print('Video ID: ' +str(video_id))
print('Query: ' + str(query))

# Find and print URL for the first recommended video
for a in page.find_all('a'):
    link = a.get('href')
    if (link.startswith('/watch?v=')):
        print('Recommended: https://www.youtube.com'+link)
        break

# Find and print video description
descr = page.find('p', id='eow-description').text
print('\nDescription:\n'+descr)
