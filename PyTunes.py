import sys
from PyQt4 import QtGui, QtCore
import pygame

class Window(QtGui.QWidget):

    def __init__(self):
        super(Window, self).__init__()
        self.is_paused = False
        self.mainPage()


    def mainPage(self):

        #Choose Music Button
        self.choose_btn = QtGui.QPushButton("Load Music", self)
        self.choose_btn.clicked.connect(self.loadMusic)
        self.choose_btn.move(0, 60)

        #play music button
        self.play_btn = QtGui.QPushButton("Play", self)
        self.play_btn.clicked.connect(self.playMusic)
        self.play_btn.move(0, 30)

        #Quit button
        quitAction = QtGui.QAction("&Quit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.triggered.connect(self.close_application)
        
        hbox = QtGui.QHBoxLayout()
        self.setLayout(hbox)

        self.setGeometry(300, 300, 100, 100)
        self.setWindowTitle("PyTunes")
        self.show()

    def playMusic(self):
        
        if pygame.mixer.get_init() == None:
            QtGui.QMessageBox.about(self, "No music loaded", "No music loaded")
        elif pygame.mixer.music.get_busy() == True and self.is_paused == False:
            pygame.mixer.music.pause()
            self.play_btn.setText("Play")
            self.is_paused = True
        elif self.is_paused == True:
            pygame.mixer.music.unpause()
            self.play_btn.setText("Pause")
            self.is_paused = False
        print(self.is_paused)

    def loadMusic(self):
        name = QtGui.QFileDialog.getOpenFileName(self, "Choose Song")
        file = open(name, "r")
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        self.play_btn.setText("Pause")


    def close_application(self):
        choice = QtGui.QMessageBox.question(self, "Quit", "Would you like to quit?",
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if choice == QtGui.QMessageBox.Yes:
            print("Program Closed")
            sys.exit()
        else:
            pass

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    
    sys.exit(app.exec_())
run()
