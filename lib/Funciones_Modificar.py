


from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QHeaderView, QMenu, QWidget,QMessageBox
from qts.Ui_ventana_modificar import Ui_Form
import mysql.connector
import ast
from mysql.connector import errorcode


class clase_modificar(QWidget):
    procCargar = QtCore.pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.widget = QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.widget)
        self.ui.pushButton_3.clicked.connect(self.Modificar)
        self.menu = QMenu()
        self.action = self.menu.addAction('Modificar')
        self.ui.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu) 
        self.ui.tableWidget.customContextMenuRequested.connect(self.generateMenu)
        self.ui.tableWidget.viewport().installEventFilter(self)
        self.ui.lineEdit.setDisabled(1)

        self.diccateg = {}
        self.dicSecequip = {}
        self.dicubifisica = {}
        self.dicubiexacta = {}
        self.dicestado = {}
        
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
                    if(j == 6):
                        self.ui.lineEdit.setText(message[j])
                    j = j+1
                i = filas
            i = i+1
        print(message)  

    def eventFilter(self,source,event):
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
                    if(i==6):
                        Fila.append(self.ui.lineEdit.text())
                    else:
                        Fila.append(self.ui.tableWidget.item(item.row(), i).text())
                    i = i + 1 
                self.action.setData(Fila)
        return super(clase_modificar, self).eventFilter(source, event) 

    def generateMenu(self,pos):
        print("pos====",pos)
        item = self.ui.tableWidget.itemAt(pos)
        if(item is not None):  
            self.menu.exec_(self.ui.tableWidget.mapToGlobal(pos))

    def Cargar_tablas(self):
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
        while (self.ui.comboBox_4.count() > 0):
                    self.ui.comboBox_4.removeItem(0)
        while (self.ui.comboBox_5.count() > 0):
                    self.ui.comboBox_5.removeItem(0)
        self.ui.lineEdit.setText('')         
        try:
                while (self.ui.tableWidget.rowCount() > 0):
                        self.ui.tableWidget.removeRow(0)
                cursor = self.cnx.cursor()

                query = ("SELECT distinct UbicacionFisicaID,UbicacionFisicaName FROM movedb.ubicacionfisica\
                        order by ubicacionfisica.UbicacionFisicaName asc")
                
                cursor.execute(query)
                records = cursor.fetchall()
                
                
                self.ui.comboBox.addItem('')
                for row in records:
                        self.dicubifisica.update( {str(row[1]) : str(row[0]) } )
                        self.ui.comboBox.addItem(row[1])
                
                
                query = ("SELECT distinct categories.CategoryID,categories.CategoryName FROM movedb.categories\
                            order by categories.CategoryName asc")
                
                cursor.execute(query)
                records = cursor.fetchall()
               

                self.ui.comboBox_4.addItem('')
                for row in records:
                        self.diccateg.update( {str(row[1]) : str(row[0]) })
                        self.ui.comboBox_4.addItem(row[1])

                query = ("SELECT distinct UbicacionExactaID,UbicacionExactaName FROM movedb.ubicacionexacta\
                            order by ubicacionexacta.UbicacionExactaName asc")
                
                cursor.execute(query)
                records = cursor.fetchall()
                

                self.ui.comboBox_5.addItem('')
                for row in records:
                        self.dicubiexacta.update( {str(row[1]) : str(row[0]) })
                        self.ui.comboBox_5.addItem(row[1])

                query = ("SELECT distinct EstadoID,Estado FROM movedb.estado\
                            order by estado.Estado asc")
                
                cursor.execute(query)
                records = cursor.fetchall()
                

                self.ui.comboBox_3.addItem('')
                for row in records:
                        self.dicestado.update( {str(row[1]) : str(row[0]) })
                        self.ui.comboBox_3.addItem(row[1])

                query = ("SELECT distinct SecEquipoID,SecEquipoName FROM movedb.secequipo\
                            order by secequipo.SecEquipoName asc")
                
                cursor.execute(query)
                records = cursor.fetchall()
                

                self.ui.comboBox_2.addItem('')
                for row in records:
                        self.dicSecequip.update( {str(row[1]) : str(row[0]) })
                        self.ui.comboBox_2.addItem(row[1])
                
                query = ("SELECT t1.TransactionID,\
                                t1.TransactionDate,\
                                t1.TransactionDescription,\
                                t1.UnitsReceived,\
                                t1.UnitsSold,\
                                t1.UnitsShrinkage,\
                                t1.UnitsStock,\
                                t1.OrigenID,\
                                t1.DestinoID,\
                                t1.NumberMov\
                                FROM movedb.inventorytransactions as t1\
                                left join movedb.destino on t1.DestinoID = destino.DestinoID\
                                left join movedb.origen on t1.OrigenID = origen.OrigenID\
                                where t1.ProductID = '"+str(self.itemID) +"'\
                                order by t1.TransactionID desc;")
                
                #query = "SELECT * FROM movedb.inventorytransactions where ProductID = '"+str(self.itemID) +"'"
                rows = cursor.execute(query)
                data = cursor.fetchall()

                for row in data:
                        add_table(convert(row), self.ui)

                self.ui.tableWidget.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
                #self.ui.tableWidget.horizontalHeader().setSectionResizeMode(4,QHeaderView.Stretch)
                self.ui.tableWidget.verticalHeader().resizeSections(QHeaderView.ResizeToContents)

        except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)
        else:
                cursor.close() 

    def setparams(self,item):
        
        
        self.cnx = item[0]
        self.itemID = item[1]                      #ID
        self.Cargar_tablas()

        self.ui.lineEdit_3.setText(item[2])        #Nombre
        self.ui.textEdit.setPlainText(item[5])          #Obsv
        self.ui.textEdit_2.setPlainText(item[8])    #descrip
        self.ui.comboBox_4.setCurrentText(item[9]) #Categoria
        self.ui.lineEdit_2.setText(item[6])        #Serie
        self.ui.comboBox_5.setCurrentText(item[10]) #Ubicacion exacta
        self.ui.comboBox.setCurrentText(item[11])   #Ubicacion Fisica
        self.ui.comboBox_2.setCurrentText(item[12]) #seccion equipo 11
        self.ui.comboBox_3.setCurrentText(item[4])   #Estado
        self.ui.lineEdit_4.setText(item[7])         # Assy
        self.ui.lineEdit.setText(item[3])          #Cantidad


    def Modificar(self):
            item = list()

            ID = self.itemID
            item.append((str)(self.itemID))

            Nombre = self.ui.lineEdit_3.text()
            item.append(Nombre)

            Cantidad = self.ui.lineEdit.text()
            item.append(Cantidad)

            estadoindex = self.dicestado[self.ui.comboBox_3.currentText()]
            item.append(self.ui.comboBox_3.currentText())

            Observacion = self.ui.textEdit.toPlainText()
            item.append(Observacion)

            Serie = self.ui.lineEdit_2.text()
            item.append(Serie)

            Assy = self.ui.lineEdit_4.text()
            item.append(Assy)

            descrip = self.ui.textEdit_2.toPlainText()
            item.append(descrip)

            catindex = self.diccateg[self.ui.comboBox_4.currentText()]
            item.append(self.ui.comboBox_4.currentText())
            
            
            ubiexacindex = self.dicubiexacta[self.ui.comboBox_5.currentText()]          
            item.append(self.ui.comboBox_5.currentText())
            
            ubifisindex = self.dicubifisica[ self.ui.comboBox.currentText() ]
            print(ubifisindex)

            item.append(self.ui.comboBox.currentText())
            

            Secequipindex = self.dicSecequip[self.ui.comboBox_2.currentText()]
            item.append(self.ui.comboBox_2.currentText())
            
            print(item)

            self.procCargar.emit(item)
            try:

                cursor = self.cnx.cursor()
                
                query = "UPDATE movedb.products\
                        SET products.ProductName = '" + Nombre +"'\
                                ,products.Observaciones = '" + Observacion +"'\
                                ,products.ProductDescription = '"+ descrip +"'\
                                ,products.EstadoID = '"+ estadoindex +"'\
                                ,products.SecEquipoID = '"+ Secequipindex +"'\
                                ,products.CategoryID = '" + catindex +"'\
                                ,products.SerialNumber = '" + Serie +"'\
                                ,products.Assy = '" + Assy +"'\
                                ,products.ubicacionexacta = '" + ubiexacindex +"'\
                                ,products.ubicacionfisica = '" + ubifisindex +"'\
                        WHERE  products.ProductID ='" + ID + "';"


                
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
            '''
            while (self.ui.comboBox.count() > 0):
                    self.ui.comboBox.removeItem(0)
            self.cargar_tablas()
            '''

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
            ### todas las columnas
            for i, column in enumerate(columns):
                    ui.tableWidget.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(str(column)))