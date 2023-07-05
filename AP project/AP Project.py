import sys
import json
import time
import math
from PIL import Image
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import webbrowser
from get_search_data import *
import shelve
from threading import Thread

def encode_dict(dictionary):
    encoded_dict = {}
    for key, value in dictionary.items():
        encoded_key = ""
        for char in key:
            encoded_key += chr(ord(char) + 1)
        encoded_value = ""
        for char in value:
            encoded_value += chr(ord(char) + 1)
        encoded_dict[encoded_key] = encoded_value
    return encoded_dict


def decode_dict(encoded_dictionary):
    decoded_dict = {}
    for key, value in encoded_dictionary.items():
        decoded_key = ""
        for char in key:
            decoded_key += chr(ord(char) - 1)
        decoded_value = ""
        for char in value:
            decoded_value += chr(ord(char) - 1)
        decoded_dict[decoded_key] = decoded_value
    return decoded_dict

def break_str(string):
    new_string = ""
    j=0
    for i in range(len(string)):
        if string[i]==" ":
            j+=1
        if string[i] == " " and  i != len(string)-1 and j%3==0:
            
            new_string += "\n"
        else:
            new_string += string[i]
    return new_string

class RegistrationForm(QWidget):
    def __init__(self,mobile_lst,headset_lst,tv_lst,tablet_lst,laptop_lst):
        super().__init__()
          
        #set titele and size window
        self.setWindowTitle('Mini Torob')
        self.setFixedSize(1000, 800)

        #List of products
        self.mobile_lst=mobile_lst
        self.headset_lst=headset_lst
        self.tv_lst=tv_lst
        self.tablet_lst=tablet_lst
        self.laptop_lst=laptop_lst
        self.all_lst=self.mobile_lst+self.headset_lst+self.tv_lst+self.tablet_lst+self.laptop_lst
        self.favorites_list=[]

        #set backgroung
        self.pixmap = QPixmap("images\\home.jpg")
        self.label=QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.resize(1000,800)

        #object for sign in gui
        self.username_label_sign_in = QLabel('Username:', self)
        self.username_field_sign_in = QLineEdit(self)
        self.username_field_sign_in.setPlaceholderText("Username")
        self.password_label_sign_in = QLabel('Password:', self)
        self.password_field_sign_in = QLineEdit(self)
        self.password_field_sign_in.setPlaceholderText("Password")
        self.sign_in_button1 = QPushButton('Sign in', self)
        self.sign_up_button1 = QPushButton('Sign up', self)
        self.error_sign_in=QLabel("",self)

        #object for sign up gui
        self.username_label_sign_up = QLabel('Username :', self)
        self.username_field_sign_up = QLineEdit(self)
        self.username_field_sign_up.setPlaceholderText("Username")
        self.password_label_sign_up = QLabel('Password:', self)
        self.password_field_sign_up = QLineEdit(self)
        self.password_field_sign_up.setPlaceholderText("Password")
        self.repeat_password_label_sign_up = QLabel('Repeat Password:', self)
        self.repeat_password_field_sign_up = QLineEdit(self)
        self.repeat_password_field_sign_up.setPlaceholderText("Repeat Password")
        self.sign_in_button2 = QPushButton('Sign in', self)
        self.sign_up_button2 = QPushButton('Sign up', self)
        self.error_sign_up=QLabel("",self) 

        #object for home gui
        self.search_field=QLineEdit(self)
        self.search_field.setPlaceholderText("Search Here")
        self.search=QPushButton('Search',self)
        self.search.setStyleSheet("background-color: qradialgradient(cx:0.5, cy:0.5,"
                                "fx:0.5,fy:0.5,radius:0.6,"
                                "stop:0 white, stop:1 #c0c0c0);"
                                "border-style: outset;"
                                "border-width: 3px;"
                                "border-radius: 10px;"
                                "border-color: gray;"
                                "padding: 6px;"
                                "color:black;"
                                "font-size:15px;")
        self.search.clicked.connect(lambda x :self.searching(self.search_field.text()))
        self.log_out=QPushButton("Log Out",self)
        self.log_out.setStyleSheet("background-color: qradialgradient(cx:0.5, cy:0.5,"
                                "fx:0.5,fy:0.5,radius:0.6,"
                                "stop:0 white, stop:1 #d30102);"
                                "border-style: outset;"
                                "border-width: 3px;"
                                "border-radius: 10px;"
                                "border-color: gray;"
                                "padding: 6px;"
                                "color:black;"
                                "font-size:15px;")
        self.all_product_btn = QPushButton("All Products",self)
        self.mobiles_btn = QPushButton("Mobile",self)
        self.tablets_btn = QPushButton("Tablet",self)
        self.tves_btn = QPushButton("TV",self)
        self.laptops_btn = QPushButton("Laptop",self)
        self.headset_btn = QPushButton("Headset",self)
        self.favorites_btn = QPushButton("Favorites",self)

        #object for page gui
        self.name_products = QLabel('', self)
        self.grid = QGridLayout()
        self.home=QPushButton("Home",self)
        self.home.setStyleSheet("background-color: qradialgradient(cx:0.5, cy:0.5,"
                                "fx:0.5,fy:0.5,radius:0.6,"
                                "stop:0 white, stop:1 #d30102);"
                                "border-style: outset;"
                                "border-width: 3px;"
                                "border-radius: 10px;"
                                "border-color: gray;"
                                "padding: 6px;"
                                "color:black;"
                                "font-size:15px;")
        self.widget = QWidget()
        self.scroll_area = QScrollArea()
        self.main_layout = QVBoxLayout()

        #object for page product gui
        self.dlg = QDialog(self)
        self.dlg.setWindowTitle("Comparing")
        self.layout1 = QVBoxLayout()
        self.label_show_message = QLabel("",self)
        self.label_show_message.setStyleSheet("font-size: 20px")
        self.timer = QTimer(self)
        self.back=QPushButton("Back",self)
        self.back.setStyleSheet("background-color: qradialgradient(cx:0.5, cy:0.5,"
                                "fx:0.5,fy:0.5,radius:0.6,"
                                "stop:0 white, stop:1 #d30102);"
                                "border-style: outset;"
                                "border-width: 3px;"
                                "border-radius: 10px;"
                                "border-color: gray;"
                                "padding: 6px;"
                                "color:black;"
                                "font-size:15px;")
        self.label_picture=QLabel(self)
        self.table = QTableWidget(self)
        self.digikala=QPushButton(self)
        self.digikala.setStyleSheet("background-color: qradialgradient(cx:0.5, cy:0.5,"
                                    "fx:0.5,fy:0.5,radius:0.6,"
                                    "stop:0 white, stop:1 #c0c0c0);"
                                    "border-style: outset;"
                                    "border-width: 3px;"
                                    "border-radius: 10px;"
                                    "border-color: gray;"
                                    "padding: 6px;"
                                    "color:black;"
                                    "font-size:15px;")
        self.divar=QPushButton(self)
        self.divar.setStyleSheet("background-color: qradialgradient(cx:0.5, cy:0.5,"
                                "fx:0.5,fy:0.5,radius:0.6,"
                                "stop:0 white, stop:1 #c0c0c0);"
                                "border-style: outset;"
                                "border-width: 3px;"
                                "border-radius: 10px;"
                                "border-color: gray;"
                                "padding: 6px;"
                                "color:black;"
                                "font-size:15px;")
        self.torob=QPushButton(self)
        self.torob.setStyleSheet("background-color: qradialgradient(cx:0.5, cy:0.5,"
                                "fx:0.5,fy:0.5,radius:0.6,"
                                "stop:0 white, stop:1 #c0c0c0);"
                                "border-style: outset;"
                                "border-width: 3px;"
                                "border-radius: 10px;"
                                "border-color: gray;"
                                "padding: 6px;"
                                "color:black;"
                                "font-size:15px;")
        self.label_price=QLabel("Product Price",self)
        self.label_price.setStyleSheet("font-size: 20px")
        self.favorit_button=QPushButton("My Favorite",self)
        self.favorit_button.setStyleSheet("background-color: qradialgradient(cx:0.5, cy:0.5,"
                                        "fx:0.5,fy:0.5,radius:0.6,"
                                        "stop:0 white, stop:1 #c0c0c0);"
                                        "border-style: outset;"
                                        "border-width: 3px;"
                                        "border-radius: 10px;"
                                        "border-color: gray;"
                                        "padding: 6px;"
                                        "color:black;"
                                        "font-size:15px;")
        self.favorit_button.setGeometry(450,750,100,32)
        self.favorit_button.clicked.connect(self.add_remove_favorites)
        self.compare_products_btn=QPushButton("Compare Products",self)
        self.compare_products_btn.setStyleSheet("background-color: qradialgradient(cx:0.5, cy:0.5,"
                                        "fx:0.5,fy:0.5,radius:0.6,"
                                        "stop:0 white, stop:1 #c0c0c0);"
                                        "border-style: outset;"
                                        "border-width: 3px;"
                                        "border-radius: 10px;"
                                        "border-color: gray;"
                                        "padding: 6px;"
                                        "color:black;"
                                        "font-size:15px;")
        self.compare_products_btn.setGeometry(25,750,150,32)
        self.compare_products_btn.clicked.connect(self.compare_products_fun)
        self.compare_lst=[]
        self.digikala.clicked.connect(lambda x :self.open_site_digikala()) #set url site
        self.divar.clicked.connect(lambda x :self.open_site_divar()) #set url site
        self.torob.clicked.connect(lambda x :self.open_site_torob()) #set url site

        self.hide_page_product() #hide element page product
        self.hide_page() #hide element page products
        self.hide_sign_in() #hide element page sign in
        self.hide_sign_up() #hide element page sign up
        self.hide_home() #hide element page home

        self.sign_in_gui()
        self.sign_up_gui()
        self.home_page()

        self.show_sign_in() #start program

