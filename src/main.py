from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Sesuaikan path ke chromedriver kamu
PATH = "D:/KULIAH/Computational Journalism/news-scrapping/src/chromedriver.exe"
driver = webdriver.Chrome(service=Service(PATH))

driver.maximize_window()
driver.get("https://www.kompas.com")  # Langsung ke beranda utama Kompas

# =================================================================================

# 1. Klik Search Icon
try:
    search_icon = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "header-search"))
    ).click()
    print("Search Box Berhasil Ditemukan!")
except TimeoutException:
    print("Search Box tidak ditemukan dalam 5 detik")

# =================================================================================

# 2. Cari input pencarian dan ketik keyword
try:
    search_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME,"header-search-input"))
    )

    keyword = 'tarif trump' #inisialisasi keyword
    search_input.send_keys(keyword) # Input Keyword
    search_input.send_keys(Keys.ENTER) #Tekan ENTER untuk mulai search
except:
    print("Input Element tidak ditemukan dalam 5 detik")

# =================================================================================

# 3. Proses Scrapping
articleBlocks = WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME,"articleItem"))
)

print(f"Jumlah Berita: {len(articleBlocks)}") # debugging

# Cek apakah terdapat Berita Ditemukan
if len(articleBlocks) == 0:
    print("Berita Tidak Ditemukan")

for index, article in enumerate(articleBlocks, start=0):
    try:
        articleTitle = WebDriverWait(article, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME,"articleTitle"))
        )
        print(f"{index}. {articleTitle.text}")
    except:
        print(f"{index}. Data not found!")

driver.quit()
