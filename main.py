from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import requests
import pandas as pd
import csv


s = Service(r"D:\Kinjal\chromedriver_win32\chromedriver.exe")

def get_free_proxies():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--headless")
    # create a webdriver instance
    driver = webdriver.Chrome(service=s, options=options)
    driver.maximize_window()
    driver.get("https://free-proxy-list.net/")
    # get the table rows
    rows = driver.find_elements(By.CSS_SELECTOR,"table.table-striped tbody tr")
    # print(rows)
    # to store proxies
    proxies = []
    for row in rows[1:]:
        tds = row.find_elements(By.CSS_SELECTOR,"td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            proxies.append(str(ip) + ":" + str(port))
            print(proxies)
            df = pd.DataFrame(proxies)
            df.columns = ['IP Address']
            df.to_csv('proxylist.csv')
        except IndexError:
            continue
    driver.quit()
    return proxies

def check_proxy_availability(proxy):
    try:
        response = requests.get("http://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200 and response.json()["origin"] == proxy.split(":")[0]:
            return True
    except:
        pass
    return False

def save_available_proxies(proxies):
    available_proxies = []
    for proxy in proxies:
        if check_proxy_availability(proxy):
            available_proxies.append(proxy)
            print(available_proxies)
            df = pd.DataFrame(available_proxies)
            df.columns = ['IP Address']
            df.to_csv('available_proxies.csv')
            

    # # Save available proxies to CSV
    # with open('available_proxies.csv', 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['IP Address'])
    #     writer.writerows([[proxy] for proxy in available_proxies])

    # # Save available proxies to text file
    with open('available_proxies.txt', 'w') as txtfile:
        txtfile.write('\n'.join(available_proxies))

# ...

# Call the function to get proxies
proxies = get_free_proxies()

# Check proxy availability and save the results
save_available_proxies(proxies)