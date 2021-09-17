from urllib.request import urlopen as urlRequest
from bs4 import BeautifulSoup as soup
import csv

newegg_url = "https://www.newegg.com/p/pl?d=graphics+card"

# opening up connection, grabbing the page
print("opening up connection, grabbing the page")
urlClient = urlRequest(newegg_url)
page_html = urlClient.read()
urlClient.close()

# html parsing
print("parsing html")
page_soup = soup(page_html, "html.parser")

# grabs all products that match
containers = page_soup.find_all("div", {"class": "item-container"})

final_results = []  # used to hold products with complete information

for container in containers:
    image_url = container.find("a", {"class": "item-img"}).img["src"]
    item_info = container.find("div", {"class": "item-info"})

    brand_container = item_info.find("a", {"class": "item-brand"})
    if not brand_container:
        continue

    brand = brand_container.img["title"]
    title = item_info.find("a", {"class": "item-title"}).text

    item_action = container.find("div", {"class": "item-action"})
    if not item_action:
        continue

    price_info_container = item_action.find("ul", {"class": "price"})
    if not price_info_container:
        continue

    price_info = price_info_container.find(
        "li", {"class": "price-current"})
    if not price_info:
        continue

    price = str(price_info.text)
    index_of_decimal = price.find(".")
    if index_of_decimal == -1:
        continue

    price = price[:index_of_decimal+3]
    print(price)

    final_results.append(
        {"title": title, "brand": brand, "price": price, "image_url": image_url})


# add data to csv
print("adding data to csv")
filename = "scraped_products.csv"
fileWriter = csv.writer(open(filename, "w", newline=""))
headers = ["image_url", "title", "brand", "price"]
fileWriter.writerow(headers)

for res in final_results:
    fileWriter.writerow([res["image_url"], res["title"],
                        res["price"], res["brand"]])
# fileWriter.close()

print("total eligible items added = " + str(len(final_results)))
