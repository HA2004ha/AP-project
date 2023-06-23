import sys
import json
import time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        #set titele and size window
        self.setWindowTitle('Mini Torob')
        self.setFixedSize(1000, 800)

        #set home background
        self.pixmap_home = QPixmap("home.jpg")
        self.label_home=QLabel(self)

        #set sign in and up backgroung
        self.pixmap = QPixmap("background.jpg")
        self.label=QLabel(self)

        #object for sign in gui
        self.username_label_sign_in = QLabel('Username :', self)
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
        self.grid = QGridLayout()
        self.search_field=QLineEdit(self)
        self.search=QPushButton('Search',self)
        self.log_out=QPushButton("Log Out",self)

        self.hide_sign_in() #hide element page sign in
        self.hide_sign_up() #hide element page sign up
        self.hide_home() #hide element page home
        self.sign_in_gui() #show and creat sign in page
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

        self.hide_sign_up()
        self.hide_home()
        self.defult()

        #set background
        self.label.setPixmap(self.pixmap)
        self.label.resize(1000,800)
        
        # Username label and text field
        self.username_label_sign_in.setGeometry(390,250,150,25)
        self.username_label_sign_in.setStyleSheet("font-size: 20px")
        self.username_field_sign_in.setGeometry(500,250,150,25)

        # Password label and text field       
        self.password_label_sign_in.setGeometry(390,300,150,25)
        self.password_label_sign_in.setStyleSheet("font-size: 20px")
        self.password_field_sign_in.setEchoMode(QLineEdit.Password)
        self.password_field_sign_in.setGeometry(500,300,150,25)

        # sign in button 
        self.sign_in_button1.setGeometry(508,400,75,25)
        self.sign_in_button1.setStyleSheet("border : 2px solid  black;")
        self.sign_in_button1.clicked.connect(self.sign_in_user)

        # sign up button
        self.sign_up_button1.setGeometry(447,760,75,25)
        self.sign_up_button1.setStyleSheet("border-radius : 20px")
        self.sign_up_button1.clicked.connect(self.sign_up_gui)

        #creat label error message
        self.error_sign_in.setAlignment(Qt.AlignCenter)
        self.error_sign_in.setGeometry(390,350,300,25)
        self.error_sign_in.setStyleSheet("font-size: 20px;color : red")

        self.show_sign_in()
   
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
                    self.hide_sign_in()
                    self.home_page()
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
        self.username_field_sign_in.show()
        self.username_label_sign_in.show()
        self.password_field_sign_in.show()
        self.password_label_sign_in.show()
        self.sign_in_button1.show()
        self.sign_up_button1.show()
        self.error_sign_in.show()    

#--------------------------------------------------------------------------------------------

    def sign_up_gui(self):
        self.hide_sign_in() 
        self.defult()

        #set background
        self.label.setPixmap(self.pixmap)
        self.label.resize(1000,800)

        # Username label and text field
        self.username_label_sign_up.setGeometry(390,200,150,25)
        self.username_label_sign_up.setStyleSheet("font-size: 20px")
        self.username_field_sign_up.setGeometry(560,200,150,25)

        # Password label and text field 
        self.password_label_sign_up.setGeometry(390,250,150,25)
        self.password_label_sign_up.setStyleSheet("font-size: 20px")
        self.password_field_sign_up.setEchoMode(QLineEdit.Password)
        self.password_field_sign_up.setGeometry(560,250,150,25)

        # reprat Password label and text field
        self.repeat_password_label_sign_up.setGeometry(390,300,170,25)
        self.repeat_password_label_sign_up.setStyleSheet("font-size: 20px")
        self.repeat_password_field_sign_up.setEchoMode(QLineEdit.Password)
        self.repeat_password_field_sign_up.setGeometry(560,300,150,25)

        # sign in button
        self.sign_up_button2.setGeometry(518,400,75,25)
        self.sign_up_button2.setStyleSheet("border : 2px solid  black;")
        self.sign_up_button2.clicked.connect(self.sign_up_user)

        # sign up button
        self.sign_in_button2.setGeometry(447,760,75,25)
        self.sign_in_button2.setStyleSheet("border-radius : 20px")
        self.sign_in_button2.clicked.connect(self.sign_in_gui)

        #creat label error message
        self.error_sign_up.setAlignment(Qt.AlignCenter)
        self.error_sign_up.setGeometry(310,350,500,25)
        self.error_sign_up.setStyleSheet("font-size: 20px;color : red")

        self.show_sign_up()

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
                    self.sign_in_gui()
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
        self.username_field_sign_up.show()
        self.username_label_sign_up.show()
        self.password_field_sign_up.show()
        self.password_label_sign_up.show()
        self.repeat_password_field_sign_up.show()
        self.repeat_password_label_sign_up.show()
        self.sign_in_button2.show()
        self.sign_up_button2.show()
        self.error_sign_up.show() 
#--------------------------------------------------------------------------------------------     
    def home_page(self):
        self.label.clear() #clear sign in background

        #set home background
        self.label_home.setPixmap(self.pixmap_home)
        self.label_home.resize(1000,800)
        
        # Add buttons products to the grid layout
        list_name=["Mobile","Tablet","TV","Laptop","Headset","Favorites"]
        for i in range(2):
            for j in range(3):
                button = QPushButton(list_name[i*2+j+1])
                button.setFixedWidth(100)
                button.setFixedHeight(100)
                self.grid.addWidget(button, i, j)

        self.setLayout(self.grid) #add grid to window

        #creat log out button to go sign in page 
        self.log_out.setGeometry(25,25,75,25)
        self.log_out.clicked.connect(self.sign_in_gui)

        #creat search box for searching amoung product
        self.search_field.setGeometry(350,50,200,25)
        self.search.setGeometry(575,50,75,25)

        self.show_home()

    def hide_home(self):
        self.log_out.hide()
        self.search_field.hide()
        self.search.hide()
        self.label_home.clear()
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            self.grid.removeWidget(widget)
            widget.setParent(None)
            
    def show_home(self):
        self.search_field.show()
        self.search.show()
        self.log_out.show()
      
if __name__ == '__main__':
    app = QApplication(sys.argv)
    registration_form = RegistrationForm()
    registration_form.show()
    sys.exit(app.exec_())