#--------------------------------------------------------------------------------------------    
    
    #Returning to the first state of errors and input and registration fields
    def defult(self):

        #defult sign in
        self.password_field_sign_in.setStyleSheet("border : 2px solid  white;")
        self.username_field_sign_in.setStyleSheet("border : 2px solid  white;")

        self.username_field_sign_in.clear()
        self.password_field_sign_in.clear()
        self.error_sign_in.clear()

        #defult sign up
        self.password_field_sign_up.setStyleSheet("border : 2px solid  white;")
        self.username_field_sign_up.setStyleSheet("border : 2px solid  white;")
        self.repeat_password_field_sign_up.setStyleSheet("border : 2px solid  white;")
    
        self.username_field_sign_up.clear()
        self.password_field_sign_up.clear()
        self.repeat_password_field_sign_up.clear()
        self.error_sign_up.clear()

#--------------------------------------------------------------------------------------------
    
    def sign_in_gui(self):
        
        # Username label and text field
        self.username_label_sign_in.setGeometry(375,250,100,25)
        self.username_label_sign_in.setStyleSheet("font-size: 20px")
        self.username_field_sign_in.setGeometry(475,250,150,25)
        
        # Password label and text field       
        self.password_label_sign_in.setGeometry(375,300,100,25)
        self.password_label_sign_in.setStyleSheet("font-size: 20px")
        self.password_field_sign_in.setEchoMode(QLineEdit.Password)
        self.password_field_sign_in.setGeometry(475,300,150,25)

        # sign in button 
        self.sign_in_button1.setGeometry(450,400,100,35)
        self.sign_in_button1.clicked.connect(self.sign_in_user)
        self.sign_in_button1.setStyleSheet("background-color: qradialgradient(cx:0.5, cy:0.5,"
                    "fx:0.5,fy:0.5,radius:0.6,"
                    "stop:0 white, stop:1 #d30102);"
                    "border-style: outset;"
                    "border-width: 2px;"
                    "border-radius: 10px;"
                    "border-color: gray;"
                    "padding: 6px;"
                    "color:black;"
                    "font-size:20px;")
        # sign up button
        self.sign_up_button1.setGeometry(463,760,74,30)
        self.sign_up_button1.clicked.connect(self.show_sign_up)
        self.sign_up_button1.setStyleSheet("background-color: qradialgradient(cx:0.5, cy:0.5,"
            "fx:0.5,fy:0.5,radius:0.6,"
            "stop:0 white, stop:1 #d30102);"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: gray;"
            "padding: 6px;"
            "color:black;"
            "font-size:15px;")
        #creat label error message
        self.error_sign_in.setAlignment(Qt.AlignCenter)
        self.error_sign_in.setGeometry(350,350,300,25)
        self.error_sign_in.setStyleSheet("font-size: 20px;color : red")

    def sign_in_user(self):

        #get user and password
        username = self.username_field_sign_in.text()
        password = self.password_field_sign_in.text()

        #change to defult color border
        self.defult()
        
        #set or error sign in user
        try:
            with open('datas\\users.json', 'r') as f:
                data = json.load(f)
                data=decode_dict(data)
                if data[username] == password:

                    self.username=username #save username for add list favorite json file

                    with shelve.open('datas\\my_data_favorites') as db:
                        self.favorites_list = db[username]

                    self.show_home()
                else:
                    self.password_field_sign_in.setStyleSheet("border : 2px solid  red;")
                    self.error_sign_in.setText("Invalid Password")
                    for i in range(0, 6):
                        time.sleep(0.1)
                        if i % 2 == 0:
                            self.password_field_sign_in.move(self.password_field_sign_in.x() - 5, self.password_field_sign_in.y())
                        else:
                            self.password_field_sign_in.move(self.password_field_sign_in.x() + 5, self.password_field_sign_in.y())
                        QApplication.processEvents()
        except :
            self.username_field_sign_in.setStyleSheet("border : 2px solid  red;")
            self.error_sign_in.setText("Invalid Username")
            for i in range(0, 6):
                time.sleep(0.1)
                if i % 2 == 0:
                    self.username_field_sign_in.move(self.username_field_sign_in.x() - 5, self.username_field_sign_in.y())
                else:
                    self.username_field_sign_in.move(self.username_field_sign_in.x() + 5, self.username_field_sign_in.y())
                QApplication.processEvents()
        
    def hide_sign_in(self):
        
        self.username_field_sign_in.hide()
        self.username_label_sign_in.hide()
        self.password_field_sign_in.hide()
        self.password_label_sign_in.hide()
        self.sign_in_button1.hide()
        self.sign_up_button1.hide()
        self.error_sign_in.hide()

    def show_sign_in(self):
        
        self.hide_sign_up()
        self.hide_home()
        self.hide_page()
        self.hide_page_product()
        
        self.username_field_sign_in.show()
        self.username_label_sign_in.show()
        self.password_field_sign_in.show()
        self.password_label_sign_in.show()
        self.sign_in_button1.show()
        self.sign_up_button1.show()
        self.error_sign_in.show()  
        self.defult()

