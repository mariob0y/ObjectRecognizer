from imageai.Detection import ObjectDetection
import os

execution_path = os.getcwd()

#Importing a model
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()

#Scanning function
def machine_scan():
    global names
    global percentages
    names = list()
    percentages = list()
    
    detections = detector.detectObjectsFromImage(
        input_image=os.path.join(user_image),
        output_image_path=os.path.join(execution_path, "output_image.jpg"),
        )
    #Results of scan 
    for eachObject in detections:
        name = eachObject['name']
        names.insert(0, name)
        percentage = eachObject["percentage_probability"]
        percentages.insert(0, percentage)
        print(eachObject["name"], ": ", eachObject["percentage_probability"], '\n')
    #Cleaning up a text for output

    result = list(zip(names, percentages))  
    result.reverse()
    global restxt
    restxt = str(result)

    restxt = restxt.replace("('", "")
    restxt = restxt.replace(")", "")
    restxt = restxt.replace(" ", "")
    restxt = restxt.replace("[", "")
    restxt = restxt.replace("]", "")
    restxt = restxt.replace("',", " : ")
    restxt = restxt.replace(",", "\n")
 


from PyQt5 import uic
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        #Importing interface of main window
        uic.loadUi('gui.ui', self)
        self.show()
        #"Open" button connect
        self.openb.clicked.connect(self.openFileNameDialog)
        #"Read" button connect
        self.readb.clicked.connect(self.reading)

            
    # Function of "Open" button  
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        global user_image
        user_image = fileName
        print(user_image)
        if fileName:
            self.pic.setPixmap(QtGui.QPixmap(fileName))
            

    # Function of "Scan" button       
    def reading(self):
        machine_scan()
        self.result.setText(restxt)
        self.pic.setPixmap(QtGui.QPixmap('output_image.jpg'))

        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()