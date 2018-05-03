from bs4 import BeautifulSoup
import requests

# Get an example page
page = requests.get("https://dataquestio.github.io/web-scraping-pages/simple.html")
print(page.content)
print()
print()
print("===================================================================" )
print()
print()

# Parse the page with beautifulsoup, print it out nicely
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())

