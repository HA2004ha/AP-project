from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

arabic_to_latin = str.maketrans("۰۱۲۳۴۵۶۷۸۹.", "0123456789.")

class Product:
    """
    A class representing a product on divar website.

    Attributes:
        name (str): The name of the product.
        price (int): The current price of the product.
        link (str): The URL of the product page on the website.

    Usage:
        >>> p1 = Product("آیفون 12 | iPhone 12", "۴۵,۵۰۰,۰۰۰", "۴.۵", "https://www.example.com/iphone12")
    """
    def __init__(self, name, price, link):
        self._name:str = None
        self._current_price:int = None
        self._unavailable:bool = False
        self._link = None
        self.name = name
        self.price = price
        self.link = link

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
                    manipulated_price = price.replace('از ', '').replace(' تومان', '').replace(',', '').translate(arabic_to_latin)
                    self._current_price = int(manipulated_price)
                except:
                    self._current_price = price

    @property
    def link(self):
        return self._link
    
    @link.setter
    def link(self, link):
        self._link = link

class Main:
    def __init__(self):
        self.browser = webdriver.Chrome('chromedriver.exe')

    def main(self, search_word = 'آیفون 13 پرو'):
        url = 'https://www.zoomit.ir/product/'

        self.browser.get(url)
        sleep(5)

        search_box = self.browser.find_element(By.CSS_SELECTOR, 'body > div.internal.mainproduct:nth-child(6) > div.c-search-box:nth-child(9) > div.search-box > div.seach-box__form > div.seach-box__field > input#productsSearch.autocomplete-input.ui-autocomplete-input:nth-child(1)')
        search_box.send_keys(search_word)
        sleep(2)
        item = self.browser.find_element(By.XPATH, '/html/body/div[2]/div[5]/div/div/div/div/div/div[1]/ul')
        item.click()

        item_name = self.browser.find_element(By.CSS_SELECTOR, 'body > div.internal.mainproduct:nth-child(6) > div.container.mrg15T.mrg15B:nth-child(10) > div.c-summary-product:nth-child(2) > div.summary-product > div.summary-product__detail:nth-child(2) > div.ProductTitle.mrg30B.hidden-sm.hidden-xs:nth-child(1) > h1:nth-child(1)') 
        item_price = self.browser.find_element(By.CSS_SELECTOR, 'body > div.internal.mainproduct:nth-child(6) > div.container.mrg15T.mrg15B:nth-child(10) > div.c-summary-product:nth-child(2) > div.summary-product > div.summary-product__detail:nth-child(2) > a.summary-product--price.fa-num.hidden-xs.hidden-sm:nth-child(2) > span:nth-child(1) > span')       
        item_link = self.browser.current_url

        return Product(item_name.text, item_price.text, item_link)

if __name__ == '__main__':
    system = Main()
    print(system.main())