#--------------------------------------------------------------------------------------------

    def sign_up_gui(self):

        # Username label and text field
        self.username_label_sign_up.setGeometry(340,200,150,25)
        self.username_label_sign_up.setStyleSheet("font-size: 20px")
        self.username_field_sign_up.setGeometry(510,200,150,25)

        # Password label and text field 
        self.password_label_sign_up.setGeometry(340,250,150,25)
        self.password_label_sign_up.setStyleSheet("font-size: 20px")
        self.password_field_sign_up.setEchoMode(QLineEdit.Password)
        self.password_field_sign_up.setGeometry(510,250,150,25)

        # reprat Password label and text field
        self.repeat_password_label_sign_up.setGeometry(340,300,170,25)
        self.repeat_password_label_sign_up.setStyleSheet("font-size: 20px")
        self.repeat_password_field_sign_up.setEchoMode(QLineEdit.Password)
        self.repeat_password_field_sign_up.setGeometry(510,300,150,25)

        # sign in button
        self.sign_up_button2.setGeometry(450,400,100,35)
        self.sign_up_button2.setStyleSheet("border : 2px solid  black;")
        self.sign_up_button2.clicked.connect(self.sign_up_user)
        self.sign_up_button2.setStyleSheet("background-color: qradialgradient(cx:0.5, cy:0.5,"
                                            "fx:0.5,fy:0.5,radius:0.6,"
                                            "stop:0 white, stop:1 #d30102);"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-radius: 10px;"
                                            "border-color: gray;"
                                            "padding: 6px;"
                                            "color:black;"
                                            "font-size:20px;")

        # sign up button
        self.sign_in_button2.setGeometry(463,760,74,30)
        self.sign_in_button2.clicked.connect(self.show_sign_in)
        self.sign_in_button2.setStyleSheet("background-color: qradialgradient(cx:0.5, cy:0.5,"
                                            "fx:0.5,fy:0.5,radius:0.6,"
                                            "stop:0 white, stop:1 #d30102);"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-radius: 10px;"
                                            "border-color: gray;"
                                            "padding: 6px;"
                                            "color:black;"
                                            "font-size:15px;")

        #creat label error message
        self.error_sign_up.setAlignment(Qt.AlignCenter)
        self.error_sign_up.setGeometry(250,350,500,25)
        self.error_sign_up.setStyleSheet("font-size: 20px;color : red")

    def sign_up_user(self):

        #get user , password and repeat password
        username = self.username_field_sign_up.text()
        password = self.password_field_sign_up.text()
        repeat_password=self.repeat_password_field_sign_up.text()

        data = {} #save user and pass 

        #chnge to defult color border
        self.defult()

        #set or error sin up user
        with open('datas\\users.json', 'r') as f: #creat or open json file for save data
            data = json.load(f)
            data = decode_dict(data)
        if username in data or len(username)==0:
            self.username_field_sign_up.setStyleSheet("border : 2px solid  red;")
            self.error_sign_up.setText("Username already exists or Less than 1 character!")
            for i in range(0, 6):
                time.sleep(0.1)
                if i % 2 == 0:
                    self.username_field_sign_up.move(self.username_field_sign_up.x() - 5, self.username_field_sign_up.y())
                else:
                    self.username_field_sign_up.move(self.username_field_sign_up.x() + 5, self.username_field_sign_up.y())
                QApplication.processEvents()
        else:   
            if len(password)<6:
                self.password_field_sign_up.setStyleSheet("border : 2px solid  red;")
                self.error_sign_up.setText("Minimum length password is 6!")
                for i in range(0, 6):
                    time.sleep(0.1)
                    if i % 2 == 0:
                        self.password_field_sign_up.move(self.password_field_sign_up.x() - 5, self.password_field_sign_up.y())
                    else:
                        self.password_field_sign_up.move(self.password_field_sign_up.x() + 5, self.password_field_sign_up.y())
                    QApplication.processEvents() 
            else: 

                if password==repeat_password  : 

                    data[username] = password
                    with open('datas\\users.json', 'w') as f:
                        json.dump(encode_dict(data), f)

                    with shelve.open('datas\\my_data_favorites') as db:
                        db[username] = []

                    self.show_sign_in()
                else: 
                    self.repeat_password_field_sign_up.setStyleSheet("border : 2px solid  red;")
                    self.error_sign_up.setText("Repeat password not match!")
                    for i in range(0, 6):
                        time.sleep(0.1)
                        if i % 2 == 0:
                            self.repeat_password_field_sign_up.move(self.repeat_password_field_sign_up.x() - 5, self.repeat_password_field_sign_up.y())
                        else:
                            self.repeat_password_field_sign_up.move(self.repeat_password_field_sign_up.x() + 5, self.repeat_password_field_sign_up.y())
                        QApplication.processEvents()    

    def hide_sign_up(self):
        
        self.username_field_sign_up.hide()
        self.username_label_sign_up.hide()
        self.password_field_sign_up.hide()
        self.password_label_sign_up.hide()
        self.repeat_password_field_sign_up.hide()
        self.repeat_password_label_sign_up.hide()
        self.sign_in_button2.hide()
        self.sign_up_button2.hide()
        self.error_sign_up.hide()

    def show_sign_up(self):

        self.hide_sign_in() 

        self.username_field_sign_up.show()
        self.username_label_sign_up.show()
        self.password_field_sign_up.show()
        self.password_label_sign_up.show()
        self.repeat_password_field_sign_up.show()
        self.repeat_password_label_sign_up.show()
        self.sign_in_button2.show()
        self.sign_up_button2.show()
        self.error_sign_up.show() 
        self.defult()

