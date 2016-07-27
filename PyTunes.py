import sys
import time
from threading import Thread
from PyQt4 import QtGui, QtCore
import pygame
import pyglet
import time

class Window(QtGui.QWidget):


    def __init__(self):
        super(Window, self).__init__()
        self.is_paused = False
        self.mainPage()


    def mainPage(self):
        #Music Progress Bar
        self.prog = QtGui.QProgressBar(self)
        self.prog.setGeometry(0, 0, 100, 20)

        #Choose Music Button
        self.choose_btn = QtGui.QPushButton("Load Music", self)
        self.choose_btn.clicked.connect(self.loadMusic)
        self.choose_btn.move(0, 60)

        #Play/Pause Button
        self.play_btn = QtGui.QPushButton("Play", self)
        self.play_btn.clicked.connect(self.playMusic)
        self.play_btn.move(0, 30)

        #Quit Action
        quitAction = QtGui.QAction("&Quit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.triggered.connect(self.close_application)
        
        #Layout
        hbox = QtGui.QHBoxLayout()
        self.setLayout(hbox)
        self.setGeometry(300, 300, 100, 100)
        self.setWindowTitle("PyTunes")
        self.show()


    def musicProgress(self, dur):
        print("Processing")
        #Use multithread to emit every percentage so it updates the bar when emitted
        #EMit should increment self.current until it hit's self.maximum
        #Create ProgThread Object, pass duration of song
        self.progThread = ProgThread(duration=dur)
        #Start it
        self.progThread.start()
        #Connect to thread, passes the value to "updateBar" automatically
        self.progThread.progSignal.connect(self.updateBar)
        

    def updateBar(self, value):
        print("Bar Updated")
        self.prog.setRange(0, self.duration)
        self.prog.setValue(value)


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


    def loadMusic(self):
        name = QtGui.QFileDialog.getOpenFileName(self, "Choose Song")
        print("close")
        file = open(name, "r")
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        self.play_btn.setText("Pause")
        src = pyglet.media.load(name)
        self.duration = src.duration
        print(str(self.duration))
        self.musicProgress(self.duration)

    def close_application(self):
        choice = QtGui.QMessageBox.question(self, "Quit",
                                           "Would you like to quit?",
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if choice == QtGui.QMessageBox.Yes:
            print("Program Closed")
            sys.exit()
        else:
            pass

class ProgThread(QtCore.QThread):
    
    progSignal = QtCore.pyqtSignal(int)

    def __init__(self, duration, parent=None):
        super(ProgThread, self).__init__(parent)
        self.duration = duration

    def run(self):
        print("Processing Thread")
        print(self.duration)
        self.current = 0 #pygame.mixer.music.get_pos()
        print(self.current < self.duration)
        while self.current < self.duration:
            self.current = pygame.mixer.music.get_pos() / 1000
            print(self.current)
            QtGui.QApplication.processEvents()
            self.progSignal.emit(self.current)
            time.sleep(0.01)

        

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
