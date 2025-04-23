import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.scrapethissite.com/pages/simple/')

print(response.status_code)
print(response.text)