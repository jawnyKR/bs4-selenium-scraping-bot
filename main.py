import requests
import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

header = {
    "User-Agent": YOUR_COMPUTER_CONFIG,
    "Accept-Language": YOUR_COMPUTER_LANG
}

response = requests.get("https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D", headers=header)
data = response.text
soup = BeautifulSoup(data, "html.parser")

#---- LINKS ----#
all_link_elements = soup.select(".list-card-top a")

all_links = []
for link in all_link_elements:
    href = link["href"]
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)
print(all_links)

#---- ADDRESS ----#
all_address_elements = soup.select(".list-card-info address")
all_addresses = [address.get_text().split('|')[-1] for address in all_address_elements]
print(all_addresses)

#---- PRICE ----#
all_price_elements = soup.select(".list-card-heading")
all_prices = []
# print(all_price_elements[0].get_text().split('+')[0])

for element in all_price_elements:
    price = element.get_text().split('+')[0]
    if '/' in price:
        price = price.split('/')[0]
    all_prices.append(price)

print(all_prices)

print(len(all_links))
print(len(all_addresses))
print(len(all_prices))

#---- GOOGLE SPREADSHEET USING GOOGLE FORM ----#
chrome_driver_path = YOUR_CHROMEDRIVER_PATH
driver = webdriver.Chrome(executable_path=chrome_driver_path)

for n in range(len(all_links)):
    driver.get("https://forms.gle/c7fhUzfjinEx6NYc9")

    time.sleep(3)
    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()
