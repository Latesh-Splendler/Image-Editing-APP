from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
import os
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageEnhance, ImageFilter
import cv2


app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("George's PhotoShop")
main_window.resize(1200, 900)


btn_folder = QPushButton("Folder")
file_list = QListWidget()



btn_left = QPushButton("left")
btn_right = QPushButton("right")
Saturation = QPushButton("color")
Blur = QPushButton("Blur")
Sharpness = QPushButton("Sharpen")
Black_White = QPushButton("B/W")
mirror = QPushButton("mirror")


filter_box = QComboBox()
filter_box.addItem("Original")
filter_box.addItem("left")
filter_box.addItem("right")
filter_box.addItem("color")
filter_box.addItem("Blur")
filter_box.addItem("Sharpen")
filter_box.addItem("B/W")
filter_box.addItem("mirror")




picture_box = QLabel("Your Image will appear here!..")




master_layout = QHBoxLayout()

col1 = QVBoxLayout()
col2 = QVBoxLayout()


col1.addWidget(btn_folder)
col1.addWidget(file_list)
col1.addWidget(filter_box)
col1.addWidget(btn_left)
col1.addWidget(Saturation)
col1.addWidget(Blur)
col1.addWidget(btn_right)
col1.addWidget(Sharpness)
col1.addWidget(Black_White)
col1.addWidget(mirror)



col2.addWidget(picture_box)


master_layout.addLayout(col1, 20)
master_layout.addLayout(col2, 80)

main_window.setLayout(master_layout)



working_directory = ""


def filter(files, extensions):
  results = []
  for file in files:
    for ext in extensions:
      if file.endswith(ext):
        results.append(file)
  return results


def getWorkdirectory():
  global working_directory
  working_directory = QFileDialog.getExistingDirectory()
  extensions = ['.jpg','.jpeg','.png','.svg']
  filenames = filter(os.listdir(working_directory), extensions)
  file_list.clear()
  for filename in filenames:
    file_list.addItem(filename)



class Editor():
  def __init__(self):
    self.image = None
    self.original = None
    self.filename = None
    self.save_folder = "New Edits"



  def load_image(self, filename):
    self.filename = filename
    fullname = os.path.join(working_directory, self.filename)
    self.image = Image.open(fullname)
    self.original = self.image.copy()


  def save_image(self):
    path = os.path.join(working_directory, self.save_folder)
    if not(os.path.exists(path) or os.path.isdir(path)):
      os.makedirs(path)

    fullname = os.path.join(path, self.filename)
    self.image.save(fullname)



  def show_image(self, path):
    picture_box.hide()
    image = QPixmap(path)
    w, h = picture_box.width(), picture_box.height()
    image = image.scaled(w, h, Qt.KeepAspectRatio)
    picture_box.setPixmap(image)
    picture_box.show() 


  def gray(self):
    self.image = self.image.convert('L')
    self.save_image()
    grayscale_path = os.path.join(working_directory, self.save_folder, self.filename)
    self.show_image(grayscale_path)


  def left(self):
    self.image = self.image.transpose(Image.ROTATE_90)
    self.save_image()
    grayscale_path = os.path.join(working_directory, self.save_folder, self.filename)
    self.show_image(grayscale_path)


  def blur(self):
    self.image = self.image.filter(ImageFilter.BLUR)
    self.save_image()
    grayscale_path = os.path.join(working_directory, self.save_folder, self.filename)
    self.show_image(grayscale_path)
  
  def contrast(self):
    self.image = ImageEnhance.Contrast(self.image).enhance(1.8)
    self.save_image()
    grayscale_path = os.path.join(working_directory, self.save_folder, self.filename)
    self.show_image(grayscale_path)

  def right(self):
    self.image = self.image.transpose(Image.ROTATE_90)
    self.save_image()
    grayscale_path = os.path.join(working_directory, self.save_folder, self.filename)
    self.show_image(grayscale_path)


  
  def color(self):
    self.image = ImageEnhance.Color(self.image).enhance(1.4)
    self.save_image()
    grayscale_path = os.path.join(working_directory, self.save_folder, self.filename)
    self.show_image(grayscale_path)  

  
  

  def mirror(self):
    self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
    self.save_image()
    mirrored_path = os.path.join(working_directory, self.save_folder, self.filename)
    self.show_image(mirrored_path)
  

  def applt_filter(self, filter_name):
    if filter_name == "Original":
      self.image = self.original.copy()
    else:
      napping = {
        "btn_left": lambda image:image.convert("Image.ROTATE_90"),
        "btn_right": lambda image:image.convert("Image.ROTATE_180"),
        "Saturation": lambda image: ImageEnhance.Contrast(image).enhance(1.8),
        "Blur": lambda image: image.filter(ImageFilter.BLUR),
        "Black_White": lambda image:image.convert("L"),
        "mirror": lambda image: image.transpose(Image.FLIP_LEFT_RIGHT)

      }  

      filter_funtion = napping.get(filter_name)
      if filter_funtion:
        self.image = filter_funtion(self.image)
        self.save_image()
        image_path = os.path.join(working_directory, self.save_folder, self.filename)
        self.show_image(image_path)

      pass

    self.save_image()
    image_path = os.path.join(working_directory, self.save_folder, self.filename)
    self.show_image(image_path)




def handle_filter():
  if file_list.currentRow() >= 0:
    select_filter = filter_box.currentText()
    main.applt_filter(select_filter)





def displayImage():
  if file_list.currentRow() >= 0:
    filename = file_list.currentItem().text()
    main.load_image(filename)
    main.show_image(os.path.join(working_directory, main.filename))

 
main = Editor()


btn_folder.clicked.connect(getWorkdirectory)
file_list.currentRowChanged.connect(displayImage)
filter_box.currentTextChanged.connect(handle_filter)



Black_White.clicked.connect(main.gray)
btn_left.clicked.connect(main.left)
Blur.clicked.connect(main.blur)
Sharpness.clicked.connect(main.contrast)
btn_right.clicked.connect(main.right)
Saturation.clicked.connect(main.color)
mirror.clicked.connect(main.mirror)



main_window.show()
app.exec_()