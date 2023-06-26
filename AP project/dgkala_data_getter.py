from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from collections import OrderedDict


browser = webdriver.Chrome('chromedriver.exe')

url = 'https://www.digikala.com/product/dkp-8366616/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%A7%D9%BE%D9%84-%D9%85%D8%AF%D9%84-iphone-13-ch-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-4-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%86%D8%A7%D8%AA-%D8%A7%DA%A9%D8%AA%DB%8C%D9%88/'
browser.get(url)

sleep(2)

# Scrolling down to the features section
browser.execute_script("window.scrollBy(0, 4000);")
sleep(2)

# Click on more button
features_btn = browser.find_element(By.XPATH, '//*[@id="specification"]/span')
features_btn.click()
sleep(3)

# Getting product features
prod_features = OrderedDict()
i = 1
while True:
    try:
        item = browser.find_element(By.XPATH, f'//*[@id="specification"]/div[2]/div/div[{i}]/p')
        try:
            value = browser.find_element(By.XPATH, f'//*[@id="specification"]/div[2]/div/div[{i}]/div/p')
        except:
            value = ''
        prod_features[item.text] = value.text
        i += 1

    except:
        print('reedi')
        break


print(prod_features)
sleep(2000)