from threading import Thread
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from collections import OrderedDict

arabic_to_latin = str.maketrans("۰۱۲۳۴۵۶۷۸۹.", "0123456789.")

class Product:
    """
    A class representing a product on digikala website.

    Attributes:
        name (str): The name of the product.
        price (int): The current price of the product.
        stars (float): The average rating of the product, on a scale of 0-5 stars.
            If the product has not yet been rated, this attribute is set to 0.
        link (str): The URL of the product page on the website.

    Usage:
        >>> p1 = Product("آیفون 12 | iPhone 12", "۴۵,۵۰۰,۰۰۰", "۴.۵", "https://www.example.com/iphone12")
    """
    def __init__(self, name, price, img_address, link):
        self._name:str = None
        self._current_price:int = None
        # self._stars:float = None
        self._unavailable:bool = False
        self._img_address = None
        self._link = None
        # self._features:OrderedDict = None
        self.name = name
        self.price = price
        # self.stars = stars
        self.img_address = img_address
        self.link = link
        # self.features_setter()


    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def price(self):
        return self._current_price
    
    @price.setter
    def price(self, price:str):
        if price == 'ناموجود':
            self._unavailable = True
            self._current_price = 0
        else:    # Translates arabic digits to latino and removes ',' seperator
            try:
                manipulated_price = price.replace(',', '').translate(arabic_to_latin)
                self._current_price = int(manipulated_price)
            except:
                try:
                    manipulated_price = price.replace(' تومان', '').replace(',', '').translate(arabic_to_latin)
                    self._current_price = int(manipulated_price)
                except:
                    self._current_price = price

    # @property
    # def stars(self):
    #     return self._stars
    
    # @stars.setter
    # def stars(self, stars:str):
    #     if stars == 0:
    #         pass
    #     else:
    #         manipulated_stars = stars.translate(arabic_to_latin)
    #         self._stars = float(manipulated_stars)
    
    @property
    def img_address(self):
        return self._img_address
    
    @img_address.setter
    def img_address(self, img_adrs):
        if img_adrs != 'image unavailable':
            self._img_address = img_adrs

    @property
    def link(self):
        return self._link
    
    @link.setter
    def link(self, link):
        self._link = link

    # @property
    # def features(self):
    #     return self._features
    
    # def features_setter(self):    # Gets features using previous module
    #     self._features = get_features(self._link)

class Main:
    def __init__(self):
        self.browser = webdriver.Chrome('chromedriver.exe')
        self.items = []

    def get_item_data(self, i):
        try:
            item_name = self.browser.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/div[2]/div/div/div/div[{i}]/a/article/div/div[1]/h2')
            item_price = self.browser.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/div[2]/div/div/div/div[{i}]/a/article/div/div[1]/div[2]')
            item_image = self.browser.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/div[2]/div/div/div/div[{i}]/a/article/div/div[3]/div/picture/img')
            item = self.browser.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/div[2]/div/div/div/div[{i}]/a')
            self.items.append(Product(item_name.text, item_price.text, item_image.get_attribute('src'), item.get_attribute('href')))

        except:
            print(f'Failed on item {i}')

    def main(self, search_word = 'آیفون 13 پرو'):
        search_word = search_word.replace(' ', '%20')
        url = 'https://divar.ir/s/tehran/mobile-phones?goods-business-type=all&q=' + search_word

        self.browser.get(url)
        sleep(5)

        t_ls = []
        i = 1
        while True:
            if i > 20:
                break
            t = Thread(target=self.get_item_data, args=[i])
            t.start()
            t_ls.append(t)
            i += 1

        for thrd in t_ls:
            thrd.join()

        return self.items


if __name__ == '__main__':
    system = Main()
    print(system.main())
