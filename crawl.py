from bs4 import BeautifulSoup as bs
import urllib.parse as urlparse
import requests
import re

# Import files from youtube data API
from googleapiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

############## Manual HTML Crawler ##############
# Probably going to be deprecated and deleted soon

'''
Video to be used here:
"SpiegelMining – Reverse Engineering von Spiegel-Online (33c3)"

This video is from a talk from the 33rd Chaos Communication Congress.
The topic is Data Mining, and how much information can be gathered
by meta data from articles on Spiegel Online
'''
def html_parse():
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


############# Youtube Data API #############

DEVELOPER_KEY = "AIzaSyC3q6vFOPgL4tHDRZxBCqkRO9Uh4Q49GxM"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

SEARCH_TERM = "Lecture"     # Term you want to search for
MAX_RESULTS = 25            # Maximum amount of results to be returned by YouTube

# Create GET request arguments
argparser.add_argument("--q", help="Search term", default=SEARCH_TERM)
argparser.add_argument("--max-results", help="Max results", default=MAX_RESULTS)
args = argparser.parse_args()

# Get an API reference
yt = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

# Search
try:
    search = yt.search().list(
            q=args.q,
            part="id,snippet",
            maxResults=args.max_results)
    search_response = search.execute()

    videos = []
    channels = []
    playlists = []

    # Parse the search results

    for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
      elif search_result["id"]["kind"] == "youtube#channel":
        channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
      elif search_result["id"]["kind"] == "youtube#playlist":
        playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))

    print("Videos:\n", "\n".join(videos), "\n")
    print("Channels:\n", "\n".join(channels), "\n")
    print("Playlists:\n", "\n".join(playlists), "\n")

except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
