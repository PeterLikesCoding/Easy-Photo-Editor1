from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog
import os
from PyQt5.QtCore import Qt
from PIL import Image
from PIL import ImageFilter
from PyQt5.QtGui import QPixmap
from PIL.ImageFilter import (SHARPEN,BLUR,CONTOUR,DETAIL,EDGE_ENHANCE,EDGE_ENHANCE_MORE,EMBOSS,FIND_EDGES,SMOOTH,SMOOTH_MORE,GaussianBlur,UnsharpMask)

app = QApplication([])
window = QWidget()
window.resize(700,500)
window.setWindowTitle("Easy editor")
#Dimi mi se racunar, dimi dimi sta se dimi gdje se dimi
main_list = QListWidget()
folder_btn = QPushButton("Folder")
left_btn = QPushButton("Left")
right_btn = QPushButton("Right")
mirror_btn = QPushButton("Mirror")
sharp_btn = QPushButton("Sharpness")
bw_btn = QPushButton("B&W") 
label = QLabel("Image")
#izvukla si cigluuuuuuuuu iz temelja ljubavi moja, dan dan ran da dan, rusis nasu ljubav samo deca ostaše
col1 = QVBoxLayout()
col1.addWidget(folder_btn)
col1.addWidget(main_list)
col2 = QVBoxLayout()
col2.addWidget(label, 95)
row_1 = QHBoxLayout()
row_1.addWidget(left_btn)
row_1.addWidget(right_btn)
row_1.addWidget(mirror_btn)
row_1.addWidget(sharp_btn)
row_1.addWidget(bw_btn)
col2.addLayout(row_1)
main_row = QHBoxLayout()
main_row.addLayout(col1,20)
main_row.addLayout(col2,80)
window.setLayout(main_row)
#mali jura

window.show()
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def filter(files, extentions):
    filter = []
    for filesname in files:
        for ext in extentions:
            if filesname.endswith(ext):
                filter.append(filesname)
    return filter   

def showFilenamelist():
    extentions=[".jpg",".png",".bmp",".gif"]
    chooseWorkdir()
    filenames=filter(os.listdir(workdir),extentions)
    main_list.clear()
    for filename in filenames:
        main_list.addItem(filename)


folder_btn.clicked.connect(showFilenamelist)


class ImageProcessor():
    def __init__ (self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "izmjeni"
    def loadImage(self, dir, filename): 
        self.dir=dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        label.hide()
        pixmapimage= QPixmap(path)
        w, h = label.width(), label.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        label.setPixmap(pixmapimage)
        label.show()

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path) 
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)      
    def do_sharp(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)      
def showChosenImage():
    if main_list.currentRow() >= 0:
        filename = main_list.currentItem().text()
        workimage.loadImage(workdir,filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)

workimage = ImageProcessor()

main_list.currentRowChanged.connect(showChosenImage)
bw_btn.clicked.connect(workimage.do_bw)
mirror_btn.clicked.connect(workimage.do_flip)
left_btn.clicked.connect(workimage.do_left)
right_btn.clicked.connect(workimage.do_right)
sharp_btn.clicked.connect(workimage.do_sharp)




app.exec_()