#-------------------------------------------------------------------------------------------- 
    
    def home_page(self):
        #welcom...
        self.label_show_message.show()
        self.label_show_message.setGeometry(400,25,250,32)
        self.label_show_message.setText("Welcome To Mini Torob")
        self.timer.timeout.connect(lambda :self.label_show_message.setText(""))
        self.timer.start(4000)

        # Add buttons products to the window
        self.all_product_btn.clicked.connect(lambda x:self.page(self.all_product_btn.text(),self.all_lst)) 
        self.all_product_btn.setGeometry(150,200,100,100)

        self.mobiles_btn.clicked.connect(lambda x:self.page(self.mobiles_btn.text(),self.mobile_lst))
        self.mobiles_btn.setGeometry(350,200,100,100)

        self.tablets_btn.clicked.connect(lambda x:self.page(self.tablets_btn.text(),self.tablet_lst))
        self.tablets_btn.setGeometry(550,200,100,100)
        
        self.tves_btn.clicked.connect(lambda x:self.page(self.tves_btn.text(),self.tv_lst))
        self.tves_btn.setGeometry(750,200,100,100)
        
        self.laptops_btn.clicked.connect(lambda x:self.page(self.laptops_btn.text(),self.laptop_lst))
        self.laptops_btn.setGeometry(150,400,100,100)
        
        self.headset_btn.clicked.connect(lambda x:self.page(self.headset_btn.text(),self.headset_lst))
        self.headset_btn.setGeometry(350,400,100,100)
        
        self.favorites_btn.clicked.connect(lambda x:self.page(self.favorites_btn.text(),self.favorites_list))
        self.favorites_btn.setGeometry(550,400,100,100)

        #set style all buttons
        list_button=[self.all_product_btn,self.mobiles_btn,self.tablets_btn,self.tves_btn,self.laptops_btn,self.headset_btn,self.favorites_btn]
        for button in list_button:
            button.setStyleSheet("background-color: qradialgradient(cx:0.8, cy:0.8,"
                                "fx:0.8,fy:0.8,radius:1,"
                                "stop:0 white, stop:1 #003366);"
                                "border-style: outset;"
                                "border-width: 3px;"
                                "border-radius: 10px;"
                                "border-color: gray;"
                                "padding: 6px;"
                                "color:black;"
                                "font-weight : bold;")

        #creat log out button to go sign in page 
        self.log_out.setGeometry(25,35,100,35)
        self.log_out.clicked.connect(self.show_sign_in)   

    def hide_home(self):

        self.log_out.hide()
        self.all_product_btn.hide()
        self.mobiles_btn.hide()
        self.tablets_btn.hide()
        self.tves_btn.hide()
        self.laptops_btn.hide()
        self.headset_btn.hide()
        self.favorites_btn.hide()
        self.label_show_message.hide()
            
    def show_home(self):
           
        self.hide_sign_in()
        self.hide_page()
        self.hide_page_product()
        
        self.log_out.show()
        self.all_product_btn.show()
        self.mobiles_btn.show()
        self.tablets_btn.show()
        self.tves_btn.show()
        self.laptops_btn.show()
        self.headset_btn.show()
        self.favorites_btn.show()
        self.label_show_message.show()

