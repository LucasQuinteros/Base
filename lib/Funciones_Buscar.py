from PyQt5.QtGui import QColor
import mysql.connector
import ast
import os
from mysql.connector import errorcode
from mysql.connector.connection import MySQLConnection
from mysql.connector.errors import Error
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QHeaderView, QMenu, QWidget,QMessageBox
from qts.Ui_ventana_busqueda import Ui_Form
### Esta libreria debe ser una clase que contenga la ventana y todos sus campos ne
### necesarios para funcionar con sus rutinas asociadas
### Lo mismo para la ventana menu


class clase_buscar(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.widget)
        self.menu = QMenu(self)
        self.action = self.menu.addAction("Modificar")       
        #self.menu.triggered.connect(self.Modificar)
        self.cnx = mysql.connector.connect(user='root', 
                                            password='12345678',
                                            host='10.0.0.50',
                                            database='movedb')

        self.ui.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu) 
        self.ui.tableWidget.customContextMenuRequested.connect(self.generateMenu)
        self.ui.tableWidget.viewport().installEventFilter(self)

        self.ui.pushButton_2.setDisabled(1)

        self.diccateg = {'':'0'}
        self.dicSecequip = {'':'0'}
        self.dicubifisica = {'':'0'}
        self.dicubiexacta = {'':'0'}
        self.dicestado = {'':'0'}
        
    
    @QtCore.pyqtSlot(list)
    def proc_cargar(self,message):
        i = 0
        j = 1
        filas = self.ui.tableWidget.rowCount()
        columnas = self.ui.tableWidget.columnCount()
        while(i< filas):
            if(self.ui.tableWidget.item(i,0).text() == message[0]):
                while(j < columnas ):
                    self.ui.tableWidget.item(i,j).setText(message[j])
                    j = j + 1
                i = filas
            i = i + 1
        print(message)    
    
    def eventFilter(self,source,event):
        if(event.type() == QtCore.QEvent.KeyPress and
           source is self.ui.tableWidget.viewport()):
            print(event.key())
            if event.modifiers() == QtCore.Qt.AltModifier:
                print('Shift+Click')
                texto = self.ui.tableWidget.item(0,2).text()
                self.ui.tableWidget.item(0,2).setText(texto + os.linesep )
                self.ui.tableWidget.verticalHeader().resizeSections(QHeaderView.ResizeToContents)
            if event.key() == QtCore.Qt.Key_Return: 
                print('Enter pressed')
                #print(self.ui.tableWidget.itemAt(event.pos()))

        if(event.type() == QtCore.QEvent.MouseButtonPress and
           event.buttons() == QtCore.Qt.RightButton and
           source is self.ui.tableWidget.viewport()):
            item = self.ui.tableWidget.itemAt(event.pos())
            print('Global Pos:', event.globalPos())
            if item is not None:  
                print('Table Item:', item.row(), item.column() )

                Fila = list()
                i = 0
                Fila.append(self.cnx)
                print(self.ui.tableWidget.columnCount())
                while (i < self.ui.tableWidget.columnCount() ):
                    Fila.append(self.ui.tableWidget.item(item.row(), i).text())
                    i = i + 1 
                self.action.setData(Fila)
        return super(clase_buscar, self).eventFilter(source, event) 

    def generateMenu(self,pos):
        print("pos====",pos)  
        item = self.ui.tableWidget.itemAt(pos)
        if(item is not None):
            self.menu.exec_(self.ui.tableWidget.mapToGlobal(pos))

    def get_ui(self):
        return self.widget
        
    def cargar_tablas(self ):
            self.diccateg.clear()
            self.dicSecequip.clear()
            self.dicubifisica.clear()
            self.dicubiexacta.clear()
            self.dicestado.clear()

            self.diccateg = {'':'0'}
            self.dicSecequip = {'':'0'}
            self.dicubifisica = {'':'0'}
            self.dicubiexacta = {'':'0'}
            self.dicestado = {'':'0'}
            while (self.ui.comboBox.count() > 0):
                    self.ui.comboBox.removeItem(0)
            while (self.ui.comboBox_2.count() > 0):
                    self.ui.comboBox_2.removeItem(0)
            while (self.ui.comboBox_3.count() > 0):
                    self.ui.comboBox_3.removeItem(0)
            self.ui.lineEdit.setText('')              
            try:
                cursor = self.cnx.cursor()

                query = ("SELECT distinct products.ProductName from movedb.products order by ProductName")
                cursor.execute(query)
                records = cursor.fetchall()
                
                for row in records:
                        self.ui.comboBox.addItem(row[0])

                query = ("SELECT distinct UbicacionFisicaName FROM movedb.ubicacionfisica\
                        order by ubicacionfisica.UbicacionFisicaName asc")
                
                cursor.execute(query)
                records = cursor.fetchall()
                
                self.ui.comboBox_2.addItem('')
                for row in records:
                        self.ui.comboBox_2.addItem(row[0])

                
                query = ("SELECT distinct categories.CategoryName FROM movedb.categories\
                            order by categories.CategoryName asc")
                
                cursor.execute(query)
                records = cursor.fetchall()
                
                self.ui.comboBox_3.addItem('')
                for row in records:
                        self.ui.comboBox_3.addItem(row[0])

            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)
            else:
                cursor.close()

    def request(self):
                #header = self.ui.tableWidget.horizontalHeader()
                #i = 0
                Nombre = ''
                NumSerie = ''
                while (self.ui.tableWidget.rowCount() > 0):
                        self.ui.tableWidget.removeRow(0)
                try:
                    cursor = self.cnx.cursor()
                       
                    if(self.ui.comboBox.currentIndex() != 0):
                        Nombre = "ProductName LIKE '%"+ self.ui.comboBox.currentText() + "' "

                    if(self.ui.lineEdit.text() != '' ):
                        NumSerie = "SerialNumber Like '%"+ self.ui.lineEdit.text() + "' "
                        if(self.ui.comboBox.currentIndex() != 0 ):
                            NumSerie = "and "+ NumSerie


                    Nombre = self.ui.comboBox.currentText()
                    NumSerie = self.ui.lineEdit.text()
                    #Assy = self.ui.lineEdit_2.text()
                    coincidencia = ''
                    #SeccEquip = self.ui.comboBox_5.currentText()

                    reqSerie =  "products.SerialNumber Like '"+ NumSerie + "%' "
                    reqNombre = "products.ProductName Like concat('%' ,'"+ Nombre + "' ,'%') "
                    #reqAssy =   "products.Assy Like '" + Assy +  "%' "
                    #reqSecEquip = "secequipo.SecEquipoName Like'"+ SeccEquip +"' "


                    if(Nombre != ''):
                        coincidencia = reqNombre

                        if(NumSerie != ''):
                                coincidencia = coincidencia + "and " + reqSerie

                    '''if(Assy != '' ):
                                coincidencia = coincidencia + "and "+ reqAssy

                    if(SeccEquip != '' and SeccEquip != 'None'):
                                coincidencia = coincidencia + "and " + reqSecEquip'''

                     
                    query = "SELECT products.ProductID,\
                                    products.ProductName,\
                                    (select SUM(UnitsReceived-UnitsSold-UnitsShrinkage) from movedb.inventorytransactions as t where t.ProductID = products.ProductID),\
                                    estado.Estado,\
                                    products.Observaciones,\
                                    products.SerialNumber,\
                                    products.Assy,\
                                    products.ProductDescription,\
                                    categories.CategoryName,\
                                    ubicacionexacta.UbicacionExactaName,\
                                    ubicacionfisica.UbicacionFisicaName,\
                                    secequipo.SecEquipoName\
                                    FROM movedb.products\
                                    LEFT JOIN movedb.categories ON products.CategoryID = categories.CategoryID\
                                    Left join movedb.ubicacionexacta on products.UbicacionExacta = ubicacionexacta.UbicacionExactaID\
                                    Left join movedb.ubicacionfisica on products.UbicacionFisica = ubicacionfisica.UbicacionFisicaID\
                                    Left join movedb.estado			 on products.EstadoID = estado.EstadoID\
                                    left join movedb.secequipo       on products.SecEquipoID = secequipo.SecEquipoID\
                                    WHERE " + coincidencia + " ;" 

                    rows = cursor.execute(query)
                    data = cursor.fetchall()

                    for row in data:
                        add_table(convert(row), self.ui)
                            
                    
                    self.ui.tableWidget.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
                    self.ui.tableWidget.horizontalHeader().setSectionResizeMode(5,QHeaderView.Stretch)
                    self.ui.tableWidget.verticalHeader().resizeSections(QHeaderView.ResizeToContents)

                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                        print("Something is wrong with your user name or password")
                    elif err.errno == errorcode.ER_BAD_DB_ERROR:
                        print("Database does not exist")
                    else:
                        print(err)
                        QMessageBox.critical(self, 'Error al buscar el producto', str(err))
                else:
                    cursor.close()

