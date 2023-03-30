import os
import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
import csv


def get_pages():
    headers = {
        "user-agent": "Mozilla/5.0(X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }

    r = requests.get(url="https://shop.casio.ru/catalog/", headers=headers, verify=False)

    if not os.path.exists("pages"):
        os.mkdir("pages")

    with open("pages/page_1.html", "w") as file:
        file.write(r.text)

    with open("pages/page_1.html") as file:
        src = file.read()

    soup_obj = BeautifulSoup(src, "lxml")
    pages_count = int(soup_obj.find("div", class_="bx-pagination-container").find_all("a")[-2].text)

    for i in range(1, pages_count + 1):
        url = f"https://shop.casio.ru/catalog/?PAGEN_1={i}"
        # print(url)

        r = requests.get(url=url, headers=headers, verify=False)

        with open(f"pages/page_{i}.html", "w") as file:
            file.write(r.text)

        time.sleep(2)

    return pages_count + 1


def scrap_info(total_page_num):
    cur_date = datetime.now().strftime("%d_%m_%Y")

    with open(f"info_{cur_date}.csv", "w") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Артикул",
                "Ссылка"
            )
        )

    data = []
    for page in range(1, total_page_num):
        with open(f"pages/page_{page}.html") as file:
            src = file.read()

        soup_obj = BeautifulSoup(src, "lxml")
        item_cards = soup_obj.find_all("a", class_="product-item__link")

        for item in item_cards:
            product_article = item.find("p", class_="product-item__articul").text.strip()
            # product_price = item.find("p", class_="product-item__price").text
            product_url = f'https://shop.casio.ru/{item.get("href")}'

            data.append(
                {
                    "product_article": product_article,
                    "product_url": product_url
                }
            )

            with open(f"info_{cur_date}.csv", "a") as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        product_article,
                        product_url
                    )
                )

    with open(f"info_{cur_date}.json", "a") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    page_num = get_pages()
    scrap_info(total_page_num=page_num)


if __name__ == '__main__':
    main()
