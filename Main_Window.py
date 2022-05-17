# alan.rg.add 28.04.2022
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence, QPalette, QColor, QWindow
import qdarkstyle  # noqa: E402
from qdarkstyle.dark.palette import DarkPalette  # noqa: E402
from qdarkstyle.light.palette import LightPalette  # noqa: E402
from PyQt5.QtWidgets import QPushButton, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import center, pyqtSlot
from lib.Funciones_Customic import  clase_customic #alan.rg.add
# end alan.rg.add

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QSizePolicy, QTableWidgetItem,QTableWidget,QTableView, QWidget
from PyQt5 import QtSql,QtWidgets,QtCore
from PyQt5.QtCore import QSettings, Qt


import sys

from lib.Funciones_Buscar import clase_buscar
from lib.Funciones_Modificar import clase_modificar
from lib.Funciones_Movimientos import clase_movimientos
from lib.Funciones_Nuevo import clase_nuevo
from lib.Funciones_Ingresos import clase_ingresos
from lib.Funciones_Configuraciones import clase_configuraciones
from lib.Funciones_MenuPrincipal import clase_principal

from qts.Ui_Menu_principal import Ui_MainWindow


if __name__ == '__main__':
    #app = QApplication(sys.argv)
    app = QtWidgets.QApplication(sys.argv)  #alan.rg.mod 28.04.2022

    Myapp = clase_principal()
    
    #Myapp.widget.changeEvent = Myapp.changeEvent
    
    #alan.rg.add 28.04.2022
    app.setStyle('Fusion')
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    #end.alan.rg.add
    
       
    sys.exit(app.exec_())
    
