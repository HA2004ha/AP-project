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
        sleep(2)
        prod_features['price'] = browser.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div[4]/div[1]/div[8]/div/div/div[1]/div[2]/div[1]/span').text
    except Exception as excp:
        try:
            prod_features['price'] = browser.find_element(By.CSS_SELECTOR, 'body > div#__next:nth-child(2) > div.h-100.d-flex.flex-column.bg-000.ai-center:nth-child(2) > div.grow-1.bg-000.d-flex.flex-column.w-100.ai-center.shrink-0:nth-child(3) > div.grow-1.bg-000.d-flex.flex-column.w-100.ai-center.styles_BaseLayoutDesktop__content__hfHD1.container-4xl-w:nth-child(3) > div.px-5-lg:nth-child(2) > div.d-flex.flex-column.flex-row-lg.styles_PdpProductContent__sectionBorder--mobile__J7liJ:nth-child(2) > div.grow-1.w-min-0:nth-child(2) > div.styles_InfoSection__leftSection__0vNpX:nth-child(2) > div.d-flex.flex-column.mr-3-lg.mb-3-lg.gap-y-2-lg.styles_InfoSection__buyBoxContainer__3nOwP:nth-child(4) > div.styles_Marketable__3IHFu.radius-medium-lg.border-200-lg.bg-000.styles_InfoSection__buybox__tknJ3:nth-child(1) > div.pos-relative.w-full.w-auto-lg.px-4-lg.pb-4-lg:nth-child(8) > div.w-full.w-auto-lg.z-3.bg-000.shadow-fab-button.shadow-none-lg.styles_BuyBoxFooter__actionWrapper__Hl4e7 > div > div.d-flex.ai-center:nth-child(1) > div.d-flex.jc-start.mr-auto.text-h3 > div.d-flex.ai-center.jc-end.w-100:nth-child(1) > span.text-h4.ml-1.color-800').text
        except:
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