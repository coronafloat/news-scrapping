from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# PATH disesuaikan dengan lokasi project, misal: your-path/news-scrapping/src/chromedriver.exe
PATH = "D:/KULIAH/Computational Journalism/news-scrapping/src/chromedriver.exe"
driver = webdriver.Chrome(service=Service(PATH))

driver.get("https://search.kompas.com/search?q=tarif+trump&type=article")

print(f"Judul Web: {driver.title}")

# Get blok bagian artikel dari browser dengan tag HTML articleItem
articleBlocks = driver.find_elements(By.CLASS_NAME,"articleItem")

print(f"Jumlah Berita: {len(articleBlocks)}")

if len(articleBlocks) == 0:
    print("Berita Tidak Ditemukan")

for index, article in enumerate(articleBlocks,start=1):
    try:
        # Get judul article dari browser dengan tag HTML articleItem
        articleTitle = article.find_element(By.CLASS_NAME,"articleTitle")
        print(f"{index}. {articleTitle.text}")
    except:
        print(f"{index}. Data not found!")

driver.quit()