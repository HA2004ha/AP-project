from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from googletrans import Translator
import Levenshtein

arabic_to_latin = str.maketrans("۰۱۲۳۴۵۶۷۸۹.", "0123456789.")
persian_transliterate = str.maketrans("ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی", "abptsjchkdzrzjsssztzaqfqkglmnvhy")

def search_system(items_name_list, search_word):
    """
    This function converts your search word to multiple forms and finds the closest matches.
    """
    transliterated_search_word = search_word.translate(persian_transliterate)
    t = Translator()
    translated_to_en_word = t.translate(search_word, src='fa', dest='en').text
    translated_to_fa_word = t.translate(search_word, src='en', dest='fa').text
    
    result_dic = {}

    min_original = min(items_name_list, key=lambda wrd: Levenshtein.distance(wrd, search_word))
    result_dic[Levenshtein.distance(min_original, search_word)] = min_original

    min_transliterated = min(items_name_list, key=lambda wrd: Levenshtein.distance(wrd, transliterated_search_word))
    result_dic[Levenshtein.distance(min_transliterated, transliterated_search_word)] = min_transliterated
        
    min_translated_to_en = min(items_name_list, key=lambda wrd: Levenshtein.distance(wrd, translated_to_en_word))
    result_dic[Levenshtein.distance(min_translated_to_en, translated_to_en_word)] = min_transliterated

    min_translated_to_fa = min(items_name_list, key=lambda wrd: Levenshtein.distance(wrd, translated_to_fa_word))
    result_dic[Levenshtein.distance(min_translated_to_fa, translated_to_fa_word)] = min_transliterated        

    return (result_dic[min(result_dic)])

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
                    manipulated_price = price.replace(' تومان', '').replace(',', '').translate(arabic_to_latin)
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
        self.items = {}

    def get_item_data(self, i):
        try:
            item_name = self.browser.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/div[2]/div/div/div/div[{i}]/a/article/div/div[1]/h2')
            item_price = self.browser.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/div[2]/div/div/div/div[{i}]/a/article/div/div[1]/div[2]')
            item = self.browser.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/div[2]/div/div/div/div[{i}]/a')
            self.items[item_name.text] = Product(item_name.text, item_price.text, item.get_attribute('href'))

        except Exception as expt:
            print(f'Failed on item {i}, because of {expt}')

    def main(self, search_word = 'آیفون 13 پرو'):
        try:
            manipulated_search_word = (' '.join(search_word.split()[:4])).replace(' ', '%20')
        except:
            try:
                manipulated_search_word = (' '.join(search_word.split()[:3])).replace(' ', '%20')
            except:
                try:
                    manipulated_search_word = (' '.join(search_word.split()[:2])).replace(' ', '%20')
                except:
                    manipulated_search_word = search_word.replace(' ', '%20')

        url = 'https://divar.ir/s/tehran/mobile-phones?goods-business-type=all&q=' + manipulated_search_word

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

        self.browser.close()

        return self.items[search_system(self.items.keys(), search_word)]


if __name__ == '__main__':
    system = Main()
    obj:Product = (system.main())
    print(obj.name)
    print(obj.price)
    print(obj.link)