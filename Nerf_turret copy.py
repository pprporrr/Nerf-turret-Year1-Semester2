from PyQt5.QtMultimediaWidgets import *
from importlib.resources import *
from PyQt5.QtMultimedia import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore

import arduino_communication

import urllib.request

import numpy as np

import time

import cv2

import sys

import os

class bluetooth_window(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        #change path
        self.ui = loadUi('C:\\Users\\Chakrit\\OneDrive\\Desktop\\ALMOST ALMOST FINAL PRJECT\\GUI\\bluetooth_window.ui', self)
        self.COMport_edit = self.ui.portline_edit
        self.COMport_edit.setStyleSheet("color: white")
        self.connect_button = self.ui.connect_button
        self.connect_button.clicked.connect(self.check_if_can_connect)
        self.parent.bluetooth = True
    
    def check_if_can_connect(self):
        port = self.COMport_edit.text()
        if (self.parent.ard_com.connect(port)):
            self.connect()
        else:
            self.COMport_edit.setText("Can't connect")
            self.COMport_edit.setAlignment(QtCore.Qt.AlignCenter)
    
    def connect(self):
        self.parent.connected = True
        self.parent.set_ui_bluetooth()
        self.parent.tool_bar()
        self.close()
    
    def closeEvent(self, event):
        self.parent.bluetooth = False

class nerf_app(QMainWindow):
    def __init__(self):
        super().__init__()
        #change path
        self.ui = loadUi('C:\\Users\\Chakrit\\OneDrive\\Desktop\\ALMOST ALMOST FINAL PRJECT\\GUI\\nerf_app.ui', self)
        self.x_medium = 0
        self.y_medium = 0
        self.save_path = ""
        self.COM_port = ""
        self.bluetooth = False
        self.connected = False     
        self.on_pad = False
        self.motor = False           
        self.shoot = False      
        self.path = False
        self.pad = False 
        self.position_x = 130
        self.position_y = 120
        self.x = 130
        self.y = 120
        self.movement = 0
        self.check_seq = 0   
        self.save_seq = 0
        self.ard_com = arduino_communication.com_ard(self)
        self.bluetooth_button = self.ui.bluetooth_button                   
        self.motor_button = self.ui.motor_on_button    
        self.check_button = self.ui.check_button  
        self.auto_button = self.ui.auto_button 
        self.pad_label_w = self.ui.pad_label_w 
        self.pad_label_a = self.ui.pad_label_a 
        self.pad_label_s = self.ui.pad_label_s
        self.pad_label_d = self.ui.pad_label_d
        self.pad_label = self.ui.pad_label 
        self.textedit = self.ui.textedit
        self.bluetooth_button.clicked.connect(self.connect_bluetooth_window)
        self.auto_button.clicked.connect(self.set_ui_auto)
        self.motor_button.clicked.connect(self.motor_on_off)     
        self.check_button.clicked.connect(self.connect_cam)
        self.textedit.setAlignment(QtCore.Qt.AlignCenter)
        self.textedit.setStyleSheet("color: white")
        cp = QDesktopWidget().availableGeometry().center()
        fg_app = self.frameGeometry()
        fg_app.moveCenter(cp)
        fg_app.setY(fg_app.y())
        self.move(fg_app.topLeft()) 
        #change url
        self.url = 'http://172.20.10.7/cam-lo.jpg'

    def connect_cam(self):
        loop = True
        while(loop == True):
            img_resp=urllib.request.urlopen(self.url)
            imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
            frame=cv2.imdecode(imgnp,-1)
            cv2.imwrite(os.path.join(self.save_path , "Capture_picture_{}.png".format(self.save_seq)), frame)
            print("Capture_picture_{}.png".format(self.save_seq))
            self.detection("Capture_picture_{}.png".format(self.save_seq))
            self.save_seq += 1
            if loop == True:
                loop = False
                break
    
    def select_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Picture Location", "")
        self.path = True
        self.check_button.setEnabled(True)
        if path:
            self.save_path = path
        self.save_seq = 0
    
    def connect_bluetooth_window(self):
        if not self.connected and not self.bluetooth:
            connect_bluetooth = bluetooth_window(self)
            cp = QDesktopWidget().availableGeometry().center()
            fg_blue = connect_bluetooth.frameGeometry()
            fg_blue.moveCenter(cp)
            fg_blue.setX(fg_blue.x() + 490)
            fg_blue.setY(fg_blue.y() + 20)
            connect_bluetooth.move(fg_blue.topLeft())
            connect_bluetooth.show()
    
    def set_ui_bluetooth(self):
        #change path
        new_button_img = QIcon('C:\\Users\\Chakrit\\OneDrive\\Desktop\\ALMOST ALMOST FINAL PRJECT\\GUI\\bluetooth_connect.png')
        self.bluetooth_button.setIcon(new_button_img)
        self.motor_button.setEnabled(True)
        self.auto_button.setEnabled(True)
        self.pad = True
    
    def set_ui_auto(self):
        if not self.auto:
            #change path
            new_button_auto = QIcon('C:\\Users\\Chakrit\\OneDrive\\Desktop\\ALMOST ALMOST FINAL PRJECT\\GUI\\auto_on.png')
            self.auto_button.setIcon(new_button_auto)
            self.movement = 0
            self.auto = True
            self.connect_cam()
            self.set_arduino_message()
        elif self.auto:
            #change path
            new_button_auto = QIcon('C:\\Users\\Chakrit\\OneDrive\\Desktop\\ALMOST ALMOST FINAL PRJECT\\GUI\\auto_off.png')
            self.auto_button.setIcon(new_button_auto)
            #change path
            self.pad_label.setPixmap(QPixmap('C:\\Users\\Chakrit\\OneDrive\\Desktop\\ALMOST ALMOST FINAL PRJECT\\GUI\\pad-pc.png'))
            self.auto = False
            self.set_arduino_message()

    def tool_bar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        select_folder_action = QAction("Select save location", self)
        select_folder_action.setToolTip("Select save location")
        select_folder_action.triggered.connect(self.select_folder)
        toolbar.addAction(select_folder_action)
        toolbar.setStyleSheet("background : grey;")
    
    def motor_on_off(self):
        if self.connected:
            self.motor = self.motor_button.isChecked()
            if self.motor:
                #change path
                self.motor_button.setIcon(QIcon('C:\\Users\\Chakrit\\OneDrive\\Desktop\\ALMOST ALMOST FINAL PRJECT\\GUI\\motor_on.png'))
                self.motor = True
                self.set_arduino_message()
            else:
                #change path
                self.motor_button.setIcon(QIcon('C:\\Users\\Chakrit\\OneDrive\\Desktop\\ALMOST ALMOST FINAL PRJECT\\GUI\\motor_off.png'))
                self.motor = False
                self.set_arduino_message()
    
    def shoot_target(self):
        if self.motor:
            if self.auto:
                self.x = self.x_medium
                self.y = self.y_medium - 20
                self.set_arduino_message()
                time.sleep(1)
            self.shoot = True
            self.textedit.setText("Shoot!!!")
            self.textedit.setAlignment(QtCore.Qt.AlignCenter)
            print("Shoot!!!")
            self.set_arduino_message()
            self.shoot_target_release()
        else:
            self.textedit.setText("Motor off")
            self.textedit.setAlignment(QtCore.Qt.AlignCenter)
            print("Turn on motor")
    
    def shoot_target_release(self):
        self.shoot = False
        self.x_medium = 0
        self.y_medium = 0
        self.set_arduino_message()

    def detection(self, name):
        images_path = self.save_path + "\\" + name
        #change path
        net = cv2.dnn.readNet("C:\\Users\\Chakrit\\OneDrive\\Desktop\\ALMOST ALMOST FINAL PRJECT\\yolov3_training_last.weights", "C:\\Users\\Chakrit\\OneDrive\\Desktop\\ALMOST ALMOST FINAL PRJECT\\yolov3_testing.cfg")
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        img = cv2.imread(images_path)
        height, width, channels = img.shape
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        count = 1
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                if count == 1:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 1)
                    cv2.rectangle(img, (x, y-50), (x + w, y), (0, 0, 0), -1)
                    cv2.putText(img, "Target"+str(count), (x + int(w/10),y-25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1)
                    self.x_medium = int((x + (x + w)) / 2)
                    self.y_medium = int((y + (y + h)) / 2)
                count = count + 1
        cv2.imwrite(os.path.join(self.save_path , "Capture_picture_{}_Tracked.png".format(self.save_seq)), img)
        self.pad_label.setPixmap(QPixmap(os.path.join(self.save_path , "Capture_picture_{}_Tracked.png".format(self.save_seq))))

    def set_arduino_message(self):
        if self.connected:
            message = bytearray([255, self.x, self.y, self.motor, self.shoot, self.movement, 254])
            self.ard_com.send_message(message)
    
    def remap(self, value_to_map, new_range_min, new_range_max, old_range_min, old_range_max):
        remapped_val = (value_to_map - old_range_min) * (new_range_max - new_range_min) / (
                    old_range_max - old_range_min) + new_range_min
        if (remapped_val > new_range_max):
            remapped_val = new_range_max
        elif (remapped_val < new_range_min):
            remapped_val = new_range_min
        return remapped_val
    
    def keyPressEvent(self, event):
        try:
            if self.connected:
                if event.key() == QtCore.Qt.Key_W:
                    self.movement = 1
                    self.textedit.setText("Forward")
                    self.textedit.setAlignment(QtCore.Qt.AlignCenter)
                    self.set_arduino_message()
                if event.key() == QtCore.Qt.Key_A:
                    self.movement = 2
                    self.textedit.setText("Move Left")
                    self.textedit.setAlignment(QtCore.Qt.AlignCenter)
                    self.set_arduino_message()
                if event.key() == QtCore.Qt.Key_S:
                    self.movement = 3
                    self.textedit.setText("Backward")
                    self.textedit.setAlignment(QtCore.Qt.AlignCenter)
                    self.set_arduino_message()
                if event.key() == QtCore.Qt.Key_D:
                    self.movement = 4
                    self.textedit.setText("Move Right")
                    self.textedit.setAlignment(QtCore.Qt.AlignCenter)
                    self.set_arduino_message()
                if event.key() == QtCore.Qt.Key_P:
                    self.movement = 0
                    self.textedit.setText("Park")
                    self.textedit.setAlignment(QtCore.Qt.AlignCenter)
                    self.set_arduino_message()
                if event.key() == QtCore.Qt.Key_Return:
                    if self.motor:
                        self.shoot_target() 
                event.accept()
        except:
            pass
    
    def mouseMoveEvent(self, event):
        if self.pad:
            if (191<event.x()<431 and 41<event.y()<281):
                self.x = int(self.remap(event.x(), 0, 240, 191, 431))
                self.y = int(self.remap(event.y(), 0, 240, 41, 281))
                self.on_pad = True
                self.set_arduino_message()
            else:
                self.x = 130
                self.y = 120
                self.on_pad = False
                self.set_arduino_message()
            if (280<event.x()<340 and 300<event.y()<350):
                self.movement = 1
                self.textedit.setText("Forward")
                self.textedit.setAlignment(QtCore.Qt.AlignCenter)
                self.set_arduino_message()
            elif (200<event.x()<260 and 380<event.y()<420):
                self.movement = 2
                self.textedit.setText("Move Left")
                self.textedit.setAlignment(QtCore.Qt.AlignCenter)
                self.set_arduino_message()
            elif (280<event.x()<340 and 380<event.y()<420):
                self.movement = 3
                self.textedit.setText("Backward")
                self.textedit.setAlignment(QtCore.Qt.AlignCenter)
                self.set_arduino_message()
            elif (360<event.x()<420 and 380<event.y()<420):
                self.movement = 4
                self.textedit.setText("Move Right")
                self.textedit.setAlignment(QtCore.Qt.AlignCenter)
                self.set_arduino_message()
            else:
                self.movement = 0
                self.textedit.setText("...")
                self.textedit.setAlignment(QtCore.Qt.AlignCenter)
                self.set_arduino_message()
        else:
            self.x = 130
            self.y = 120
            self.on_pad = False
            self.set_arduino_message()
    
    def mousePressEvent(self, event):
        if self.on_pad and self.motor:
            self.shoot_target()
        elif not self.motor:
            self.textedit.setText("Motor off")
            self.textedit.setAlignment(QtCore.Qt.AlignCenter)
            print("Turn on motor")
    
    def mouseReleaseEvent(self, event):
        if self.on_pad:
            self.shoot = False
            self.set_arduino_message()
    
    def closeEvent(self, event):
        try:
            int_check_seq = int(self.check_seq)
            int_save_seq = int(self.save_seq)
            for int_check_seq in range(int_save_seq):
                pic_location = self.save_path + '//' + "Capture_picture_{}.png".format(int_check_seq)
                os.remove(pic_location)
                track_location = self.save_path + '//' + "Capture_picture_{}_Tracked.png".format(int_check_seq)
                os.remove(track_location)
                int_check_seq += 1
        except:
            print("Don't have file")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    App = nerf_app()
    App.show()
    app.exec_()