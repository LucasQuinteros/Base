from typing import Text
from PyQt5.QtGui import QColor
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QDialog, QHeaderView, QMenu, QMessageBox, QTextEdit, QWidget,QComboBox
from lib.Funciones_Movimientos import clase_movimientos
from lib.Item import *
from qts.Ui_ventana_ingresos import Ui_Form
from qts.Ui_ventana_coincidencias import Ui_Dialog
import mysql.connector
import ast
from mysql.connector import errorcode
from datetime import datetime

class clase_Coincidencias(QWidget):
        procCargar = QtCore.pyqtSignal(list)
    
        def __init__(self):
                super().__init__()
                self.dialog = QDialog()
                self.dialog.setMinimumSize(1366,600)
                self.ui = Ui_Dialog()
                self.ui.setupUi(self.dialog)
                self.data = ''
                self.ui.buttonBox.accepted.connect(self.Confirmado)
                self.ui.buttonBox.rejected.connect(self.close)
                self.ui.tableWidget.itemClicked.connect(self.handleclickitem)
                self.seleccion = list()

        #muestra los datos obtenidos del query
        def cargar_data(self, data, cantidad = ''):
                while (self.ui.tableWidget.rowCount() > 0):
                        self.ui.tableWidget.removeRow(0)
                for row in data:
                        fila = convert(row)
                        if(cantidad != ''):
                            if(int(fila[2]) >= int(cantidad)): 
                                add_table(fila, self.ui)
                                
                        else:
                            add_table(fila,self.ui)
                             
                self.ui.tableWidget.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
                #self.ui.tableWidget.horizontalHeader().setSectionResizeMode(5,QHeaderView.Stretch)
                self.ui.tableWidget.verticalHeader().resizeSections(QHeaderView.ResizeToContents)

        def Confirmado(self):
                self.procCargar.emit(self.seleccion)
                self.seleccion.clear()

        def handleclickitem(self,item):
                item2 = self.ui.tableWidget.item(item.row(),0)
                tup = ()
                aux = list()
                if item2.checkState() == QtCore.Qt.Checked:
                        item2.setCheckState(QtCore.Qt.Unchecked)
                        for i in range(self.ui.tableWidget.columnCount()):
                                columns = self.ui.tableWidget.item(item.row(),i).text()
                                aux.append(columns)

                        tup = tuple(aux)        
                        self.seleccion.remove(tup)

                elif item2.checkState() == QtCore.Qt.Unchecked:
                        item2.setCheckState(QtCore.Qt.Checked) 
                        for i in range(self.ui.tableWidget.columnCount()):
                                columns = self.ui.tableWidget.item(item.row(),i).text()
                                aux.append(columns)
                        tup = tuple(aux)                        
                        self.seleccion.append(tup)
                                