#--------------------------------------------------------------------------------------------   
  
    def page(self,name_products,products): 

        #set name products label
        if type(name_products) is str:
            self.name_products.setText(name_products)
            self.name_products.setAlignment(Qt.AlignCenter)       
            self.name_products.setStyleSheet("font-size: 20px")
            self.name_products.setGeometry(425,15,150,25)

        #creat search box for searching amoung product
        self.search_field.setGeometry(325,70,200,30)
        self.search.setGeometry(550,70,100,30)
        self.list_products_for_search=products

        #creat home button to go home page 
        self.home.setGeometry(875,35,100,35)
        self.home.clicked.connect(self.show_home)

        self.show_page(products)

    def searching(self,name):

        result=[]
        for product in self.list_products_for_search:
            if name.lower() in product.name.lower() :
                result.append(product)
        self.search_field.clear()
        self.show_page(result)

    #creat grid for name products and set on a layout     
    def creat_grid(self,products):

        #at the first clear grid (when click back button last grid is full  and its problem )
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            self.grid.removeWidget(widget)
            widget.setParent(None)

        # Add name products in page
        number_products=0
        for i in range(math.ceil(len(products)/4)):
            for j in range(4):
                if number_products==len(products):
                    break
                button = QPushButton(break_str(products[i*4+j].name)) 
                button.setStyleSheet("background-color: qradialgradient(cx:0.8, cy:0.8,"
                                    "fx:0.8,fy:0.8,radius:1,"
                                    "stop:0 white, stop:1 #003366);"
                                    "border-style: outset;"
                                    "border-width: 3px;"
                                    "border-radius: 10px;"
                                    "border-color: gray;"
                                    "padding: 6px;"
                                    "color:black;"
                                    "font-weight : bold;"
                                    "font-size:10px;")
                button.setFixedWidth(100)
                button.setFixedHeight(100)
                button.clicked.connect(lambda _, product=products[i*4+j]: self.page_product(product,products)) 
                self.grid.addWidget(button, i, j)
                number_products+=1
                
                
        # Create a new scroll area and set the widget as its content
        self.widget.setLayout(self.grid)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.widget)

        # Add the scroll area to the main window
        self.main_layout.setContentsMargins(10, 185, 10, 10)
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

    def hide_page(self):

        self.search_field.hide()
        self.search.hide()
        self.log_out.hide()
        self.home.hide()
        self.scroll_area.setParent(None)
        self.name_products.hide()
        self.favorit_button.hide()

        #clear grid when change the page  
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            self.grid.removeWidget(widget)
            widget.setParent(None)
        
    def show_page(self,products):

        self.creat_grid(products)

        self.hide_home()
        self.hide_page_product()

        self.log_out.show()
        self.home.show()
        self.search_field.show()
        self.search.show()
        self.name_products.show()

