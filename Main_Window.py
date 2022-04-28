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
    app = QApplication(sys.argv)

    Myapp = clase_principal()
       
    sys.exit(app.exec_())