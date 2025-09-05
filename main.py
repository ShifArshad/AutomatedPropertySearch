from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers=header)
data = response.text
soup = BeautifulSoup(data, "html.parser")

all_links = soup.select(".StyledPropertyCardDataWrapper a")
all_property_links = [link["href"] for link in all_links]
# print(f"There are {len(all_property_links)} links to individual listings in total: \n")
# print(all_property_links)

all_address = soup.select(".StyledPropertyCardDataWrapper address")
all_addresses = [address.get_text().replace(" | ", " ").strip() for address in all_address]
# print(all_addresses)

all_prices = soup.select(".PropertyCardWrapper span")
all_price = [price.get_text().replace("/mo", "").split("+")[0] for price in all_prices if "$" in price.text]
# print(f"\n After having been cleaned up, the {len(all_prices)} prices now look like this: \n")
# print(all_price)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for n in range(len(all_property_links)):

    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSci3ZbYJ8r-nl3wqGgKWujJLBLA5fZTWfXjT66U2gD-ql_org/viewform")
    time.sleep(5)

    address = driver.find_element(by=By.XPATH,
                                  value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(by=By.XPATH,
                                value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(by=By.XPATH,
                               value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(by=By.XPATH,
                                        value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    address.send_keys(all_addresses[n])
    time.sleep(1)
    price.send_keys(all_price[n])
    time.sleep(1)
    link.send_keys(all_property_links[n])
    time.sleep(1)
    submit_button.click()


