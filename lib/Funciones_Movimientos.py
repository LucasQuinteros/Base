from logging import error
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QHeaderView, QMenu, QWidget,QMessageBox
from qts.Ui_ventana_movimientos import Ui_Form
import mysql.connector
import ast
from mysql.connector import errorcode


class clase_movimientos(QWidget):
    procCargar = QtCore.pyqtSignal(list)
    procIngresos = QtCore.pyqtSignal(list)

    def __init__(self,invocador):
        super().__init__()
        self.widget = QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.widget)
        self.ui.pushButton_2.clicked.connect(self.Modificar)
        self.ui.lineEdit_3.textEdited.connect(self.CalcularStock)
        self.ui.lineEdit_4.textEdited.connect(self.CalcularStock)
        self.ui.lineEdit_5.textEdited.connect(self.CalcularStock)
        self.invocador = invocador
        self.cambiosenfila = ''

    def setparams(self,item):
    
        self.cnx = item[0]
        self.itemID = item[1]                      #ID
        self.Cargar_tablas()
        
        self.ui.lineEdit.setText(item[2])           #Date
        self.ui.lineEdit_2.setText(item[3])         #Desc
        self.ui.lineEdit_3.setText(item[4])         #R
        self.ui.lineEdit_4.setText(item[5])         #Sold
        self.ui.lineEdit_5.setText(item[6])         #Shr
        self.ui.lineEdit_7.setText(item[7])         #Stock
        self.ui.lineEdit_6.setText(item[10])        #NumMov
        self.ui.comboBox.setCurrentText(item[8])    #Origen
        self.ui.comboBox_2.setCurrentText(item[9])  #destino
        
        
        self.receiv = int(self.ui.lineEdit_3.text())
        self.sold = int(self.ui.lineEdit_4.text())
        self.shr =int(self.ui.lineEdit_5.text())
        self.stock = int(self.ui.lineEdit_7.text())
        if(int(self.ui.lineEdit_7.text()) >= 0):
            self.ui.pushButton_2.setDisabled(0)

    def CalcularStock(self):
        if( (self.ui.lineEdit_3.text() == '') | (self.ui.lineEdit_4.text() == '') | (self.ui.lineEdit_5.text() == '')):
            self.ui.pushButton_2.setDisabled(1)
        else:
            self.ui.pushButton_2.setDisabled(0)
            deltaRec = int(self.ui.lineEdit_3.text()) - self.receiv
            deltaSold = int(self.ui.lineEdit_4.text()) - self.sold
            deltaShr = int(self.ui.lineEdit_5.text()) - self.shr
            Unitstock = self.stock + deltaRec - deltaSold - deltaShr
            
            self.ui.lineEdit_7.setText(str(Unitstock))
            if(Unitstock < 0):
                    self.ui.pushButton_2.setDisabled(1)
            else:
                    self.ui.pushButton_2.setDisabled(0)
        '''
        if (self.ui.lineEdit_3.text() == ''):
            self.ui.lineEdit_3.setText('0')
        if (self.ui.lineEdit_4.text() == ''):
            self.ui.lineEdit_4.setText('0')
        if (self.ui.lineEdit_5.text() == ''):
            self.ui.lineEdit_5.setText('0')
        '''

    def Cargar_tablas(self ):
            while (self.ui.comboBox.count() > 0):
                    self.ui.comboBox.removeItem(0)
            while (self.ui.comboBox_2.count() > 0):
                    self.ui.comboBox_2.removeItem(0)

            #self.ui.lineEdit.setText('')              
            try:
                cursor = self.cnx.cursor()

                query = ("SELECT OrigenName FROM movedb.origen order by OrigenID;")
                cursor.execute(query)
                records = cursor.fetchall()
                print("Total number of rows in table: ", cursor.rowcount)
                for row in records:
                        self.ui.comboBox.addItem(row[0])

                query = ("SELECT DestinoName FROM movedb.destino order by DestinoID;")
                
                cursor.execute(query)
                records = cursor.fetchall()
                print("Total number of rows in table: ", cursor.rowcount)
                self.ui.comboBox_2.addItem('')
                for row in records:
                        self.ui.comboBox_2.addItem(row[0])

            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)
            else:
                cursor.close()

    def Modificar(self):
            item = list()

            ID = self.itemID
            item.append((str)(self.itemID))

            Date = self.ui.lineEdit.text()
            item.append(Date)

            descrip = self.ui.lineEdit_2.text()
            item.append(descrip)

            Urec = self.ui.lineEdit_3.text()
            item.append(Urec)

            Usold = self.ui.lineEdit_4.text()
            item.append(Usold)

            UShink = self.ui.lineEdit_5.text()
            item.append(UShink)

            UStock = self.ui.lineEdit_7.text()
            item.append(UStock)

            Origen = (str)(self.ui.comboBox.currentText())
            item.append(self.ui.comboBox.currentText())

            destino = (str)(self.ui.comboBox_2.currentText())
            item.append(self.ui.comboBox_2.currentText())

            NumMov = self.ui.lineEdit_6.text()
            item.append(NumMov)
            print(item)

            if(self.invocador == 'Pag_busqueda'):
                self.procCargar.emit(item)

                
                try:

                    cursor = self.cnx.cursor()

                    query = "UPDATE movedb.inventorytransactions\
                            SET TransactionDate = '" + Date +"'\
                                    ,TransactionDescription = '" + descrip +"'\
                                    ,UnitsReceived = '"+ Urec +"'\
                                    ,UnitsSold = '"+ Usold +"'\
                                    ,UnitsShrinkage = '"+ UShink +"'\
                                    ,UnitsStock= '"+ UStock +"'\
                                    ,OrigenID = '" + Origen +"'\
                                    ,DestinoID = '" + destino +"'\
                                    ,NumberMov = '" + NumMov +"'\
                            WHERE  TransactionID ='" + ID + "';"

                    rows = cursor.execute(query)
                    data = cursor.fetchall()
                
                except mysql.connector.Error as err:
                        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                            print("Something is wrong with your user name or password")
                        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                            print("Database does not exist")
                        else:
                            print(err)
                            QMessageBox.critical(self, 'Error al actualizar en base', err)
                else:
                        cursor.close()
                        QMessageBox.information(self, 'Info', 'Carga Exitosa')
            
            elif(self.invocador == 'Pag_ingresos'):
                self.procIngresos.emit(item)
                self.widget.close()
                
