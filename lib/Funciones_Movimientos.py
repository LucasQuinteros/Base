from logging import error
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QHeaderView, QMenu, QWidget,QMessageBox
from qts.Ui_ventana_movimientos import Ui_Form
from lib.Item import item_Mov
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

        self.invocador = invocador
        self.cambiosenfila = ''
        self.Destino = ''
        self.Origen = ''
    
    def setparams(self,item : item_Mov):
    
        self.cnx = item.Cnx
        self.itemID = item.ID                      #ID
        self.Cargar_tablas()
        self.receiv = int(item.Urec)
        self.sold = int(item.Usold)
        self.shr =int(item.Ush)
        self.stock = int(item.Usto)+ self.receiv -self.sold
        
        self.ui.lineEdit.setText(item.Date)           #Date
        self.ui.lineEdit_2.setText(item.Descr)         #Desc
        self.ui.lineEdit_3.setText(item.Urec)         #R
        self.ui.lineEdit_4.setText(item.Usold)         #Sold
        self.ui.lineEdit_5.setText(item.Ush)         #Shr
        self.ui.lineEdit_7.setText(str(self.stock))         #Stock
        self.ui.lineEdit_6.setText(item.NumMov)        #NumMov
        self.Origen = item.Ori    #Origen
        self.Destino = item.Dest  #destino
        if(self.Destino != ''):
                    self.ui.comboBox_2.setCurrentText(self.Destino)
        if(self.Origen != ''):
                    self.ui.comboBox.setCurrentText(self.Origen)
        
        

        if(int(self.ui.lineEdit_7.text()) >= 0):
            self.ui.pushButton_2.setDisabled(0)
            
        self.ui.lineEdit_3.textChanged.connect(self.CalcularStock)
        self.ui.lineEdit_4.textChanged.connect(self.CalcularStock)
        self.ui.lineEdit_5.textChanged.connect(self.CalcularStock)
        
        
        
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
                self.ui.comboBox.addItem('')
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
                
