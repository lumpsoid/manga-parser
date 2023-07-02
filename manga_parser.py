#!/home/qq/Applications/miniconda3/bin/python
import re
import os
from bs4 import BeautifulSoup
import requests
import pickle


def five_numbers_test(num):
    num = str(num)
    match_num = re.findall(r'[0-9]+', num)
    num_len = len(match_num[0])
    if num_len == 5:
        return num
    elif num_len > 5:
        raise ValueError(f"Value len is more than five ({num_len})")
    if len(match_num) > 1:
        return ((5 - num_len) * "0") + match_num[0] + "(" + match_num[1] + ")"
    return ((5 - num_len) * "0") + match_num[0]


def download_images_from_dict(manga_dict, directory_to_download, manga_name, chapter_limit=None):
    print('Starting image downloading...')
    chapter_number_com = re.compile(r'/chapter-(.+)/')
    # file_number_com = re.compile(r'/([^/]+)\.[a-z]+$')
    file_extension_com = re.compile(r'/[^/]+\.([a-z]+)$')
    chapters_downloaded = 0
    for chapter, image_list in reversed(manga_dict.items()):
        if chapter_limit and chapters_downloaded >= chapter_limit:
            break

        num_chapter = chapter_number_com.search(chapter).group(1)
        num_chapter = five_numbers_test(num_chapter)
        chapter_path = f'{directory_to_download}/{manga_name}/{num_chapter}'
        if not os.path.exists(chapter_path):
            os.makedirs(chapter_path)
            print(f'downloading chapter №{num_chapter}')
        for index, image in enumerate(image_list):
            file_num = five_numbers_test(index)
            file_extension = file_extension_com.search(image).group(1)
            image_path = f'{chapter_path}/{file_num}.{file_extension}'
            if not os.path.exists(image_path):
                r = requests.get(image)
                print('proccessing:', image)
                with open(image_path, 'wb') as f:
                    f.write(r.content)
        chapters_downloaded += 1
    return print("Download complited")


def manga_download_sel(manga_http, manga_name, directory_to_download, dict_download_path, flag_images=0):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.javascript": 2
    })
    browser = webdriver.Chrome(chrome_options=chrome_options)

    browser.get(manga_http)
    chapters = browser.find_elements(By.CLASS_NAME, "wp-manga-chapter")
    manga_dict = {}
    for chapter in chapters:
        manga_dict.update({chapter.find_element(
            By.TAG_NAME, "a").get_attribute("href"): []})
    tab_sub = re.compile(r'^[\t\n]+')
    for chapter, _ in reversed(manga_dict.items()):
        browser.get(chapter)
        manga_img_chapter = browser.find_elements(
            By.CLASS_NAME, "wp-manga-chapter-img")
        for image in manga_img_chapter:
            manga_dict.get(chapter).append(
                tab_sub.sub('', image.get_attribute('data-src')))

    browser.close()
    print('Dict is filled')
    with open(f'{dict_download_path}/{manga_name}.pickle', 'wb') as handle:
        pickle.dump(manga_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    if flag_images:
        download_images_from_dict(
            manga_dict, directory_to_download, manga_name)
    return print('Script is done')


def manga_download_bs(manga_http, directory_to_download, dict_download_path, flag_images=0, chapter_limit=None):
    manga_name = re.search(r'([^/]+)[\/]?$', manga_http).group(1)
    # Send a request to the website
    response = requests.get(manga_http)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'lxml')

    # Find all the chapters on the page
    chapters = soup.find_all('li', class_='wp-manga-chapter')
    print('got chapters')

    # Create a dictionary to store the chapters and their corresponding image lists
    manga_dict = {}
    for chapter in chapters:
        chapter_link = chapter.find('a').get('href')
        manga_dict[chapter_link] = []

    # Iterate through the chapters and scrape the images
    tab_sub = re.compile(r'^[\t\n]+')
    for chapter, _ in reversed(manga_dict.items()):
        chapter_number_com = re.compile(r'/chapter-(.+)/')
        # Send a request to the chapter URL
        response = requests.get(chapter)
        print(f'parsign chapter№{chapter_number_com.search(chapter).group(1)}')
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the images on the page
        images = soup.find_all('img', class_='wp-manga-chapter-img')

        # Add the images to the dictionary
        for image in images:
            manga_dict[chapter].append(tab_sub.sub('', image.get('data-src')))

    # Download the images using the download_images_from_dict function
    if flag_images:
        download_images_from_dict(
            manga_dict, directory_to_download, manga_name, chapter_limit)

    # Save the dictionary to a pickle file
    with open(f'{dict_download_path}/{manga_name}.pickle', 'wb') as handle:
        pickle.dump(manga_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return print('Script is done')


def from_dict_to_images(manga_name, directory_to_download, dict_download_path, chapter_limit):
    with open(f'{dict_download_path}/{manga_name}.pickle', 'rb') as handle:
        manga_dict = pickle.load(handle)

    download_images_from_dict(
        manga_dict, directory_to_download, manga_name, chapter_limit)
    return print('Script is done')


if __name__ == "__main__":
    manga_download_bs(
        manga_http="https://mangaclash.com/manga/skeleton-soldier-skeleton-soldier-couldnt-protect-the-dungeon",
        directory_to_download="/home/qq/Downloads/manga",
        dict_download_path="/home/qq/Downloads/manga/manga_dict",
        flag_images=1,
        chapter_limit=None
    )

    # from_dict_to_images(
    #     manga_name='skeleton-soldier-skeleton-soldier-couldnt-protect-the-dungeon',
    #     directory_to_download="/home/qq/Downloads/manga",
    #     dict_download_path="/home/qq/Downloads/manga/manga_dict",
    #     chapter_limit=None
    # )

# "https://mangaclash.com/manga/skeleton-soldier-couldnt-protect-the-dungeon/",
