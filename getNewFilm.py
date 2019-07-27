import urllib
from bs4 import BeautifulSoup
import requests
page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
#create request and set user agent
#request = urllib.Request('https://scrapethissite.com/pages/simple/')
#request.add_header('User-Agent', 'ScrapingAuthority (ScrapingAuthority.com')

#open page
#open = urllib.urlopen(request)

soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())