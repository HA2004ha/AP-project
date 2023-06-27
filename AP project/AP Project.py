import sys
import json
import time
import math
from PIL import Image
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import webbrowser

class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()

        #set titele and size window
        self.setWindowTitle('Mini Torob')
        self.setFixedSize(1000, 800)

        #List of products
        self.favorites_list=[]

        #set backgroung
        self.pixmap = QPixmap("home.jpg")
        self.label=QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.resize(1000,800)

        #object for sign in gui
        self.username_label_sign_in = QLabel('Username:', self)
        self.username_field_sign_in = QLineEdit(self)
        self.password_label_sign_in = QLabel('Password:', self)
        self.password_field_sign_in = QLineEdit(self)
        self.sign_in_button1 = QPushButton('Sign in', self)
        self.sign_up_button1 = QPushButton('Sign up', self)
        self.error_sign_in=QLabel("",self)

        #object for sign up gui
        self.username_label_sign_up = QLabel('Username :', self)
        self.username_field_sign_up = QLineEdit(self)
        self.password_label_sign_up = QLabel('Password:', self)
        self.password_field_sign_up = QLineEdit(self)
        self.repeat_password_label_sign_up = QLabel(' Repeat Password:', self)
        self.repeat_password_field_sign_up = QLineEdit(self)
        self.sign_in_button2 = QPushButton('Sign in', self)
        self.sign_up_button2 = QPushButton('Sign up', self)
        self.error_sign_up=QLabel("",self) 

        #object for home gui
        self.search_field=QLineEdit(self)
        self.search=QPushButton('Search',self)
        self.log_out=QPushButton("Log Out",self)
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
        self.widget = QWidget()
        self.scroll_area = QScrollArea()
        self.main_layout = QVBoxLayout()

        #object for page product gui
        self.back=QPushButton("Back",self)
        self.label_picture=QLabel(self)
        self.table = QTableWidget(self)
        self.digikala=QPushButton(self)
        self.divar=QPushButton(self)
        self.torob=QPushButton(self)
        self.label_price=QLabel("Product Price",self)
        self.favorit_button=QPushButton("My Favorit",self)
        self.favorit_button.setGeometry(450,750,100,25)
        self.favorit_button.clicked.connect(self.add_remove_favorites)

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
            with open('users.json', 'r') as f:
                data = json.load(f)

                if data[username] == password:

                    self.username=username #save username for add list favorite json file

                    with open('favorites.json', 'r') as fa: #read list of favorite each user 
                        favorit_lst = json.load(fa)
                        self.favorites_list=favorit_lst[username]

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
        with open('users.json', 'r') as f: #creat or open json file for save data
            data = json.load(f)

        #creat or open json file for save favorit list for each user    
        with open('favorites.json', 'r') as fa:
            favorit_lst = json.load(fa)    

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
                    with open('users.json', 'w') as f:
                        json.dump(data, f)

                    favorit_lst[username]=[]
                    with open('favorites.json', 'w') as fa:
                        json.dump(favorit_lst, fa)  

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

        # Add buttons products to the window
        self.all_product_btn.clicked.connect(lambda x:self.page(self.all_product_btn.text(),["1","2"]+["3","4"])) 
        self.all_product_btn.setGeometry(150,200,100,100)

        self.mobiles_btn.clicked.connect(lambda x:self.page(self.mobiles_btn.text(),["5","6"]))
        self.mobiles_btn.setGeometry(350,200,100,100)

        self.tablets_btn.clicked.connect(lambda x:self.page(self.tablets_btn.text(),["7","8"]))
        self.tablets_btn.setGeometry(550,200,100,100)
        
        self.tves_btn.clicked.connect(lambda x:self.page(self.tves_btn.text(),["9","10"]))
        self.tves_btn.setGeometry(750,200,100,100)
        
        self.laptops_btn.clicked.connect(lambda x:self.page(self.laptops_btn.text(),["11","12"]))
        self.laptops_btn.setGeometry(150,400,100,100)
        
        self.headset_btn.clicked.connect(lambda x:self.page(self.headset_btn.text(),["13","14"]))
        self.headset_btn.setGeometry(350,400,100,100)
        
        self.favorites_btn.clicked.connect(lambda x:self.page(self.favorites_btn.text(),self.favorites_list))
        self.favorites_btn.setGeometry(550,400,100,100)

        #creat log out button to go sign in page 
        self.log_out.setGeometry(25,25,75,25)
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