#--------------------------------------------------------------------------------------------  

    def page_product(self,product,products):
        #set back button to go page products
        self.back.setGeometry(750,35,100,35)
        self.back.clicked.connect(lambda x : self.show_page(products))
        
        #set photo product at page product
        try :
            image=Image.open(  product._img_dir) #set name photo product , just example
            new_size=(300,300)
            resize_image=image.resize(new_size)
            resize_image.save( product._img_dir) #set name photo product , just example
            self.product_picture = QPixmap( product._img_dir) #set name photo product , just example
            self.label_picture.setPixmap(self.product_picture)
            self.label_picture.setGeometry(600,100,300,300)
        except:
            pass
        #number detail product
        list_detail=[]
        for item in product.features:
            list_detail.append([item,product.features[item]])

        self.table.setRowCount(10)
        self.table.setColumnCount(2)
        try:
            for row in range(10):
                for column in range(2):
                    item = QTableWidgetItem(list_detail[row][column])
                    item.setTextAlignment(Qt.AlignCenter) #set detail product
                    self.table.setItem(row, column, item)
        except:
            pass        
        self.table.horizontalHeader().setDefaultSectionSize(150) #size a tabel
        self.table.verticalHeader().setDefaultSectionSize(50)
        self.table.setGeometry(100,100,302,502)
        self.table.verticalHeader().setVisible(False) #remove index
        self.table.horizontalHeader().setVisible(False)

        #set button price product
        self.label_price.setGeometry(600,550,300,25)
        
        self.digikala.setGeometry(600,600,300,30)
        self.url_digikala=product.link
        self.digikala.setText(fr"Digikala : {product._current_price}") #set price
        self.url_divar=product.similar_product.divar_link
        self.divar.setGeometry(600,650,300,30)
        self.url_torob=product.similar_product.torob_link
        self.divar.setText(fr"Divar : {product.similar_product.divar_price}")  #set price

        self.torob.setGeometry(600,700,300,30)
        
        self.torob.setText(fr"Torob : {product.similar_product.torob_price}")  #set price
        product.link


        #set Favorit product 
        self.favorit_product=product

        #choose product for compare
        self.choose_product=product

        self.show_page_product()

    def compare_products_fun(self):
        self.compare_lst.append(self.choose_product)
        
        if len(self.compare_lst)==1:
            self.label_show_message.setText("Product was selection")
            self.timer.timeout.connect(lambda :self.label_show_message.setText(""))
            self.timer.start(4000)
        elif self.compare_lst[0]==self.compare_lst[1]:
            self.compare_lst.clear()
            self.label_show_message.setText("Product Selection removed")
            self.timer.timeout.connect(lambda :self.label_show_message.setText(""))
            self.timer.start(4000)      
        else:
            for product in self.compare_lst:
                label=QLabel(product.name)
                list_detail=[]
                for item in product.features:
                    list_detail.append([item,product.features[item]])
                table=QTableWidget()
                table.setRowCount(2)
                table.setColumnCount(len(list_detail))
                try:
                    for row in range(2):
                        for column in range(len(list_detail)):
                            item = QTableWidgetItem(list_detail[column][row])
                            item.setTextAlignment(Qt.AlignCenter) #set detail product
                            table.setItem(row, column, item)
                except:
                    pass        
                table.horizontalHeader().setDefaultSectionSize(150) #size a tabel
                table.verticalHeader().setDefaultSectionSize(50)
                table.setGeometry(100,100,302,502)
                table.verticalHeader().setVisible(False) #remove index
                table.horizontalHeader().setVisible(False)

                digikala=QPushButton()
                digikala.clicked.connect(lambda x :self.open_site(product.link)) #set url site
                digikala.setText(fr"Digikala : {product.price}") #set price

                divar=QPushButton()
                divar.clicked.connect(lambda x :self.open_site()) #set url site
                divar.setText(fr"Divar : ")  #set price

                torob=QPushButton()
                torob.clicked.connect(lambda x :self.open_site()) #set url site
                torob.setText(fr"Torob : ")  #set price
                self.layout1.addWidget(label)
                self.layout1.addWidget(table)
                self.layout1.addWidget(digikala)
                self.layout1.addWidget(divar)
                self.layout1.addWidget(torob)
            self.dlg.setLayout(self.layout1)
            self.dlg.exec()

            while self.layout1.count():
                item = self.layout1.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            self.compare_lst.clear()

    #add or remove produt  favorit page
    def add_remove_favorites(self):

        if self.favorit_product in self.favorites_list:
            self.favorites_list.remove(self.favorit_product)
            self.label_show_message.setText("Removed Successfully")
            self.timer.timeout.connect(lambda :self.label_show_message.setText(""))
            self.timer.start(4000)
        else:
            self.favorites_list.append(self.favorit_product)
            self.label_show_message.setText("Added Successfully")
            self.timer.timeout.connect(lambda :self.label_show_message.setText(""))
            self.timer.start(4000)
             
        with shelve.open('datas\\my_data_favorites') as db:
            db[self.username] = self.favorites_list     

    #open chrome
    def open_site_digikala(self,url="https://www.google.com"): #for example
        try:
            webbrowser.open(self.url_digikala)
        except:
            pass    
    #open chrome
    def open_site_divar(self,url="https://www.google.com"): #for example
        try:
            webbrowser.open(self.url_divar)
        except:
            pass
            #open chrome
    def open_site_torob(self,url="https://www.google.com"): #for example
        try:
            webbrowser.open(self.url_torob)
        except:
            pass
    def hide_page_product(self):

        self.back.hide()
        self.label_picture.hide()
        self.table.hide()
        self.digikala.hide()
        self.divar.hide()
        self.torob.hide()
        self.label_price.hide()
        self.favorit_button.hide()
        self.label_show_message.hide()
        self.compare_products_btn.hide()
            
    def show_page_product(self):

        self.hide_page()

        self.log_out.show()
        self.home.show()
        self.back.show()
        self.label_picture.show()
        self.table.show()
        self.digikala.show()
        self.divar.show()
        self.torob.show()
        self.label_price.show()
        self.favorit_button.show()
        self.label_show_message.show()
        self.compare_products_btn.show()

