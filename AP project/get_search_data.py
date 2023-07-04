from threading import Thread
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from collections import OrderedDict
from dgkala_data_getter import get_features
from divar_search import Main as DIVARMAIN
from torob_search import Main as TOROBMAIN
# from zoomit_search import Main as ZOOMITMAIN

arabic_to_latin = str.maketrans("۰۱۲۳۴۵۶۷۸۹.", "0123456789.")
illegal_chars = str.maketrans("#<>$+%!*`&'|{}?=:/\@", "--------------------")

class SimilarProduct:
    def __init__(self, name):
        self._name = None
  
        self._divar_name = None
        self._divar_price = None
        self._divar_link = None

        self._torob_name = None
        self._torob_price = None
        self._torob_link = None

        self._zoomit_name = None
        self._zoomit_price = None
        self._zoomit_link = None
        
        self.setter(name)

    @property
    def divar_name(self):
        return self._divar_name
    
    @property
    def divar_price(self):
        return self._divar_price
    
    @property
    def divar_link(self):
        return self._divar_link
    
    @property
    def torob_name(self):
        return self._torob_name
    
    @property
    def torob_price(self):
        return self._torob_price
    
    @property
    def torob_link(self):
        return self._torob_link
    
    @property
    def zoomit_name(self):
        return self._zoomit_name
    
    @property
    def zoomit_price(self):
        return self._zoomit_price
    
    @property
    def zoomit_link(self):
        return self._zoomit_link

    def setter(self, name):
        try:
            def f0(self):
                try:
                    # Get similar products from DIVAR
                    divar_obj = DIVARMAIN()
                    divar_product = divar_obj.main(name)
                    self._divar_name = divar_product.name
                    self._divar_price = divar_product.price
                    self._divar_link = divar_product.link
                except:
                    pass    # PASS, if there is no similar product in DIVAR
        
            def f1(self):
                try:
                    # Get similar products from TOROB
                    torob_obj = TOROBMAIN()
                    torob_product = torob_obj.main(name)
                    self._torob_name = torob_product.name
                    self._torob_price = torob_product.price
                    self._torob_link = torob_product.link
                except:
                    pass    # PASS, if there is no similar product in TOROB

            # def f2(self):
            #     try:
            #         # Get similar products from TOROB
            #         zoomit_obj = ZOOMITMAIN()
            #         zoomit_product = zoomit_obj.main(name)
            #         self._zoomit_name = zoomit_product.name
            #         self._zoomit_price = zoomit_product.price
            #         self._zoomit_link = zoomit_product.link
            #     except:
            #         pass    # PASS, if there is no similar product in DIVAR
            
            t0 = Thread(target=lambda:f0(self))
            t0.start()
            t1 = Thread(target=lambda:f1(self))
            t1.start()
            # t2 = Thread(target=lambda:f2(self))
            # t2.start()
            t0.join()
            t1.join()
            # t2.join()

        except Exception as excp:
            print(f'ITEM {name} FAILED BECAUSE OF {excp}')

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
    def __init__(self, name, link):
        self._name:str = None
        self._current_price:int = None
        self._unavailable:bool = False
        self._img_address = None
        self._img_dir = None
        self._link = None
        self._features:OrderedDict = None
        self._similar_product:SimilarProduct = None
        self.name = name
        self.link = link
        self.features_setter()
        self.price_setter()
        self.img_address_setter()
        self.similar_product_setter()

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

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
        self._features = get_features(self.name, self._link)

    @property
    def price(self):
        return self._current_price
    
    def price_setter(self):
        if type(self._features['price']) == str:
            price = self._features['price']
        else:
            price = self._features['price'].text

        if price == 'ناموجود':
            self._unavailable = True
            self._current_price = 0
        else:    # Translates arabic digits to latino and removes ',' seperator
            manipulated_price = price.replace(',', '').translate(arabic_to_latin)
            self._current_price = int(manipulated_price)

    @property
    def img_address(self):
        return self._img_address
    
    def img_address_setter(self):
        if self._features['img_adrs'] != 'image unavailable':
            self._img_address = self._features['img_adrs']    
            self._img_dir = f'images\\item {self.name}.jpg'

    @property
    def img_dir(self):
        return self._img_dir

    @property
    def similar_product(self):
        return self._similar_product

    def similar_product_setter(self):
        try:
            self._similar_product = SimilarProduct(self.name)
        except Exception as excp:
            print(f'[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]\n[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]\n[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]\n{excp}\n[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]\n[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]\n[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]\n')

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
                if cnt >= 2:    # Breaking loop, if it took too much time
                    break
                
                # Getting name
                item_name = self.browser.find_element(By.XPATH, f'//*[@id="ProductListPagesWrapper"]/section[1]/div[2]/div[{i}]/a/div/article/div[2]/div[2]/div[2]/h3')

                # Getting href attrib of product div tag
                item = self.browser.find_element(By.XPATH, f'//*[@id="ProductListPagesWrapper"]/section[1]/div[2]/div[{i}]/a')

                # Appending item to the list
                self.items.append(Product(item_name.text, item.get_attribute('href')))
    
                break    # Breaking while loop if succeeded

            except Exception as excp:
                for j in range(5):
                    self.browser.find_element(By.TAG_NAME, "body").send_keys(Keys.DOWN)
                sleep(0.2)
                cnt += 1

    def main(self, search_word = 'آیفون 13 پرو'):
        search_word = search_word.replace(' ', '%20')
        url = 'https://www.digikala.com/search/' + search_word

        self.browser.get(url)
        sleep(5)

        number_of_items = 1
        i = 1
        t_ls = []
        while True:
            # Loop until a problem occurs while getting data from dgkala
            try:
                t = Thread(target=self.get_item_data, args=[i])
                t.start()
                t_ls.append(t)

                i += 1

            except:
                print(f'Failed on item: {i}')
                number_of_items += 1
                break
            
            print('i: ', i)
            if i > number_of_items:
                break

        for thrd in t_ls:
            thrd.join()

        self.browser.close()

        return self.items

if __name__ == '__main__':
    system = Main()
    obj:Product = system.main(search_word = 'category-mobile-phone/product-list')[0]
    print(obj.name)
    print(obj.price)
    print(obj.features)
    print(obj.link)
    print(obj.img_address)
    print(obj.img_dir)
    similar_obj:SimilarProduct = obj.similar_product
    print(similar_obj.divar_name)
    print(similar_obj.divar_price)
    print(similar_obj.divar_link)

    print(similar_obj.torob_name)
    print(similar_obj.torob_price)
    print(similar_obj.torob_link)

    print(similar_obj.zoomit_name)
    print(similar_obj.zoomit_price)
    print(similar_obj.zoomit_link)