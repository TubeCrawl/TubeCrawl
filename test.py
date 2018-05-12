from bs4 import BeautifulSoup as bs
import urllib.parse as urlparse
import requests

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

# Find the title of the video using its tag and id
title = page.find('span', id="eow-title").text
print("Video title:")
print(title)
print()

# Parse the video URL to get the video ID
parsed_url = urlparse.urlparse(url)        # This is a 6-tuple, we need to get 'query' for GET params
query = parsed_url.query
video_id = urlparse.parse_qs(query)['v'][0]
print('Video ID: ' + str(video_id))
print('Query: ' + str(query))