#--------------------------------------------------------------------------------------------  

if __name__ == '__main__':

    with open('datas\\last_time.json', 'r') as l:
        last_time = json.load(l)

    # if time.time() - last_time["time"]> 86400:
    if time.time() - last_time["time"]> 11111:
        system1 = Main()
        system2 = Main()
        system3 = Main()
        system4 = Main()
        system5 = Main()
        shared_ls = {}
        def f0(shared_ls):
            shared_ls[0]=system1.main(search_word = "category-mobile-phone/product-list")
        def f1(shared_ls):
            shared_ls[1]=system2.main(search_word = "category-headphone")
        def f2(shared_ls):
            shared_ls[2]=system3.main(search_word = "category-tv2")
        def f3(shared_ls):
            shared_ls[3]=system4.main(search_word = "category-tablet")
        def f4(shared_ls):
            shared_ls[4]=system5.main(search_word = "notebook-netbook-ultrabook")
        
        t0 = Thread(target=lambda: f0(shared_ls))
        t1 = Thread(target=lambda: f1(shared_ls))
        t2 = Thread(target=lambda: f2(shared_ls))
        t3 = Thread(target=lambda: f3(shared_ls))
        t4 = Thread(target=lambda: f4(shared_ls))
        t0.start()
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t0.join()
        t1.join()
        t2.join()
        t3.join()
        t4.join()

        mobile_lst = shared_ls[0]
        headset_lst = shared_ls[1]
        tv_lst = shared_ls[2]
        tablet_lst = shared_ls[3]
        laptop_lst = shared_ls[4]
        
        with shelve.open('datas\\data_products') as db:
            db['mobile_lst']=mobile_lst
            db['headset_lst']=headset_lst
            db['tv_lst']=tv_lst
            db['tablet_lst']=tablet_lst
            db['laptop_lst']=laptop_lst

        last_time["time"]=time.time()
        with open('datas\\last_time.json', 'w') as l:
            json.dump(last_time, l)
    else: 
        
        with shelve.open('datas\\data_products') as db:
                        
            mobile_lst=db['mobile_lst']
            headset_lst=db['headset_lst']
            tv_lst=db['tv_lst']
            tablet_lst=db['tablet_lst']
            laptop_lst=db['laptop_lst']

    app = QApplication(sys.argv)
    registration_form = RegistrationForm(mobile_lst,headset_lst,tv_lst,tablet_lst,laptop_lst)
    registration_form.show()
    sys.exit(app.exec_())