from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QSizePolicy, QTableWidgetItem,QTableWidget,QTableView, QWidget
from PyQt5 import QtSql,QtWidgets,QtCore
from PyQt5.QtCore import QSettings, Qt

import sys
import mysql.connector
from mysql.connector import errorcode

from lib.Funciones_Buscar import clase_buscar
from lib.Funciones_Modificar import clase_modificar
from lib.Funciones_Movimientos import clase_movimientos
from lib.Funciones_Nuevo import clase_nuevo
from lib.Funciones_Ingresos import clase_ingresos
from lib.Funciones_Configuraciones import clase_configuraciones

from qts.Ui_Menu_principal import Ui_MainWindow


class clase_principal(QWidget):
    def __init__(self):
        super(clase_principal,self).__init__()
        self.MainWindow = QMainWindow()
        self.Pag_configuraciones = clase_configuraciones()
        self.Pag_Busqueda = clase_buscar(self.Pag_configuraciones.connector)
        self.Pag_modificar = clase_modificar()
        self.Pag_nuevo = clase_nuevo()
        self.Pag_movimientos = clase_movimientos('Pag_busqueda')
        self.Pag_ingresos = clase_ingresos(self.Pag_configuraciones.connector)

        self.widget = QtWidgets.QStackedWidget()
        self.widget.setMinimumSize(1600,1200)
        self.widget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.Boton_Ingreso.clicked.connect(self.GotoIngreso)
        self.ui.Boton_Buscar.clicked.connect(self.GotoBuscar)
        self.ui.Boton_Config.clicked.connect(self.GotoConfig)
        self.widget.addWidget(self.MainWindow)
        
        self.Pag_Busqueda.ui.pushButton.clicked.connect(self.Pag_Busqueda.request)
        self.Pag_Busqueda.ui.buttonBox.accepted.connect(self.ir_menu)
        self.Pag_Busqueda.ui.buttonBox.rejected.connect(self.ir_menu)
        #Pag_Busqueda.ui.pushButton_2.clicked.connect(GotoNuevo)
        self.Pag_Busqueda.menu.triggered.connect(self.GotoModificar)
        self.widget.addWidget(self.Pag_Busqueda.widget)

        self.Pag_modificar.procCargar.connect(self.Pag_Busqueda.proc_cargar)
        self.Pag_modificar.ui.pushButton.clicked.connect(self.GotoBuscar)
        self.Pag_modificar.menu.triggered.connect(self.GotoMovimientos)
        self.widget.addWidget(self.Pag_modificar.widget)

        self.Pag_nuevo.ui.pushButton.clicked.connect(self.GotoBuscar)
        self.widget.addWidget(self.Pag_nuevo.widget)

        self.Pag_movimientos.procCargar.connect(self.Pag_modificar.proc_cargar)
        self.Pag_movimientos.ui.pushButton.clicked.connect(self.GotoModificar)
        self.widget.addWidget(self.Pag_movimientos.widget)

        #Pag_ingresos.ui.pushButton_6.clicked.connect(GotoMovimientos)
        self.Pag_ingresos.ui.buttonBox.accepted.connect(self.ir_menu)
        self.Pag_ingresos.ui.buttonBox.rejected.connect(self.ir_menu)
        self.widget.addWidget(self.Pag_ingresos.widget)

        self.Pag_configuraciones.procEstado.connect(self.proc_estado)
        self.Pag_configuraciones.procCargar.connect(self.proc_cargar)
        self.Pag_configuraciones.ui.pushButton_2.clicked.connect(self.ir_menu)
        self.widget.addWidget(self.Pag_configuraciones.widget)
        
        self.widget.setWindowTitle('Base v1.0')
        self.widget.showMaximized()

        self.Probar_conexion()
    @QtCore.pyqtSlot(bool)
    def proc_estado(self,bool):
        if(bool):
            self.ui.label.setText("Estado: Conectado")
        else:
            self.ui.label.setText("Estado: Desconectado")

    @QtCore.pyqtSlot(dict)
    def proc_cargar(self,message):
        self.Pag_Busqueda.Actualizar_Conector(message)
        self.Pag_ingresos.Actualizar_Conector(message)
        self.Probar_conexion()
        print(message)


    def Probar_conexion(self):
        try:
                self.cnx = mysql.connector.connect(user=self.Pag_configuraciones.connector['user'], 
                                                        password=self.Pag_configuraciones.connector['password'],
                                                        host=self.Pag_configuraciones.connector['host'],
                                                        database=self.Pag_configuraciones.connector['database'])
                cursor = self.cnx.cursor()
        except mysql.connector.Error as err:
                self.proc_estado(False)
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)
        else:
                self.proc_estado(True)
                cursor.close()
        
    def GotoBuscar(self):
        self.widget.setCurrentIndex(1)
        self.Pag_Busqueda.cargar_tablas()

    def ir_menu(self):
        self.widget.setCurrentIndex(0)
        
    def GotoModificar(self,arg):
        self.widget.setCurrentIndex(2)
        if( type(arg) != bool ):
            item =  arg.data()
            self.Pag_modificar.setparams(item)
            print(item)

    def GotoMovimientos(self,arg):
        self.widget.setCurrentIndex(4)
        if( type(arg) != bool):
            if( type(arg)!= int):
                item =  arg.data()
                self.Pag_movimientos.setparams(item)
                print(item)

    def GotoNuevo(self):
        self.widget.setCurrentIndex(3)
        self.Pag_nuevo.Cargar_tablas(self.Pag_Busqueda.cnx)

    def GotoIngreso(self):
        self.widget.setCurrentIndex(5)
        self.Pag_ingresos.Cargar_tablas()

    def GotoConfig(self):
        self.widget.setCurrentIndex(6)