#--------------------------------------------------------------------------------------------   
  
    def page(self,name_products,products): 

        #set name products label
        if type(name_products) is str:
            self.name_products.setText(name_products)
            self.name_products.setAlignment(Qt.AlignCenter)       
            self.name_products.setStyleSheet("font-size: 20px")
            self.name_products.setGeometry(425,0,150,25)

        #creat search box for searching amoung product
        self.search_field.setGeometry(350,50,200,25)
        self.search.setGeometry(575,50,75,25)

        #creat home button to go home page 
        self.home.setGeometry(900,25,75,25)
        self.home.clicked.connect(self.show_home)
        
        self.show_page(products)

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
                button = QPushButton(products[i*4+j]) 
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
        self.back.setGeometry(800,25,75,25)
        self.back.clicked.connect(lambda x : self.show_page(products))
        
        #set photo product at page product
        image=Image.open("iphon.webp") #set name photo product , just example
        new_size=(300,300)
        resize_image=image.resize(new_size)
        resize_image.save("iphon.webp") #set name photo product , just example
        self.product_picture = QPixmap("iphon.webp") #set name photo product , just example
        self.label_picture.setPixmap(self.product_picture)
        self.label_picture.setGeometry(100,100,300,300)

        #number detail product
        self.table.setRowCount(10)
        self.table.setColumnCount(2)
        
        for row in range(10):
            for column in range(2):
                item = QTableWidgetItem("Row %d, Column %d" % (row+1, column+1)) #set detail product
                self.table.setItem(row, column, item)
                
        self.table.horizontalHeader().setDefaultSectionSize(150) #size a tabel
        self.table.verticalHeader().setDefaultSectionSize(50)
        self.table.setGeometry(600,100,302,502)
        self.table.verticalHeader().setVisible(False) #remove index
        self.table.horizontalHeader().setVisible(False)

        #set button price product
        self.label_price.setGeometry(100,550,300,25)

        self.digikala.setGeometry(100,600,300,25)
        self.digikala.clicked.connect(lambda x :self.open_site()) #set url site
        self.digikala.setText(fr"Digikala : ") #set price

        self.divar.setGeometry(100,650,300,25)
        self.divar.clicked.connect(lambda x :self.open_site()) #set url site
        self.divar.setText(fr"Divar : ")  #set price

        self.torob.setGeometry(100,700,300,25)
        self.torob.clicked.connect(lambda x :self.open_site()) #set url site
        self.torob.setText(fr"Torob : ")  #set price
        
        #set Favorit product 
        self.favorit_product=product

        self.show_page_product()
        
    #add or remove produt  favorit page
    def add_remove_favorites(self):

        if self.favorit_product in self.favorites_list:
            self.favorites_list.remove(self.favorit_product)
        else:
            self.favorites_list.append(self.favorit_product)
             
        with open('favorites.json', 'r') as fa:
            favorit_lst = json.load(fa) 
            
        favorit_lst[self.username]=self.favorites_list
        with open('favorites.json', 'w') as fa:
            json.dump(favorit_lst, fa)     

    #open chrome
    def open_site(self,url="https://www.google.com"): #for example
        webbrowser.open(url)

    def hide_page_product(self):

        self.back.hide()
        self.label_picture.hide()
        self.table.hide()
        self.digikala.hide()
        self.divar.hide()
        self.torob.hide()
        self.label_price.hide()
        self.favorit_button.hide()
         
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
    
#--------------------------------------------------------------------------------------------  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    registration_form = RegistrationForm()
    registration_form.show()
    sys.exit(app.exec_())