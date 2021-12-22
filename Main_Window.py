from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QSizePolicy, QTableWidgetItem,QTableWidget,QTableView, QWidget
from PyQt5 import QtSql,QtWidgets,QtCore
from PyQt5.QtCore import Qt

import sys

from lib.Funciones_Buscar import clase_buscar
from lib.Funciones_Modificar import clase_modificar
from lib.Funciones_Movimientos import clase_movimientos
from lib.Funciones_Nuevo import clase_nuevo
from lib.Funciones_Ingresos import clase_ingresos
from lib.Funciones_Configuraciones import clase_configuraciones

from qts.Ui_Menu_principal import Ui_MainWindow

lastindex = 0

def GotoBuscar():
    widget.setCurrentIndex(1)
    Pag_Busqueda.cargar_tablas()

def ir_menu():
    widget.setCurrentIndex(0)
    
def GotoModificar(arg):
    widget.setCurrentIndex(2)
    if( type(arg) != bool ):
        item =  arg.data()
        Pag_modificar.setparams(item)
        print(item)

def GotoMovimientos(arg):
    widget.setCurrentIndex(4)
    if( type(arg) != bool):
        if( type(arg)!= int):
            item =  arg.data()
            Pag_movimientos.setparams(item)
            print(item)

def GotoNuevo():
    widget.setCurrentIndex(3)
    Pag_nuevo.Cargar_tablas(Pag_Busqueda.cnx)

def GotoIngreso():
    widget.setCurrentIndex(5)
    Pag_ingresos.Cargar_tablas()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    Pag_Busqueda = clase_buscar()
    Pag_modificar = clase_modificar()
    Pag_nuevo = clase_nuevo()
    Pag_movimientos = clase_movimientos('Pag_busqueda')
    Pag_ingresos = clase_ingresos()
    #Pag_configuraciones = clase_coincidencias()
    widget = QtWidgets.QStackedWidget()
    
    
    widget.setMinimumSize(1600,1200)
    widget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
    
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.Boton_Ingreso.clicked.connect(GotoIngreso)
    ui.Boton_Buscar.clicked.connect(GotoBuscar)
    widget.addWidget(MainWindow)
      
    Pag_Busqueda.ui.pushButton.clicked.connect(Pag_Busqueda.request)
    Pag_Busqueda.ui.buttonBox.accepted.connect(ir_menu)
    Pag_Busqueda.ui.buttonBox.rejected.connect(ir_menu)
    #Pag_Busqueda.ui.pushButton_2.clicked.connect(GotoNuevo)
    Pag_Busqueda.menu.triggered.connect(GotoModificar)
    widget.addWidget(Pag_Busqueda.widget)

    Pag_modificar.procCargar.connect(Pag_Busqueda.proc_cargar)
    Pag_modificar.ui.pushButton.clicked.connect(GotoBuscar)
    Pag_modificar.menu.triggered.connect(GotoMovimientos)
    widget.addWidget(Pag_modificar.widget)

    Pag_nuevo.ui.pushButton.clicked.connect(GotoBuscar)
    widget.addWidget(Pag_nuevo.widget)

    Pag_movimientos.procCargar.connect(Pag_modificar.proc_cargar)
    Pag_movimientos.ui.pushButton.clicked.connect(GotoModificar)
    widget.addWidget(Pag_movimientos.widget)

    #Pag_ingresos.ui.pushButton_6.clicked.connect(GotoMovimientos)
    Pag_ingresos.ui.buttonBox.accepted.connect(ir_menu)
    Pag_ingresos.ui.buttonBox.rejected.connect(ir_menu)
    widget.addWidget(Pag_ingresos.widget)


    
    widget.setWindowTitle('Base v1.0')
    
    widget.showMaximized()
    sys.exit(app.exec_())