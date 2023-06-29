from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from collections import OrderedDict
from dgkala_data_getter import get_features

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
    def __init__(self, name, price, stars, link):
        self._name:str = None
        self._current_price:int = None
        self._stars:float = None
        self._unavailable:bool = False
        self._link = None
        self._features:OrderedDict = None
        self.name = name
        self.price = price
        self.stars = stars
        self.link = link
        self.features_setter()


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
            manipulated_price = price.replace(',', '').translate(arabic_to_latin)
            self._current_price = int(manipulated_price)

    @property
    def stars(self):
        return self._stars
    
    @stars.setter
    def stars(self, stars:str):
        if stars == 0:
            pass
        else:
            manipulated_stars = stars.translate(arabic_to_latin)
            self._stars = float(manipulated_stars)
    
    @property
    def link(self):
        return self._link
    
    @link.setter
    def link(self, link):
        self._link = link

    @property
    def features(self):
        return self._features
    
    def features_setter(self):    # Gets features using previous module
        self._features = get_features(self._link)

class Main:
    def __init__(self):
        # Initiating driver
        self.browser = webdriver.Chrome('chromedriver.exe')
        # A list of product items
        self.items = []

    def get_item_data(self, i):
        cnt = 0
        while True:
            try:
                if cnt > 10:
                    break
                # Getting name
                item_name = self.browser.find_element(By.XPATH, f'//*[@id="ProductListPagesWrapper"]/section[1]/div[2]/div[{i}]/a/div/article/div[2]/div[2]/div[2]/h3')
                # Getting price
                try:
                    item_price = self.browser.find_element(By.XPATH, f'//*[@id="ProductListPagesWrapper"]/section[1]/div[2]/div[{i}]/a/div/article/div[2]/div[2]/div[4]/div[1]/div/span')
                except:
                    item_price = '0'
                # Getting stars, if there is no such tag, the stars value is set to 0
                try:
                    item_stars = self.browser.find_element(By.XPATH, f'//*[@id="ProductListPagesWrapper"]/section[1]/div[2]/div[{i}]/a/div/article/div[2]/div[2]/div[3]/div[2]/p')
                except:
                    item_stars = 0
                # Getting href attrib of product div tag
                item = self.browser.find_element(By.XPATH, f'//*[@id="ProductListPagesWrapper"]/section[1]/div[2]/div[{i}]/a')

                # Appending item to the list
                self.items.append(Product(item_name.text, item_price.text, item_stars.text, item.get_attribute('href')))
                break    # Breaking while loop if succeeded

            except:
                for j in range(5):
                    self.browser.find_element(By.TAG_NAME, "body").send_keys(Keys.DOWN)
                sleep(0.2)
                cnt += 1

    def main(self, search_word = 'آیفون 13 پرو'):
        search_word = search_word.replace(' ', '%20')
        url = 'https://www.digikala.com/search/?q=' + search_word

        self.browser.get(url)
        sleep(5)

        i = 1
        t_ls = []
        while True:
            # Loop until a problem occurs while getting data from dgkala
            try:
                t = Thread(target=lambda: self.get_item_data(i))
                t.start()
                t_ls.append(t)
                # self.get_item_data(i)

                i += 1

            except:
                break
            
            print('i: ', i)
            if i >= 10:
                break

        for thrd in t_ls:
            thrd.join()

        return self.items

if __name__ == '__main__':
    system = Main()
    print(system.main(search_word = 'آیفون 13 پرو'))