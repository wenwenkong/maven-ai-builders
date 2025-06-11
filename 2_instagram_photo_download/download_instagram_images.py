import os
import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

account = "grapeot"

def scroll_to_load_all(driver, pause_time=3, max_scrolls=50):
    last_height = driver.execute_script("return document.body.scrollHeight")
    scrolls = 0

    while scrolls < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print(f"No new content loaded after {scrolls} scrolls.")
            break

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        img_count = len(soup.find_all('img'))
        print(f"Scrolled {scrolls + 1} times → Found {img_count} <img> tags")

        last_height = new_height
        scrolls += 1

def extract_image_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('img')
    image_urls = set()
    for img in img_tags:
        if 'src' in img.attrs:
            url = img['src']
            if url.endswith(".jpg") or "cdninstagram" in url:
                image_urls.add(url)
    return list(image_urls)

def download_images(image_urls, folder=account + "_downloads"):
    os.makedirs(folder, exist_ok=True)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) "
            "Gecko/20100101 Firefox/139.0"
        ),
        "Referer": "https://www.instagram.com/"
    }
    for i, url in enumerate(image_urls, 1):
        try:
            filename = os.path.join(folder, f"image_{i:03d}.jpg")
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded {filename}")
            else:
                print(f"Failed to download {url} (status: {response.status_code})")
        except Exception as e:
            print(f"Error downloading {url}: {e}")

def main():
    username = account
    profile_url = f"https://www.instagram.com/{username}/"

    from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
    options = Options()
    options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"
    # Don't use headless yet
    # options.add_argument("--headless")

    # Replace this with your real Firefox profile
    profile_path = "/Users/wenwen/Library/Application Support/Firefox/Profiles/zcunun8s.default-1414630811518-1725749568761"
    profile = FirefoxProfile(profile_path)
    driver = webdriver.Firefox(options=options, firefox_profile=profile)


    driver = webdriver.Firefox(options=options)
    driver.get(profile_url)

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # Wait until the posts grid or user icon confirms you're logged in
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article div img"))
        )
        print("✅ Logged-in view detected, ready to scroll.")
    except:
        print("⚠️ Timeout waiting for logged-in state.")

    print("Scrolling to load all images...")
    scroll_to_load_all(driver, pause_time=3, max_scrolls=50)
    time.sleep(2)  # Allow JavaScript to finish

    print("Extracting image URLs...")
    page_source = driver.page_source
    driver.quit()

    image_urls = extract_image_urls(page_source)
    print(f"Found {len(image_urls)} image(s). Downloading...")

    download_images(image_urls)

if __name__ == "__main__":
    main()

