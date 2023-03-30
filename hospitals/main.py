import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from urllib.parse import unquote
import random
import json
from config import path_for_driver, url_for_page,  urls_file


headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "accept": "application/json, text/plain, text/html, */*"
}


def get_init_html(url):

    driver = webdriver.Chrome(
        executable_path=path_for_driver
    )

    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(5)

        while True:
            try:
                next_element_button = driver.find_element(By.CLASS_NAME, "button-show-more")
                if next_element_button:
                    actions = ActionChains(driver)
                    actions.click(next_element_button).perform()
                    time.sleep(3)
                    next_element_button.click()

                else:
                    print("no next_element_button")

            except:
                with open("main-page.html", "w") as file:
                    file.write(driver.page_source)
                    print("file completed")
                    break

            if driver.find_element(By.CLASS_NAME, "hasmore-text"):
                with open("main-page.html", "w") as file:
                    file.write(driver.page_source)

                break
            else:
                actions = ActionChains(driver)
                actions.move_to_element(next_element_button).perform()
                next_element_button.click()
                time.sleep(5)
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def get_urls(location):
    with open(location) as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    div_blocks = soup.find_all("div", class_="minicard-item__container")

    urls = []
    for item in div_blocks:
        item_url = item.find("h2", class_="minicard-item__title").find("a").get("href")
        urls.append(item_url)

    with open("urls.txt", "w") as file:
        for url in urls:
            file.write(f"{url}\n")

    return "Get_urls finished successfully!"


def get_info(file_path):
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]

    result_list = []
    for url in urls_list:
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        try:
            hosp_name = soup.find("span", {"itemprop": "name"}).text.strip()
        except Exception as _ex:
            hosp_name = None

        hosp_phones_list = []
        try:
            hosp_phones = soup.find("div", class_="service-phones-list").find_all("a", class_="js-phone-number")
            for phone in hosp_phones:
                hosp_phone = phone.get("href").split(":")[-1].strip()
                hosp_phones_list.append(item_phone)
        except Exception as _ex:
            hosp_phones_list = None

        try:
            hosp_address = soup.find("address", class_="iblock").text.strip()
        except Exception as _ex:
            hosp_address = None

        try:
            # hosp_site = soup.find(text=re.compile("Сайт|Официальный сайт|Компания в сети")).find("a").get("href")
            hosp_site = soup.find(class_="service-website-value").find("a").get("href")
        except Exception as _ex:
            hosp_site = None

        sn_list = []
        try:
            hosp_sn = soup.find(class_="js-service-socials ").find_all("a")
            for sn in hosp_sn:
                sn_url = sn.get("href")
                sn_url = unquote(sn_url.split("?to=")[1].split("&")[0])
                sn_list.append(sn_url)
        except Exception as _ex:
            sn_list = None

        result_list.append(
            {
                "hosp_name": hosp_name,
                "hosp_url": url,
                "hosp_phones_list": hosp_phones_list,
                "hosp_address": hosp_address,
                "hosp_site": hosp_site,
                "sn_list": sn_list
            }
        )

        time.sleep(random.randrange(2, 3))

    with open("result.json", "w") as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)
    return "Get_info finished successfully!"


def main():
    # get_init_html(url="https://spb.zoon.ru/medical/?search_query_form=1&m%5B5200e522a0f302f066000055%5D=1&center%5B%5D=59.91878264665887&center%5B%5D=30.342586983263384&zoom=10")
    # print(get_urls(location=url_for_page))
    get_info(file_path=urls_file)


if __name__ == "__main__":
    main()
