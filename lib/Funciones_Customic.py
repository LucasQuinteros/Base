
'''
for install qdarkstyle libraries:
pip install qdarkstyle
pip install .
python setup.py install
'''

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence, QPalette, QColor, QWindow
import qdarkstyle  # noqa: E402
from qdarkstyle.dark.palette import DarkPalette  # noqa: E402
from qdarkstyle.light.palette import LightPalette  # noqa: E402

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, center, Qt
from PyQt5 import QtCore, QtGui, QtWidgets

#from qts.Ui_Menu_principal import Ui_MainWindow

class clase_customic(QWidget):
        def __init__(self):
                super().__init__()
                self.flag = False
                self.flag2 = False
                self.darkmode = False
                self.setWindowTitle("CHWCT (Change Window Colours Theme) v.05")
                self.setFixedSize(480, 220)
                
                #grupos
                GroupBox1 = QGroupBox('Selección de Colores')
                GroupBox2 = QGroupBox('Info')
                #botones
                #self.boton1 = QPushButton('Black&White/ReverseColour', self)
                #self.boton1.setFixedSize(380,25)
                #self.boton1.clicked.connect(self.blackwhite)
                self.boton2 = QPushButton('&Guardar Colores', self)
                self.boton2.setFixedSize(150,25)
                self.boton2.clicked.connect(self.guardar)
                self.boton3 = QPushButton('&Acerca de...', self)
                self.boton3.setFixedSize(150,25)
                self.boton3.clicked.connect(self.acercade)
                self.boton4 = QPushButton('Q&DarkStile/QLightStile', self)
                self.boton4.setFixedSize(380,25)
                self.boton4.clicked.connect(self.QDarkLight)
                self.boton5 = QPushButton('&Salir', self)
                self.boton5.setFixedSize(150,25)
                self.boton5.clicked.connect(self.Salir)
                self.boton6 = QPushButton('&OriginalStile', self)
                self.boton6.setFixedSize(380,25)
                self.boton6.clicked.connect(self.OriginalStile)
                # Layout de los botones y grupos
                lay1 = QVBoxLayout(self)
                lay1.setAlignment(Qt.AlignCenter)
                #lay1.addWidget(self.boton1)
                lay1.addWidget(self.boton4)
                lay1.addWidget(self.boton6)
                lay1.addSpacing(10)
                lay1.addWidget(self.boton2, alignment=Qt.AlignRight)
                
                lay2 = QHBoxLayout(self)
                lay2.addWidget(self.boton3, alignment=Qt.AlignLeft)
                lay2.addWidget(self.boton5, alignment=Qt.AlignRight)
        
                GroupBox1.setLayout(lay1)
                GroupBox2.setLayout(lay2)
        
                mainLay = QVBoxLayout(self)
                mainLay.addWidget(GroupBox1)
                mainLay.addWidget(GroupBox2)
        
        def OriginalStile(self):
                qApp.setStyleSheet("")
                #self.palette = self.palette([])
                #self.setPalette(self.palette)
                #QApplication.setPalette(self.palette)
                qApp.setStyle('Fusion')
        
        def QDarkLight(self):
                if not self.flag2:
                        style = qdarkstyle.load_stylesheet(palette=DarkPalette)
                        self.darkmode = True
                else:
                        style = qdarkstyle.load_stylesheet(palette=LightPalette)
                        self.darkmode = False
                self.flag2 = not self.flag2
                qApp.setStyleSheet(style)

        def blackwhite(self):
                qApp.setStyleSheet("")
                #print("click")
                if not self.flag: #ok
                        self.palette.setColor(QPalette.Background, QColor('black'))
                        self.palette.setColor(QPalette.Foreground, QColor('White'))
                        self.palette.setColor(QPalette.Window, QColor('black'))
                        self.palette.setColor(QPalette.WindowText, QColor('White'))
                        self.palette.setColor(QPalette.Button, QColor('white'))
                        self.palette.setColor(QPalette.ButtonText, QColor('black'))
                        self.palette.setColor(QPalette.Base, QColor('white'))
                        self.palette.setColor(QPalette.AlternateBase, QColor('white'))
                        self.palette.setColor(QPalette.Highlight, QColor('black'))
                        self.palette.setColor(QPalette.HighlightedText, QColor('white'))  
                else: 
                        self.palette.setColor(QPalette.Background, QColor('black'))
                        self.palette.setColor(QPalette.Foreground, QColor('white'))                        
                        self.palette.setColor(QPalette.Window, QColor('white'))
                        self.palette.setColor(QPalette.WindowText, QColor('black'))
                        self.palette.setColor(QPalette.Button, QColor('black'))
                        self.palette.setColor(QPalette.ButtonText, QColor('white'))
                        self.palette.setColor(QPalette.Base, QColor('white'))
                        self.palette.setColor(QPalette.AlternateBase, QColor('white'))
                        self.palette.setColor(QPalette.Highlight, QColor('black'))
                        self.palette.setColor(QPalette.HighlightedText, QColor('white'))
                QApplication.setPalette(self.palette)
                self.setPalette(self.palette)
                qApp.setStyle('Fusion')
                self.flag = not self.flag

        def acercade(self):
                #QApplication.setPalette(self.palette)
                QMessageBox.about(self, "Acerca de...", "CHWCT (Change Window Colours Theme) v.05 is a proyect by Alan R.G.Systemas for customing a Lucas Base for Meva")

        def guardar(self):
                #QApplication.setPalette(self.palette)
                dialog = Dialog(self)  # self hace referencia al padre
                dialog.show()
        
        def Salir(self):
                self.close()

class Dialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Guardar Colores")
        self.setFixedSize(250, 70)
        self.botonSi = QPushButton('&Si', self)
        self.botonSi.setFixedSize(90,30)
        self.botonSi.clicked.connect(self.clickeoSi)
        self.botonNo = QPushButton('&No', self)
        self.botonNo.setFixedSize(90,30)
        self.botonNo.clicked.connect(self.clickeoNo)
        lay = QHBoxLayout(self)
        lay.addWidget(self.botonSi)
        lay.addWidget(self.botonNo)

    def clickeoSi(self):
        self.close()
        
    def clickeoNo(self):
        self.close()

'''
if __name__ == '__main__':
    import sys
    #app = QtWidgets.QApplication(sys.argv)   
    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')    # <-----
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    w = clase_customic()
    w.show()
    sys.exit(app.exec_())
'''
