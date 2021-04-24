from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog)
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image, ImageFilter
#lalala

app = QApplication([])
win = QWidget()
win.resize(700,500)
win.setWindowTitle('Easy Editor')

bt_levo = QPushButton('Лево')
bt_pravo = QPushButton('Право')
bt_zerkalo = QPushButton('Зеркало')
bt_rezkost = QPushButton('Резкость')
bt_chb = QPushButton('Ч/Б')
bt_folder = QPushButton('Папка')

lb_picture = QLabel('')

lw_files = QListWidget()

v1 = QVBoxLayout()
v3 = QVBoxLayout()
h2_main = QHBoxLayout()
h4 = QHBoxLayout()

h4.addWidget(bt_levo)
h4.addWidget(bt_pravo)
h4.addWidget(bt_zerkalo)
h4.addWidget(bt_rezkost)
h4.addWidget(bt_chb)

v1.addWidget(bt_folder)
v1.addWidget(lw_files)

v3.addWidget(lb_picture)
v3.addLayout(h4)

h2_main.addLayout(v1, 23)
h2_main.addLayout(v3, 77)

win.setLayout(h2_main)

workdir = ''

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extentions = ['png', 'jpg', 'jpeg', 'gif']
    chooseWorkdir()
    listFiles = os.listdir(workdir)
    filenames = filter(listFiles,extentions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)

bt_folder.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        lb_picture.hide()
        pixmapimage = QPixmap(path)
        w = lb_picture.width()
        h = lb_picture.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_picture.setPixmap(pixmapimage)
        lb_picture.show()

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_pravo(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_levo(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_rezkost(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

lw_files.currentRowChanged.connect(showChosenImage)

bt_chb.clicked.connect(workimage.do_bw)
bt_zerkalo.clicked.connect(workimage.do_flip)
bt_pravo.clicked.connect(workimage.do_pravo)
bt_levo.clicked.connect(workimage.do_levo)
bt_rezkost.clicked.connect(workimage.do_rezkost)

win.show()
app.exec_()
