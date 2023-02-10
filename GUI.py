import requests
import os
from PIL import Image
import json
from PySide6.QtWidgets import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys
import ezgmail
import threading

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):

        # create label for background image
        bg_label = QLabel(self)
        bg_pixmap = QPixmap("/home/interstellar/python_amFOSS_project/icons/bg_image.png")
        bg_label.setPixmap(bg_pixmap)
        bg_label.resize(bg_pixmap.width(), bg_pixmap.height())
        bg_label.move(1650, 0)

        # create buttons
        fetch_button = QPushButton("Fetch Image")
        next_button = QPushButton("Next Image")
        prev_button = QPushButton("Prev Image")
        send_button = QPushButton("Send Email")  

        # create image label and text box label

        self.image_label = QLabel()

        self.date_input = QtWidgets.QLineEdit(self)
        self.date_input.move(1420, 200)
        self.date_input.resize(490,30)
        self.date_input.text()
        self.date_input.show()

        self.email_id = QtWidgets.QLineEdit(self)
        self.email_id.move(1420, 350)
        self.email_id.resize(490,30)
        self.email_id.text()
        self.email_id.show()

        self.date_input1 = QLabel(self)
        self.date_input1.setText("Date:")
        self.date_input1.move(1375, 200)

        self.camera_input = QComboBox(self)
        self.camera_input.addItems(['fhaz','mast','rhaz','navcam'])
        self.camera_input.show()
        self.current_values = self.camera_input.currentText()
        self.camera_input.move(1420, 250)
        self.camera_input.resize(490,30) 

        self.camera_input1 = QLabel(self)
        self.camera_input1.setText("Camera:")
        self.camera_input1.move(1355,250)

        self.page_input = QComboBox(self)
        self.page_input.addItems(['1','2','3','4'])
        self.page_input.show()
        self.page_current_values = self.page_input.currentText()
        self.page_input.move(1420, 300)
        self.page_input.resize(490,30)

        self.page_input1 = QLabel(self)
        self.page_input1.setText("Page:")
        self.page_input1.move(1370,300)

        self.email_id1 = QLabel(self)
        self.email_id1.setText("Email ID:")
        self.email_id1.move(1355, 350)

        self.image_label = QLabel(self)
        
        # create horizontal layout for buttons
        h_layout = QHBoxLayout()
        h_layout.addWidget(fetch_button)
        h_layout.addWidget(prev_button)
        h_layout.addWidget(next_button)
        h_layout.addWidget(send_button)
        
        # create vertical layout for image label and buttons
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.image_label)
        v_layout.addLayout(h_layout)
        
        # set main layout
        self.setLayout(v_layout)
        
        # connect buttons to functions
        fetch_button.clicked.connect(self.fetch_image)
        next_button.clicked.connect(self.next_image)
        prev_button.clicked.connect(self.prev_image)
        send_button.clicked.connect(self.send_email)

        # set icons for buttons
        fetch_button.setIcon(QIcon("/home/interstellar/python_amFOSS_project/icons/fetch_icon.png"))
        next_button.setIcon(QIcon("/home/interstellar/python_amFOSS_project/icons/next_icon.png"))
        prev_button.setIcon(QIcon("/home/interstellar/python_amFOSS_project/icons/prev_icon.png"))
        send_button.setIcon(QIcon("/home/interstellar/python_amFOSS_project/icons/send_email.png"))

        # add stylesheet
        self.setStyleSheet("""
            QPushButton {
                background-color: #ffa07a;
                color: #ffffff;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
        """)\
        
        self.setStyleSheet("""
            QVBoxLayout{
                background-color: black;
                color: #ffffff;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
        """)\
        
    def fetch_image(self):
        enter_date = self.date_input.text()
        page = self.page_input.text()
        self.api_key = '5SmFOsZLd2pZod4q3aaBn0s0mGQg88B8iTG9y5WV'
        print("clicked")
        
        response=requests.get('https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date='+enter_date+'&page='+page+'&api_key='+self.api_key)
        # response=requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date=2015-6-3&api_key=5SmFOsZLd2pZod4q3aaBn0s0mGQg88B8iTG9y5WV')
  
        data=json.loads(response.text) #converts json into text
        os.makedirs('rover_images',exist_ok=True) # make directory

        data1= data['photos'] # gets values of the key photos
        pictures=[] # list to store picture urls


        for i in data1:

            for j in i:
                if j=='img_src':
                    pictures.append(i[j])
        print(pictures) # Gets the image URL

        n=0
        for i in pictures:
            print(i)
            img=Image.open(requests.get(i,stream=True).raw)
            print("image opened")
            os.chdir(r'/home/interstellar/python_amFOSS_project/rover_images')
            img.save(f'attachments{n}.jpg')
            n+=1

        self.show_image()
        
    def send_email(self):
        emailid = (self.email_id.text()).lower() 
        images_folder=os.listdir(f'/home/interstellar/python_amFOSS_project/rover_images')
        print(images_folder)
        os.chdir(f'/home/interstellar/python_amFOSS_project/rover_images')
        cwd = os.getcwd()
        print(cwd)
        ezgmail.send(str(emailid),'Mars Rover images','Here are the images',images_folder)

    def next_image(self):
        if self.image_index < self.count - 1:
            print("Button nxt is working")
            self.image_index += 1
            pixmap = QPixmap(self.images[self.image_index])
            pixmap = pixmap.scaled(1000, 1920, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
        
    def prev_image(self):
        if self.image_index > 0:
            print("Button prev is working")
            self.image_index -= 1
            pixmap = QPixmap(self.images[self.image_index])
            pixmap = pixmap.scaled(1000, 1920, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
        
    def show_image(self):
        self.images=os.listdir(r'/home/interstellar/python_amFOSS_project/rover_images')
        self.images.append(f"/home/interstellar/python_amFOSS_project/rover_images")
        os.chdir(r'/home/interstellar/python_amFOSS_project/rover_images')
        self.count=0
        dir_path='/home/interstellar/python_amFOSS_project/rover_images'
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                self.count+=1
        self.image_index = 0
        pixmap = QPixmap(self.images[self.image_index])
        pixmap = pixmap.scaled(1000, 1920, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)
        
    def retriving_image(self):
        pic = threading.Thread(target=self.fetch_image)
        pic.start()

    def sending_mail(self):
        mail = threading.Thread(target=self.send_email)
        mail.start()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.setGeometry(10, 10, 1920, 1080)
    viewer.setWindowTitle("The Martian Chronicles")
    viewer.show()
    sys.exit(app.exec())
