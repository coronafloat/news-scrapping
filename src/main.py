from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

PATH = "D:/KULIAH/Computational Journalism/news-scrapping/src/chromedriver.exe"
driver = webdriver.Chrome(service=Service(PATH))

try:
    driver.maximize_window()
    driver.get("https://www.kompas.com")
    print("Halaman Kompas.com telah dibuka")

    # Klik Search Icon
    try:
        search_icon = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "header-search"))
        )
        search_icon.click()
        print("Search Box Berhasil Ditemukan!")
    except TimeoutException:
        print("Search Box tidak ditemukan dalam 5 detik")
        driver.quit()
        exit()

    # Input keyword dan enter
    try:
        search_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "header-search-input"))
        )
        keyword = 'tarif trump'
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.ENTER)
        print(f"Mencari berita dengan keyword: '{keyword}'")
        time.sleep(3)
    except TimeoutException:
        print("Input Element tidak ditemukan dalam 5 detik")
        driver.quit()
        exit()

    # Proses Scraping
    try:
        articleBlocks = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "articleItem"))
        )
        print(f"Jumlah Berita: {len(articleBlocks)}")

        if not articleBlocks:
            print("Berita Tidak Ditemukan")
            driver.quit()
            exit()

        search_result_url = driver.current_url

        for index, article in enumerate(articleBlocks, start=1):
            print(f"\n======= ARTIKEL {index} =======")
            try:
                articleTitle = WebDriverWait(article, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "articleTitle"))
                )
                print(f"Judul Artikel: {articleTitle.text}")

                try:
                    articleTag = WebDriverWait(article, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "articlePost-subtitle"))
                    )
                    print(f"Tag Artikel: {articleTag.text}")
                except TimeoutException:
                    print("Tidak menemukan Tag Artikel!")
                    continue

                try:
                    article_link = article.find_element(By.TAG_NAME, "a").get_attribute("href")
                    print(f"URL Artikel: {article_link}")
                except NoSuchElementException:
                    print("URL Artikel tidak ditemukan!")
                    continue

                driver.execute_script(f"window.open('{article_link}');")
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(3)

                try:
                    show_all_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".paging__link.paging__link--show"))
                    )
                    
                    # Scroll ke elemen terlebih dahulu
                    driver.execute_script("arguments[0].scrollIntoView(true);", show_all_button)
                    time.sleep(0.5)  # opsional: beri waktu animasi scroll
                    show_all_button.click()
                    print("Tombol 'Show All' ditemukan dan diklik")
                    time.sleep(2)
                except (TimeoutException, Exception):
                    print("Tidak ada tombol 'Show All'")


                try:
                    article_content = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".read__content"))
                    )
                    paragraphs = article_content.find_elements(By.TAG_NAME, "p")

                    # print(f"Jumlah paragraf: {len(paragraphs)}") #debugging
                    print("\nKONTEN ARTIKEL:")
                    for i, p in enumerate(paragraphs, 1):
                        if p.text.strip():
                            print(f"[P{i}] {p.text}")
                except TimeoutException:
                    print("Konten artikel tidak ditemukan")

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)

            except Exception as e:
                print(f"Error pada artikel {index}: {str(e)}")
                if len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                if driver.current_url != search_result_url:
                    driver.get(search_result_url)
                    time.sleep(2)
                    articleBlocks = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "articleItem"))
                    )

    except TimeoutException as e:
        print(f"Gagal mengambil daftar artikel: {str(e)}")

except Exception as e:
    print(f"Terjadi kesalahan: {str(e)}")

finally:
    print("\nSelesai scraping, menutup browser...")
    driver.quit()
