import requests
from bs4 import BeautifulSoup
import csv

response = requests.get('https://www.scrapethissite.com/pages/simple/')

# print(response.status_code)
# print(response.text)

soup = BeautifulSoup(response.text, "html.parser")

countryBlocks = soup.find_all("div", class_="col-md-4 country")
print(f"Number of countries: {len(countryBlocks)}")

result = []
for blocks in countryBlocks:
    nameElement = blocks.find("h3", class_="country-name")
    countryName = nameElement.get_text(strip=True)

    capitalElement = blocks.find("span", class_="country-capital")
    capitalName = capitalElement.get_text(strip=True)
    result.append({"name": countryName, "capital": capitalName })

print(f"jumlah result: {len(result)}")

with open("data.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldNames = ["name", "capital"]
    writer = csv.DictWriter(csvfile, fieldnames=["name","capital"])

    writer.writeheader()

    for items in result:
        writer.writerow(items)