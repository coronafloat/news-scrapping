import requests
from bs4 import BeautifulSoup
import csv

response = requests.get('https://search.kompas.com/search?q=tarif+trump&type=article')
BASE_URL = 'https://search.kompas.com/search?q=tarif+trump&type=article' #(WIP) pagination: scrap from next page
page=1 #(WIP) pagination: scrap from next page

print(response.status_code)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    titleTotal = soup.find_all("div", class_="articleItem")
    print(f"Number of News: {len(titleTotal)}\n\n")

    hitung=1
    result = []

    for items in titleTotal:
        # Title
        titleElement = items.find("h2", class_="articleTitle")
        titleValue = titleElement.get_text(strip=True)

        # Isi / Content
        isiElement = items.find("div", class_="articleLead")
        isiValue = isiElement.get_text(strip=True)

        # Date
        dateElement = items.find("div", class_="articlePost")
        dateValue = dateElement.get_text(strip=True)
        
        # Tag
        tagElement = items.find("div", class_="articlePost-subtitle")
        tagValue = tagElement.get_text(strip=True)


        # Result akan berisi array yang diisi object yang isinya data dari berita untuk dimasukkan csv nantinya
        result.append(
            {
                "Judul Berita": titleValue,
                "Isi Berita": isiValue,
                "Tanggal Berita": dateValue,
                "Tag Berita": tagValue,
            }
        )

        # Debug
        print(f"judul ke {hitung}: {titleValue}")
        print(f"isi ke {hitung}: {isiValue}")
        print(f"tanggal ke {hitung}: {dateValue}")
        print(f"tag ke {hitung}: {tagValue}")
        print("\n")
        hitung+=1

else:
    print(f"Failed to srapping with status code {response.status_code}")