class clase_ingresos(QWidget):
        procCargar = QtCore.pyqtSignal(list)
    
        def __init__(self,conn):
                super().__init__()
                self.widget = QWidget()
                self.ui = Ui_Form()
                self.ui.setupUi(self.widget)
                self.menu = QMenu()
                self.menu_2 = QMenu()
                self.cambios = list()
                self.conn = conn
                self.Ingresos = list()
                self.action = self.menu.addAction("Eliminar")
                self.action_2 = self.menu_2.addAction("Eliminar")
                
                self.seleccion = int()
                self.menu.triggered.connect(self.Eliminaritem)
                self.menu_2.triggered.connect(self.EliminaritemMov)
                self.ventana = clase_Coincidencias()
                self.ventana.procCargar.connect(self.Cargar_seleccion)
                
                self.ventana_movi = clase_movimientos('Pag_ingresos')
                self.ventana_movi.procIngresos.connect(self.proc_cargar)
                self.ventana_movi.ui.pushButton.clicked.connect(self.ventana_movi.widget.close)

                self.ui.comboBox_2.currentTextChanged.connect(lambda: self.handlercambio('Cat'))
                self.ui.comboBox_3.currentTextChanged.connect(lambda: self.handlercambio('UbiFis'))
                self.ui.comboBox_4.currentTextChanged.connect(lambda: self.handlercambio('UbiExac'))
                self.ui.comboBox_5.currentTextChanged.connect(lambda: self.handlercambio('SeccEquip'))
                self.ui.comboBox_6.currentTextChanged.connect(lambda: self.handlercambio('Estado'))
                self.ui.lineEdit.textChanged.connect(lambda: self.handlercambio('Nserie'))
                self.ui.lineEdit_2.textChanged.connect(lambda: self.handlercambio('PartNum'))
                
                self.ui.pushButton.clicked.connect(self.Actualizar_en_base)
                self.ui.pushButton_2.clicked.connect(self.agregar_nuevoitem)
                self.ui.pushButton_4.clicked.connect(self.Limpiar_selecciones)
                self.ui.pushButton_5.clicked.connect(lambda: self.Traer_Prod(self.ui.comboBox.currentText() ) )
                #self.ui.pushButton_3.clicked.connect(lambda: self.Chequear_serie(self.ui.lineEdit.text() )  )
                self.ui.pushButton_6.clicked.connect(self.agregar_movimiento)
                self.ui.pushButton_7.clicked.connect(self.agregar_movimiento)
                self.ui.pushButton_8.clicked.connect(self.agregar_movimiento)
                

                Multiline = BlobDelegate()
                Multiline.Signalresize.connect(self.proc_reajustar)
                self.ui.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu) 
                self.ui.tableWidget.customContextMenuRequested.connect(self.generateMenu)
                self.ui.tableWidget.viewport().installEventFilter(self)
                
                self.ui.tableWidget.itemChanged.connect(self.changed)
                self.ui.tableWidget.setItemDelegateForColumn(4, Multiline)
                
                
                
                self.ui.tableWidget_2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                self.ui.tableWidget_2.customContextMenuRequested.connect(self.generateMenuMov)
                self.ui.tableWidget_2.viewport().installEventFilter(self)
                

                self.productpos = {'ProductID':'0','ProductName':'1','Cantidad':'2','Estado':'3','Observacion':'4','Nserie':'5',
                                   'PartNum':'6','Descrip':'7','Cat':'8','UbiExac':'9','UbiFis':'10','SeccEquip':'11'}
                self.diccateg =    {'':'0','None':'None'}
                self.dicSecequip = {'':'0','None':'None'}
                self.dicubifisica = {'':'0','None':'None'}
                self.dicubiexacta = {'':'0','None':'None'}
                self.dicestado =    {'':'0','None':'None'}

        #Obtiene el nuevo movimiento agregado
        @QtCore.pyqtSlot(list)
        def proc_cargar(self,message):
                rowPosition = self.ui.tableWidget_2.rowCount()


                if ( self.ui.tableWidget.selectedItems() != []):
                        fila = self.ui.tableWidget.selectedItems()[0].row()
                        ID = self.ui.tableWidget.item(fila,0).text()
                        for prod in self.Ingresos:
                                
                                if( str(prod.ProductID) == ID ):
                                        index = self.Ingresos.index(prod)

                        Producto = self.Ingresos[index]
                        Mov = item_Mov(message)
                        Producto.Movimientos.append(Mov)
                        self.Agregar_tabMov(Mov.__dict__)
                        aux = QtWidgets.QTableWidgetItem(str(Mov.Usto))
                        self.ui.tableWidget.setItem(fila,int(self.productpos['Cantidad']),aux)
                        if(Mov.Usto == '0'):
                                self.ui.tableWidget.item(fila,int(self.productpos['Cantidad'])).setBackground(QColor(255,0,0))
                        
                ### todas las columnas
                '''
                for i, column in enumerate(message):
                        item = QtWidgets.QTableWidgetItem(str(column))
                        item = self.ui.tableWidget_2.setItem(0, i, item)
                '''
        
        def Actualizar_Conector(self,conn):
                self.conn = conn

        @QtCore.pyqtSlot()
        def proc_reajustar(self):
                self.ui.tableWidget.verticalHeader().resizeSections(QHeaderView.ResizeToContents)

        def Limpiar_selecciones(self):
                if(self.ui.tableWidget.selectedItems() !=[]):
                        self.ui.tableWidget.clearSelection()
                while (self.ui.tableWidget_2.rowCount() > 0):
                        self.ui.tableWidget_2.removeRow(0)
                self.ui.comboBox.setCurrentIndex(0)
                self.ui.comboBox_2.setCurrentIndex(0)
                self.ui.comboBox_3.setCurrentIndex(0)
                self.ui.comboBox_4.setCurrentIndex(0)
                self.ui.comboBox_5.setCurrentIndex(0)
                self.ui.comboBox_6.setCurrentIndex(0)
                self.ui.lineEdit.setText('')
                self.ui.lineEdit_2.setText('')
                
        def changed(self,item):
                ID = self.ui.tableWidget.item(item.row(),0).text()
                for P in self.Ingresos:
                        if (str(P.ProductID) == ID):
                                aux = P

                                if(item.column() == int(self.productpos['Observacion'])):
                                                aux.__dict__['Observacion'] = item.text()
                                                

                                if(item.column() == int(self.productpos['Nserie'])):
                                                aux.__dict__['Nserie'] = item.text()
                                                
                                if(item.column() == int(self.productpos['PartNum'])):
                                                aux.__dict__['PartNum'] = item.text()
                                
                                if(item.column() == int(self.productpos['Descrip'])):
                                                aux.__dict__['Descrip'] = item.text()

                                if(item.column() == int(self.productpos['ProductName'])):
                                                aux.__dict__['ProductName'] = item.text()
                                
       #rutina boton agregar movimiento
        def agregar_movimiento(self):
                ExistenMovs = False
                if ( self.ui.tableWidget.selectedItems() != []):
                        Date = datetime.now()
                        fila = self.ui.tableWidget.selectedItems()[0].row()
                        ID = self.ui.tableWidget.item(fila,0).text()
                        index = 0

                        for prod in self.Ingresos:
                                print(prod.ProductID, ID)
                                if( str(prod.ProductID) == ID ):
                                        index = self.Ingresos.index(prod)

                        Producto = self.Ingresos[index]
                        movNuevo = item_Mov( self.cnx)
                        table = self.ui.tableWidget_2
                        Fila = list()
                        Fila.append(self.cnx)
                        if( self.ui.tableWidget_2.rowCount() > 0 ):
                                ExistenMovs = True
                        
                        for m in Producto.Movimientos:
                                aux = str(m.ID)
                                if(aux[0] == 'N'):
                                        if(index < int(aux[1:]) ):
                                                index = int(aux[1:])
                        
                        #Agrego a mov
                        if ( ExistenMovs is True ):
                                movNuevo.Date = Date.strftime("%Y-%m-%d %H:%M:%S")
                                movNuevo.ID = 'N'+ str(index+1)
                                movNuevo.Urec = '0'
                                movNuevo.Usold = '0'
                                movNuevo.Ush = '0'
                                movNuevo.Usto = self.ui.tableWidget.item(fila,2).text()
                                
                                '''
                                for i in range(self.ui.tableWidget_2.columnCount() ):
                                        Fila.append(self.ui.tableWidget_2.item(0, i).text())
                                Fila[1] = 'N'+ str(index+1)
                                Fila[2] = Date.strftime("%Y-%m-%d %H:%M:%S")
                                Fila[4] = '0'
                                Fila[5] = '0'
                                Fila[6] = '0'
                                Fila[10] = ''
                                if(self.sender() == self.ui.pushButton_8):
                                        Fila[8] = 'Stock'
                                '''
                        #Comienzo nueva listmov
                        elif(  ExistenMovs is False):
                                movNuevo.Date = Date.strftime("%Y-%m-%d %H:%M:%S")
                                movNuevo.ID = 'N1'
                                movNuevo.Urec = '0'
                                movNuevo.Usold = '0'
                                movNuevo.Ush = '0'
                                movNuevo.Usto = '0'
                                
                                '''
                                for i in range(self.ui.tableWidget_2.columnCount() ):
                                        Fila.append('0')
                                Fila[1] = 'N1'
                                Fila[2] = Date.strftime("%Y-%m-%d %H:%M:%S")
                                '''
                        if(self.sender() == self.ui.pushButton_7):     
                                movNuevo.Ori = 'Stock'
                                movNuevo.Descr = 'Egreso'
                                movNuevo.Usold = '1'
                        if(self.sender() == self.ui.pushButton_8):  
                                movNuevo.Descr = 'Ingreso'      
                                movNuevo.Urec = '1'
                                movNuevo.Ori = 'Stock'
                                movNuevo.Dest = 'Stock'
                                
                        
                        self.ventana_movi.setparams(movNuevo)
                        self.ventana_movi.widget.show()   
        
        def agregar_nuevoitem(self):
                item = list()
                lastindex = ''
                index = 0
                for pro in self.Ingresos:
                        aux = str(pro.ProductID)
                        if(aux[0] == 'N'):
                                if(index < int(aux[1:])):
                                        index = int(aux[1:])
                                        

                item.append('N'+ str(index + 1 ) )          #ID null
                item.append(self.ui.comboBox.currentText()) #Nombre
                item.append('0') #Cantidad
                item.append(self.ui.comboBox_6.currentText()) #Estado
                item.append('') #Observacion
                item.append(self.ui.lineEdit.text()) #Nserie
                item.append(self.ui.lineEdit_2.text()) #assy
                item.append('') #descr
                item.append(self.ui.comboBox_2.currentText()) #cat
                item.append(self.ui.comboBox_4.currentText()) #ubiexa
                item.append(self.ui.comboBox_3.currentText()) #ubifis
                item.append(self.ui.comboBox_5.currentText()) #SeccEqu
                producto = item_Prod(item)
                self.Ingresos.append(producto)
                self.Agregar_tabIngre(producto.__dict__)
              
        def handlercambio(self, key):


                if ( self.ui.tableWidget.selectedItems() != []):
                        fila = self.seleccion
                        print('handlercambio:' + str(fila))
                        ID = self.ui.tableWidget.item(fila,int(self.productpos['ProductID'])).text()
                        #self.ui.tableWidget.selectRow(fila)
                        contenido = ''
                        existe = bool(False)
                        aux = ''
                        
                                        
                        
                        if(key == 'Cat'):
                                contenido = self.ui.comboBox_2.currentText()
                                item = self.ui.tableWidget.item(fila,int(self.productpos[key]))
                                if(self.ui.comboBox_2.findText(contenido) >= 0):
                                        existe = True
                        elif(key == 'Estado' ):
                                contenido = self.ui.comboBox_6.currentText()
                                item = self.ui.tableWidget.item(fila,int(self.productpos[key]))
                                if(self.ui.comboBox_6.findText(contenido) >= 0):
                                        existe = True
                        elif(key == 'Nserie'):
                                contenido = self.ui.lineEdit.text()
                                item = self.ui.tableWidget.item(fila,int(self.productpos[key]))
                                existe = True
                        elif(key == 'PartNum'):
                                contenido = self.ui.lineEdit_2.text()
                                item = self.ui.tableWidget.item(fila,int(self.productpos[key]))
                                existe = True
                        elif(key == 'UbiFis'):
                                contenido = self.ui.comboBox_3.currentText()
                                item = self.ui.tableWidget.item(fila,int(self.productpos[key]))
                                if(self.ui.comboBox_3.findText(contenido) >= 0):
                                        existe = True
                        elif(key == 'UbiExac'):
                                contenido = self.ui.comboBox_4.currentText()
                                item = self.ui.tableWidget.item(fila,int(self.productpos[key]))
                                if(self.ui.comboBox_4.findText(contenido) >= 0):
                                        existe = True
                        elif(key == 'SeccEquip'):
                                contenido = self.ui.comboBox_5.currentText()
                                item = self.ui.tableWidget.item(fila,int(self.productpos[key]))
                                if(self.ui.comboBox_5.findText(contenido) >= 0):
                                        existe = True
                        
                        
                        if( contenido != item.text() and existe is True ):
                                item.setText(contenido)
                                for P in self.Ingresos:
                                        if (str(P.ProductID) == ID):
                                                P.__dict__[key] = contenido
                                                print(P.__dict__[key])
                

                                
        def eventFilter(self,source,event):
                
                if(event.type() == QtCore.QEvent.MouseButtonPress and
                        event.buttons() == QtCore.Qt.LeftButton and
                                source is self.ui.tableWidget.viewport()):

                        item = self.ui.tableWidget.itemAt(event.pos())
                        
                        if item is not None:
                                #self.ui.tableWidget.selectRow(item.row())
                                if(self.ui.tableWidget.item(item.row(),2).text() == '0' ):
                                        self.ui.pushButton_7.setDisabled(1)
                                else:
                                        self.ui.pushButton_7.setDisabled(0)
                                self.Cargar_movimientos(item)
                        if item is None:
                                self.ui.pushButton_7.setDisabled(0)
                                while (self.ui.tableWidget_2.rowCount() > 0):
                                        self.ui.tableWidget_2.removeRow(0)
                                
                
                if(event.type() == QtCore.QEvent.MouseButtonPress and
                        event.buttons() == QtCore.Qt.RightButton and
                                source is self.ui.tableWidget.viewport()):

                        item = self.ui.tableWidget.itemAt(event.pos())
                        
                        if item is not None:  
                                print('Table Item:', item.row(), item.column() )
                                
                                #self.ui.tableWidget.removeRow(item.row())
                                #self.ui.tableWidget_2.clear()
                                self.action.setData(item)
                        

                if(event.type() == QtCore.QEvent.MouseButtonPress and
                        event.buttons() == QtCore.Qt.RightButton and
                                source is self.ui.tableWidget_2.viewport()):

                        item = self.ui.tableWidget.itemAt(event.pos())
                        
                        if item is not None:  
                                print('Table Item:', item.row(), item.column() )
                                self.action_2.setData(item)
                
                return super(clase_ingresos, self).eventFilter(source, event) 

        def generateMenuMov(self,pos):
                item = self.ui.tableWidget_2.itemAt(pos)
                if(item is not None):
                        self.menu_2.exec_(self.ui.tableWidget_2.mapToGlobal(pos))        

        def generateMenu(self,pos):
                item = self.ui.tableWidget.itemAt(pos)
                if(item is not None):
                        self.menu.exec_(self.ui.tableWidget.mapToGlobal(pos))
        
        def EliminaritemMov(self,arg):
                item = arg.data()
                #itemID = self.ui.tableWidget_2.item(item.row(),0).text()

                if ( self.ui.tableWidget.selectedItems() != []):
                        fila = self.ui.tableWidget.selectedItems()[0].row()
                        ID = self.ui.tableWidget.item(fila,0).text()
                        
                        for prod in self.Ingresos:
                                print(prod.ProductID, ID)
                                if( str(prod.ProductID) == ID ):
                                        index = self.Ingresos.index(prod)
                Producto = self.Ingresos[index]

                Producto.Movimientos.pop()
                if(self.ui.tableWidget_2.rowCount() == 1 ):
                        aux = QtWidgets.QTableWidgetItem('0')
                        self.ui.tableWidget.setItem(fila,int(self.productpos['Cantidad']), aux)
                        self.ui.tableWidget.item(fila,int(self.productpos['Cantidad'])).setBackground(QColor(255,0,0))
                else:   
                        cantidad = self.ui.tableWidget_2.item(1, 6 ).text()
                        aux = QtWidgets.QTableWidgetItem(cantidad)
                        self.ui.tableWidget.setItem(fila,int( self.productpos['Cantidad']), aux)
                        if(cantidad == '0'):
                                self.ui.tableWidget.item(fila,int(self.productpos['Cantidad'])).setBackground(QColor(255,0,0))              
                
                self.ui.tableWidget_2.removeRow(0)

                for mov in Producto.Movimientos:
                        print(mov.__dict__)

        def Eliminaritem(self,arg):
                fila = arg.data()
                itemID = self.ui.tableWidget.item(fila.row(),0).text()
                
                for prod in self.Ingresos:
                        print(prod.ProductID, itemID)
                        if( str(prod.ProductID) == itemID ):
                                index = self.Ingresos.index(prod)

                Producto = self.Ingresos[index]
                self.Ingresos.remove(Producto)
                print('\n')
                for prod in self.Ingresos:
                        print(prod.__dict__)
                self.ui.tableWidget.removeRow(fila.row())
                while (self.ui.tableWidget_2.rowCount() > 0):
                        self.ui.tableWidget_2.removeRow(0)

        def Chequear_serie(self,Serie):
                
                NumSerie = self.ui.lineEdit.text()
                Assy = self.ui.lineEdit_2.text()
                coincidencia = ''
                reqSerie = "products.SerialNumber Like '"+ self.ui.lineEdit.text() + "%' "
                reqAssy = "products.Assy Like '" + self.ui.lineEdit_2.text()+  "%' "

                if((NumSerie == '' and Assy == '') == False):
                        try:
                                cursor = self.cnx.cursor()
                                

                                if(NumSerie == '' and Assy != ''):
                                        coincidencia = reqAssy

                                elif(NumSerie != '' and Assy == ''):
                                        coincidencia = reqSerie

                                elif(NumSerie != '' and Assy != '' ):
                                        coincidencia = reqSerie +"or "+ reqAssy
                                
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
                                        WHERE "+ coincidencia +";" 
                                        
                                
                                rows = cursor.execute(query)
                                data = cursor.fetchall()
                                

                                filas = self.ui.tableWidget.rowCount()
                                agregar = True
                                if(len(data)> 1):
                                        #self.Mostrar_coincidencias(data)
                                        self.ventana.cargar_data(data)
                                        self.ventana.dialog.show()
                                else:   
                                        for row in data:
                                                columns = convert(row)
                                                if (filas == 0):
                                                        agregar = True            
                                                else:   
                                                        for rows in range(filas):
                                                                if(columns[0] == self.ui.tableWidget.item(rows,0).text() ):
                                                                        agregar = False
                                                if(agregar):
                                                        add_table(columns, self.ui)

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
        
        ### Busca y Carga en tabla los movimientos de un item seleccionado con click
        def Cargar_movimientos(self,item):
                
                self.seleccion = item.row()
                itemID = self.ui.tableWidget.item(item.row(),0).text()
                try:
                        for prod in self.Ingresos:
                                if( str(prod.ProductID) == itemID ):
                                        index = self.Ingresos.index(prod)
                        
                        Producto = self.Ingresos[index]
                        #Nombre
                        self.ui.comboBox.setCurrentText(self.ui.tableWidget.item(item.row(),1).text())
                        #categoria
                        self.ui.comboBox_2.setCurrentText(self.ui.tableWidget.item(item.row(),8).text())
                        #ubifis
                        self.ui.comboBox_3.setCurrentText(self.ui.tableWidget.item(item.row(),10).text())
                        #ubiExac
                        self.ui.comboBox_4.setCurrentText(self.ui.tableWidget.item(item.row(),9).text())
                        #SeccEqui
                        self.ui.comboBox_5.setCurrentText(self.ui.tableWidget.item(item.row(),11).text())
                        #Estad
                        self.ui.comboBox_6.setCurrentText(self.ui.tableWidget.item(item.row(),3).text())
                        #Serie
                        self.ui.lineEdit.setText(self.ui.tableWidget.item(item.row(),5).text())
                        #Assy
                        self.ui.lineEdit_2.setText(self.ui.tableWidget.item(item.row(),6).text())
                        while (self.ui.tableWidget_2.rowCount() > 0):
                                        self.ui.tableWidget_2.removeRow(0)
                        
                        for Mov in Producto.Movimientos:
                                
                                self.Agregar_tabMov(Mov.__dict__)
                        
                except:
                        while (self.ui.tableWidget_2.rowCount() > 0):
                                        self.ui.tableWidget_2.removeRow(0)

                self.ui.tableWidget_2.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
                #self.ui.tableWidget.horizontalHeader().setSectionResizeMode(4,QHeaderView.Stretch)
                self.ui.tableWidget_2.verticalHeader().resizeSections(QHeaderView.ResizeToContents)
                
        #Carga la seleccion hecha en ventana y la agrega a la lista ingresos
        #Lo muestra en tabla
        #Busca los movimientos del producto          
        def Cargar_seleccion(self,data):
                filas = self.ui.tableWidget.rowCount()
                agregar = True
                for row in data:
                        columns = convert(row)

                        if (filas == 0):
                                agregar = True            
                        else:   
                                for rows in range(filas):

                                        if(str(columns[0]) == self.ui.tableWidget.item(rows,0).text() ):
                                                agregar = False
                        if(agregar):
                                Producto = item_Prod(columns)
                                self.Traer_Mov(Producto)
                                self.Ingresos.append(Producto)              
                                self.Agregar_tabIngre(Producto.__dict__)
                                #add_table(columns, self.ui)
                        self.ui.tableWidget.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
                        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(4,QHeaderView.Stretch)
                        self.ui.tableWidget.verticalHeader().resizeSections(QHeaderView.ResizeToContents)                
                
        def Cargar_tablas(self):
                self.Limpiar_selecciones()
                
                self.diccateg.clear()
                self.dicSecequip.clear()
                self.dicubifisica.clear()
                self.dicubiexacta.clear()
                self.dicestado.clear()

                self.diccateg =    {'':'0','None':'0'}
                self.dicSecequip = {'':'0','None':'0'}
                self.dicubifisica = {'':'0','None':'0'}
                self.dicubiexacta = {'':'0','None':'0'}
                self.dicestado =    {'':'0','None':'0'}
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
                while (self.ui.comboBox_6.count() > 0):
                        self.ui.comboBox_6.removeItem(0)
                while (self.ui.comboBox_8.count() > 0):
                        self.ui.comboBox_7.removeItem(0)
                while (self.ui.comboBox_8.count() > 0):
                        self.ui.comboBox_8.removeItem(0)
                
                
                self.ui.lineEdit.setText('')              
                try:
                        self.cnx = mysql.connector.connect(user=self.conn['user'], 
                                                        password=self.conn['password'],
                                                        host=self.conn['host'],
                                                        database=self.conn['database'])
                        cursor = self.cnx.cursor()

                        query = ("SELECT distinct products.ProductName from movedb.products order by ProductName")
                        cursor.execute(query)
                        records = cursor.fetchall()
                        
                        for row in records:
                                self.ui.comboBox.addItem(row[0])
                
                        query = ("SELECT distinct categories.CategoryID,categories.CategoryName FROM movedb.categories\
                                order by categories.CategoryID asc")
                        
                        cursor.execute(query)
                        records = cursor.fetchall()
                        
                        self.ui.comboBox_2.addItem('')
                        for row in records:
                                self.diccateg.update( {str(row[1]) : str(row[0]) })
                                self.ui.comboBox_2.addItem(row[1])

                        query = ("SELECT distinct UbicacionFisicaID,UbicacionFisicaName FROM movedb.ubicacionfisica\
                                order by ubicacionfisica.UbicacionFisicaName asc")
                        
                        cursor.execute(query)
                        records = cursor.fetchall()
                        
                        self.ui.comboBox_3.addItem('')
                        for row in records:
                                self.dicubifisica.update( {str(row[1]) : str(row[0]) } )
                                self.ui.comboBox_3.addItem(row[1])

                        query = ("SELECT distinct UbicacionExactaID,UbicacionExactaName,Objeto,Numero,Puerta,Seccion,Estante FROM movedb.ubicacionexacta\
                                order by ubicacionexacta.UbicacionExactaName asc")
                        
                        cursor.execute(query)
                        records = cursor.fetchall()
                        
                        
                        self.ui.comboBox_4.addItem('')
                        self.ui.comboBox_7.addItem('')
                        self.ui.comboBox_8.addItem('')
                        for row in records:
                                self.dicubiexacta.update( {str(row[1]) : str(row[0]) })
                                self.ui.comboBox_4.addItem(row[1])
                                self.Interprete2(row)

                        query = ("SELECT distinct SecEquipoID,SecEquipoName FROM movedb.secequipo\
                                order by secequipo.SecEquipoID asc")
                        
                        cursor.execute(query)
                        records = cursor.fetchall()
                        
                        self.ui.comboBox_5.addItem('')
                        for row in records:
                                self.dicSecequip.update( {str(row[1]) : str(row[0]) })
                                self.ui.comboBox_5.addItem(row[1])

                        query = ("SELECT distinct EstadoID,Estado FROM movedb.estado\
                                order by estado.EstadoID asc")

                        cursor.execute(query)
                        records = cursor.fetchall()
                        
                        self.ui.comboBox_6.addItem('')
                        for row in records:
                                self.dicestado.update( {str(row[1]) : str(row[0]) })
                                self.ui.comboBox_6.addItem(row[1])

                except mysql.connector.Error as err:
                        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                                print("Something is wrong with your user name or password")
                        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                                print("Database does not exist")
                        else:
                                print(err)
                                QMessageBox.critical(self, 'Error al cargar tablas', err)
                else:
                        cursor.close()

        def Interprete2(self,row):
                
                
                if(row[2] != None and row[2] != "" and self.ui.comboBox_7.findText(row[2])<0):
                        self.ui.comboBox_7.addItem(row[2])

                if(row[3] != None and row[2] != "" and self.ui.comboBox_8.findText(row[3])<0):
                        self.ui.comboBox_8.addItem(row[3])
                '''
                if(row[4] != None and self.ui.comboBox_4.findText(row[4])<0):
                        self.ui.comboBox_4.addItem(row[4])'''
        
        #Busca por nombre de producto y numero de serie carga resultados en lista ingresos
        def Traer_Prod(self,Nombre):
                try:
                        self.cnx = mysql.connector.connect(user=self.conn['user'], 
                                                        password=self.conn['password'],
                                                        host=self.conn['host'],
                                                        database=self.conn['database'])
                        aux = ''
                        cursor = self.cnx.cursor()
                        Nombre = self.ui.comboBox.currentText()
                        
                        NumSerie = self.ui.lineEdit.text()
                        Assy = self.ui.lineEdit_2.text()
                        
                        SeccEquip = self.ui.comboBox_5.currentText()
                        Categoria = self.ui.comboBox_2.currentText()
                        ubifis = self.ui.comboBox_3.currentText()
                        ubiexac = self.ui.comboBox_4.currentText()
                        estado = self.ui.comboBox_6.currentText()
                        cantidad = self.ui.lineEdit_3.text()

                        reqSerie =  "products.SerialNumber Like '"+ NumSerie + "%' "
                        reqNombre = "products.ProductName Like concat('%' ,'"+ Nombre + "' ,'%') "
                        reqAssy =   "products.Assy Like '" + Assy +  "%' "
                        reqSecEquip = "secequipo.SecEquipoName Like'"+ SeccEquip +"' "
                        reqCategoria = "categories.CategoryName Like '"+ Categoria +"' "
                        reqUbiFis = "ubicacionfisica.UbicacionFisicaName Like '"+ubifis+"' "
                        reqUbiExac = "ubicacionexacta.UbicacionExactaName Like '"+ubiexac+"' "
                        reqEstado = "estado.Estado Like '"+ estado +"' "

                        req = list()
                        
                        if(Nombre != ''):
                               req.append(reqNombre)
                        if(NumSerie != ''):
                               req.append(reqSerie)
                        if(Assy != '' ):
                                req.append(reqAssy)
                        if(SeccEquip != '' and SeccEquip != 'None'):
                                req.append(reqSecEquip)
                        if(Categoria != '' and Categoria != 'None'):
                                req.append(reqCategoria)
                        if(ubifis != '' and ubifis != 'None'):
                                req.append(reqUbiFis)
                        if(ubiexac != '' and ubiexac != 'None'):
                                req.append(reqUbiExac)
                        if(estado != '' and estado != 'None'):
                                req.append(reqEstado)
                        
                        
                        if len(req) > 1:
                                for reqpart in req:
                                        aux = aux + str(reqpart) + " and "
                                aux = aux[:-5]
                                
                        elif len(req) == 1:
                                aux = req[0]

                        
  
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
                                    WHERE " + aux + " ;" 

                        rows = cursor.execute(query)
                        data = cursor.fetchall()
                        

                        filas = self.ui.tableWidget.rowCount()
                        agregar = True
                        if(cantidad != ''):
                                self.ventana.cargar_data(data,cantidad)
                        else:
                                self.ventana.cargar_data(data)
                        
                        self.ventana.dialog.show()
  

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

        # Busca los movimientos segun ID y los carga en el item producto dado
        def Traer_Mov(self,Producto):

                try:
                        self.cnx = mysql.connector.connect(user=self.conn['user'], 
                                                        password=self.conn['password'],
                                                        host=self.conn['host'],
                                                        database=self.conn['database'])
                        cursor = self.cnx.cursor()
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
                                        where t1.ProductID = '"+str(Producto.ProductID) +"'\
                                        order by t1.TransactionID asc;")
                        
                        #query = "SELECT * FROM movedb.inventorytransactions where ProductID = '"+str(self.itemID) +"'"
                        rows = cursor.execute(query)
                        data = cursor.fetchall()

                        for row in data:
                                columns = convert(row)
                                Mov = item_Mov(list(columns))
                                Producto.Movimientos.append(Mov)
                                
                                #print(Mov.__dict__)
                                #for mov in Producto.Movimientos:
                                        #self.Agregar_tabMov(mov.__dict__)

                        self.ui.tableWidget_2.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
                        #self.ui.tableWidget.horizontalHeader().setSectionResizeMode(4,QHeaderView.Stretch)
                        self.ui.tableWidget_2.verticalHeader().resizeSections(QHeaderView.ResizeToContents)
                        
                except mysql.connector.Error as err:
                        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                                print("Something is wrong with your user name or password")
                        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                                print("Database does not exist")
                        else:
                                print(err)
                else:
                        cursor.close() 

        #Muestra en la tabla de ingresos la fila deseada
        def Agregar_tabIngre(self,row):
                rowPosition = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(rowPosition)
                
                ### todas las columnas
                for i, column in enumerate(row):
                        item = QtWidgets.QTableWidgetItem(str(row[column]))
                        if(i == 0):
                                item.setFlags(QtCore.Qt.ItemIsEnabled)
                        item = self.ui.tableWidget.setItem(rowPosition, i, item)
        
                        if(i == 2):
                                self.ui.tableWidget.item(rowPosition,i).setTextAlignment(QtCore.Qt.AlignCenter)
                                if(str(row[column]) != 'None'):
                                        if((int)(row[column]) <= 0):
                                                self.ui.tableWidget.item(rowPosition,i).setBackground(QColor(255,0,0))                

        #Muestra en la tabla de movimientos la fila deseada
        def Agregar_tabMov(self, row):
            rowPosition = self.ui.tableWidget_2.rowCount()
            self.ui.tableWidget_2.insertRow(0)
            
            ### todas las columnas
            for i, column in enumerate(row):
                
                item = QtWidgets.QTableWidgetItem(str(row[column]))
                if(i == 0):
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                item = self.ui.tableWidget_2.setItem(0, i, item)
            
        def Actualizar_en_base(self):
                if(self.ui.tableWidget.rowCount() > 0):
                        try:
                                self.cnx = mysql.connector.connect(user=self.conn['user'], 
                                                        password=self.conn['password'],
                                                        host=self.conn['host'],
                                                        database=self.conn['database'])
                                cursor = self.cnx.cursor()

                                for P in self.Ingresos:
                                        
                                        aux = str(P.ProductID)
                                        #Actualizacion de item
                                        if(aux[0] != 'N'):

                                                estadoindex = self.dicestado[str(P.Estado)]
                                                Secequipindex = self.dicSecequip[str(P.SeccEquip)]
                                                catindex = self.diccateg[str(P.Cat)]
                                                ubiExacindex = self.dicubiexacta[str(P.UbiExac)]
                                                ubiFisindex = self.dicubifisica[str(P.UbiFis)]
                                                        
                                                query = "UPDATE movedb.products\
                                                        SET products.ProductName = '" + str(P.ProductName) +"'\
                                                                        ,products.Observaciones = '" + str(P.Observacion) +"'\
                                                                        ,products.ProductDescription = '"+ str(P.Descrip) +"'\
                                                                        ,products.EstadoID = '"+ estadoindex +"'\
                                                                        ,products.SecEquipoID = '"+ Secequipindex +"'\
                                                                        ,products.CategoryID = '" + catindex +"'\
                                                                        ,products.SerialNumber = '" + str(P.Nserie) +"'\
                                                                        ,products.Assy = '" + str(P.PartNum) +"'\
                                                                        ,products.ubicacionexacta = '" + ubiExacindex+"'\
                                                                        ,products.ubicacionfisica = '" + ubiFisindex+"'\
                                                        WHERE  products.ProductID ='" + aux + "';"

                                                rows = cursor.execute(query)
                                                data = cursor.fetchall()

                                                #carga de movimientos nuevos
                                                for m in P.Movimientos:
                                                        
                                                        
                                                        if (str(m.ID[0]) == 'N'):
                                                                query = "insert into movedb.inventorytransactions\
                                                                        (  TransactionDate,\
                                                                                ProductID,\
                                                                                TransactionDescription,\
                                                                                UnitsReceived,\
                                                                                UnitsSold ,\
                                                                                UnitsShrinkage,\
                                                                                UnitsStock,\
                                                                                OrigenID,\
                                                                                DestinoID,\
                                                                                NumberMov)\
                                                                        Values  ('" + str(m.Date) +"', \
                                                                                 '" + str(P.ProductID) +"',\
                                                                                 '" + str(m.Descr) +"',\
                                                                                 '" + str(m.Urec) +"',\
                                                                                 '" + str(m.Usold) +"',\
                                                                                 '" + str(m.Ush) +"',\
                                                                                 '" + str(m.Usto) +"',\
                                                                                 '" + str(m.Ori) +"',\
                                                                                 '" + str(m.Dest) +"',\
                                                                                 '" + str(m.NumMov) +"');"

                                                                rows = cursor.execute(query)
                                                                data = cursor.fetchall()

                                                                query = " select Last_insert_ID();"
                                                                rows = cursor.execute(query)
                                                                data = cursor.fetchall()
                                                                m.ID = str(data[0][0]) 
                                        #Creacion de item nuevo           
                                        if(aux[0] == 'N'):
                                                
                                                estadoindex = self.dicestado[str(P.Estado)]
                                                Secequipindex = self.dicSecequip[str(P.SeccEquip)]
                                                catindex = self.diccateg[str(P.Cat)]
                                                ubiExacindex = self.dicubiexacta[str(P.UbiExac)]
                                                ubiFisindex = self.dicubifisica[str(P.UbiFis)]

                                                query = "insert into movedb.products\
                                                        (  products.ProductName,\
                                                                products.Observaciones,\
                                                                products.ProductDescription,\
                                                                products.EstadoID,\
                                                                products.SecEquipoID,\
                                                                products.CategoryID,\
                                                                products.SerialNumber,\
                                                                products.Assy,\
                                                                products.UbicacionExacta,\
                                                                products.UbicacionFisica)\
                                                        Values  ('" + str(P.ProductName) +"', \
                                                                '" + str(P.Observacion) +"',\
                                                                '" + str(P.Descrip) +"',\
                                                                '" + estadoindex +"',\
                                                                '" + Secequipindex +"',\
                                                                '" + catindex +"',\
                                                                '" + str(P.Nserie) +"',\
                                                                '" + str(P.PartNum) +"',\
                                                                '" + ubiExacindex +"',\
                                                                '" + ubiFisindex +"');"
                                                        
                                                rows = cursor.execute(query)
                                                data = cursor.fetchall()

                                                query = " select Last_insert_ID();"
                                                rows = cursor.execute(query)
                                                data = cursor.fetchall()
                                                for Fila in range(self.ui.tableWidget.rowCount()):
                                                        ID = self.ui.tableWidget.item(Fila,0).text()
                                                        if(str(P.ProductID) == ID):
                                                                self.ui.tableWidget.item(Fila,0).setText(str(data[0][0]))
                                                                P.ProductID = str(data[0][0])

                                                #Creacion de movimientos
                                                for m in P.Movimientos:
                                                        
                                                        
                                                        if (str(m.ID[0]) == 'N'):
                                                                query = "insert into movedb.inventorytransactions\
                                                                        (  TransactionDate,\
                                                                                ProductID,\
                                                                                TransactionDescription,\
                                                                                UnitsReceived,\
                                                                                UnitsSold ,\
                                                                                UnitsShrinkage,\
                                                                                UnitsStock,\
                                                                                OrigenID,\
                                                                                DestinoID,\
                                                                                NumberMov)\
                                                                        Values  ('" + str(m.Date) +"', \
                                                                                 '" + str(P.ProductID) +"',\
                                                                                 '" + str(m.Descr) +"',\
                                                                                 '" + str(m.Urec) +"',\
                                                                                 '" + str(m.Usold) +"',\
                                                                                 '" + str(m.Ush) +"',\
                                                                                 '" + str(m.Usto) +"',\
                                                                                 '" + str(m.Ori) +"',\
                                                                                 '" + str(m.Dest) +"',\
                                                                                 '" + str(m.NumMov) +"');"

                                                                rows = cursor.execute(query)
                                                                data = cursor.fetchall()

                                                                query = " select Last_insert_ID();"
                                                                rows = cursor.execute(query)
                                                                data = cursor.fetchall()
                                                                m.ID = str(data[0][0])
                                while (self.ui.tableWidget_2.rowCount() > 0):
                                        self.ui.tableWidget_2.removeRow(0)

                                while (self.ui.comboBox.count() > 0):
                                        self.ui.comboBox.removeItem(0)
                                query = ("SELECT distinct products.ProductName from movedb.products order by ProductName")
                                cursor.execute(query)
                                records = cursor.fetchall()
                        
                                for row in records:
                                        self.ui.comboBox.addItem(row[0])
                                
                        except mysql.connector.Error as err:
                                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                                        print("Something is wrong with your user name or password")
                                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                                        print("Database does not exist")
                                else:
                                        print(err)

                                        QMessageBox.critical(self, 'Error al actualizar en base', err)
                        else:
                                QMessageBox.information(self, 'Info', 'Carga Exitosa')
                                cursor.close()
                        
                
        

                
                        