def convert(in_data):
        def cvt(data):
            try:
                return ast.literal_eval(data)
            except Exception:
                return str(data)
        return tuple(map(cvt, in_data))

class BlobDelegate(QtWidgets.QStyledItemDelegate):
        def displayText(self, value, locale):
            if isinstance(value, QtCore.QByteArray):
                value = value.data().decode()
            return super(BlobDelegate, self).displayText(value, locale)
        
def add_table(columns, ui):
            rowPosition = ui.tableWidget.rowCount()
            ui.tableWidget.insertRow(rowPosition)
            '''
            ui.tableWidget.setItem(rowPosition,0, QtWidgets.QTableWidgetItem(str(columns[0]) ) )
            ui.tableWidget.setItem(rowPosition,1, QtWidgets.QTableWidgetItem(str(columns[1]) ) ) 
            ui.tableWidget.setItem(rowPosition,2, QtWidgets.QTableWidgetItem(str(columns[2]) ) )
            ui.tableWidget.setItem(rowPosition,3, QtWidgets.QTableWidgetItem(str(columns[3]) ) ) 
            ui.tableWidget.setItem(rowPosition,4, QtWidgets.QTableWidgetItem(str(columns[4]) ) )
            ui.tableWidget.setItem(rowPosition,5, QtWidgets.QTableWidgetItem(str(columns[5]) ) )  
            ui.tableWidget.setItem(rowPosition,6, QtWidgets.QTableWidgetItem(str(columns[6]) ) )  '''         
            ### todas las columnas
            for i, column in enumerate(columns):
                    ui.tableWidget.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(str(column)))
                    if(i == 2):
                        ui.tableWidget.item(rowPosition,i).setTextAlignment(QtCore.Qt.AlignCenter)
                        if(str(column) != 'None'):
                            if((int)(column) <= 0):
                                ui.tableWidget.item(rowPosition,i).setBackground(QColor(255,0,0))

                            

            