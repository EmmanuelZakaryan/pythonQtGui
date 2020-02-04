from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import QTimer, Signal
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile, QObject, QThread, Slot

import firebase_admin
from firebase_admin import credentials, firestore
import sys
from threading import Thread
import cv2
from pyzbar import pyzbar
from time import time, sleep
from ast import literal_eval
import os

try:
    app = QtWidgets.QApplication([])

    ui_file = QFile("gui/page1.ui")
    ui_file.open(QFile.ReadOnly)
    loader = QUiLoader()

    main = loader.load("gui/page1.ui")
    personnal = loader.load("gui/page2.ui")

    main.qr.setPixmap(QtGui.QPixmap('gui/qr.png'))   


    personnal.acier.setPixmap(QtGui.QPixmap('gui/cons2.png'))
    personnal.alu.setPixmap(QtGui.QPixmap('gui/can.png'))
    personnal.verre.setPixmap(QtGui.QPixmap('gui/beer.png'))
    personnal.pet.setPixmap(QtGui.QPixmap('gui/evian.png'))
    personnal.autre.setPixmap(QtGui.QPixmap('gui/nonRecycled.gif'))
except:
    pass

global oldp, visible

oldp = []
visible = False

class OtherThread(QThread):

    v = Signal(object)

    def run(self):

        while True:

            try:
                c = open("actual.txt", "r").readlines()
            except:
                print("couldnt read")
                continue
            
            self.v.emit(c)

            sleep(0.5)
            
                
class MyApp(QObject):

    def __init__(self):

        print("init start")
        super(MyApp, self).__init__()
        self.thread = OtherThread(self)
        self.thread.v.connect(self.update)
        self.thread.start()
        print("init done")

    def updateGui(self, p):

        try:
            d = literal_eval(p[0])
            name = p[1]
        except:
            print("File data type is not right")
            sys.exit(1)
            return

        personnal.nacier.setText(str(d["acier"]))
        personnal.nalu.setText(str(d["alu"]))
        personnal.npet.setText(str(d["pet"]))
        personnal.nverre.setText(str(d["verre"]))
        personnal.nautre.setText(str(d["autre"]))

        n = d["acier"]+d["alu"]+d["verre"]+d["pet"]+d["autre"]

        personnal.points.setText( "points : " + str(n))

        personnal.name.setText("Bonjour " + name)

        print(name, d)

        print("out refresh")

    @Slot(object)
    def update(self, p):

        global oldp, visible

        print(p)

        if p == [] and visible == False:
            pass
   
        if p == [] and visible == True:
            print("personnal hide() 1")
            personnal.hide()
            visible = False
            
        if p != [] and visible == False:
            print("personnal.show() 1")
            personnal.show()
            visible = True
        
        if oldp == p:
            print("No need to update")
            oldp = p

        if oldp != p and p != []:
            print("updating")
            self.updateGui(p)
            oldp = p



        print("visible -> ", visible)

        #sleep(0.5)


ma = MyApp()

main.show()

sys.exit(app.exec_())
