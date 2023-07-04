from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from time import sleep
from collections import OrderedDict
import requests
import random

def get_features(name, url = 'https://www.digikala.com/product/dkp-8366616/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%A7%D9%BE%D9%84-%D9%85%D8%AF%D9%84-iphone-13-ch-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-4-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%86%D8%A7%D8%AA-%D8%A7%DA%A9%D8%AA%DB%8C%D9%88/'):
    browser = webdriver.Chrome('chromedriver.exe')

    browser.get(url)

    sleep(2)

    actions = ActionChains(browser)

    scroller = 0
    while True:
        # Scrolling down to the features section, using keys
        actions.key_down(Keys.DOWN).perform()
        sleep(0.5)
        actions.key_up(Keys.DOWN).perform()
        sleep(0.1)

        try:
            # Click on more button
            features_btn = browser.find_element(By.XPATH, '//*[@id="specification"]/span')
            features_btn.click()
            sleep(3)
            break
        except:
            if scroller >= 15:
                break
        scroller += 1

    # Getting product features
    prod_features = OrderedDict()
    i = 1
    while True:
        try:
            item = browser.find_element(By.XPATH, f'//*[@id="specification"]/div[2]/div/div[{i}]/p')
            try:
                value = browser.find_element(By.XPATH, f'//*[@id="specification"]/div[2]/div/div[{i}]/div/p')
                prod_features[item.text] = value.text
            except:
                value = ''
                prod_features[item.text] = value

            i += 1

        except:
            break

    # Adding price to features
    try:
        prod_features['price'] = browser.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div[4]/div[1]/div[8]/div/div/div[1]/div[2]/div[1]/span').text
    except Exception as excp:
        print(f'\033[91m{excp}')
        prod_features['price'] = 'ناموجود'

    # Downloading image and add its address to product features
    try:
        prod_features['img_adrs'] = browser.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/img').get_attribute('src')
        try:
            img_bytes = requests.get(prod_features['img_adrs']).content
            try:
                img_file = open(f'images\\{browser.title}.jpg', "wb")
            except:
                img_file = open(f'images\\item {name}.jpg', "wb")
            img_file.write(img_bytes)
            img_file.close()
        except Exception as excp:
            pass
    except:
        prod_features['img_adrs'] = 'image unavailable'

    browser.close()

    return prod_features


if __name__ == '__main__':
    print(get_features('آیفون 13', url = 'https://www.digikala.com/product/dkp-8366616/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%A7%D9%BE%D9%84-%D9%85%D8%AF%D9%84-iphone-13-ch-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-4-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%86%D8%A7%D8%AA-%D8%A7%DA%A9%D8%AA%DB%8C%D9%88/')['price'])