def convert(in_data):
        def cvt(data):
            try:
                return ast.literal_eval(data)
            except Exception:
                return str(data)
        return tuple(map(cvt, in_data))

class BlobDelegate(QtWidgets.QStyledItemDelegate):
        Signalresize = QtCore.pyqtSignal()
        def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QWidget:
            parent = QTextEdit(parent)
            
            return parent

        def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
            
            editor.setText(index.data())
        
        def setModelData(self, editor: QWidget, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
            model.setData(index, editor.toPlainText())
            self.Signalresize.emit()
                        
            
            


        def displayText(self, value, locale):
                #value = value + '1'
                if isinstance(value, QtCore.QByteArray):
                        value = value.data().decode() + '1'
                return super(BlobDelegate, self).displayText(value, locale)


def add_table(columns, ui):
            rowPosition = ui.tableWidget.rowCount()
            ui.tableWidget.insertRow(rowPosition)
            
            ### todas las columnas
            for i, column in enumerate(columns):
                item = QtWidgets.QTableWidgetItem(str(column))
                '''if i==0:
                        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        item.setCheckState(QtCore.Qt.Unchecked)
                '''
                item = ui.tableWidget.setItem(rowPosition, i, item)
        
                if(i == 2):
                        ui.tableWidget.item(rowPosition,i).setTextAlignment(QtCore.Qt.AlignCenter)
                        if(str(column) != 'None'):
                            if((int)(column) <= 0):
                                ui.tableWidget.item(rowPosition,i).setBackground(QColor(255,0,0))

def add_table2(columns, ui):
            rowPosition = ui.tableWidget_2.rowCount()
            ui.tableWidget_2.insertRow(rowPosition)
            
            ### todas las columnas
            for i, column in enumerate(columns):
                item = QtWidgets.QTableWidgetItem(str(column))
                '''if i==0:
                        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        item.setCheckState(QtCore.Qt.Unchecked)
                '''
                item = ui.tableWidget_2.setItem(rowPosition, i, item)
                

