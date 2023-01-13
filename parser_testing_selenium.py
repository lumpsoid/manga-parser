from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_experimental_option("prefs", {
# "download.prompt_for_download": False,
# "download.directory_upgrade": True,
# "profile.default_content_settings.popups": 0,
# "profile.managed_default_content_settings.javascript": 2
# })
browser = webdriver.Chrome(chrome_options=chrome_options)

browser.get('http')
chapters = browser.find_elements(By.CLASS_NAME, "wp-manga-chapter")
for chapter in chapters:
    print(chapter.find_element(By.TAG_NAME, "a").get_attribute("href"))

for chapter in chapters:
    browser.get(chapter)
    for image in browser.find_elements(By.CLASS_NAME, "wp-manga-chapter-img"):
        image.get_attribute('data-src')

browser.close()