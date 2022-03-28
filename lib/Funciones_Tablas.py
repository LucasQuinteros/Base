import errno
from msilib.schema import ListView
import string

from xml.dom.minidom import TypeInfo
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QWidget,QComboBox,QTableWidgetItem,QTableWidget,QHeaderView
from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from functools import partial
from qts.Ui_ventana_tablas import Ui_Form

NoneType = type(None)
class clase_tablas(QWidget):
    
    def __init__(self, conn):
        super().__init__()
        self.widget = QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.widget)
        self.conn = conn
        self.ListaUbiFis = list()
        self.ListaUbiexac = list()
        self.ui.comboBox_3.addItem('')
        self.ui.comboBox_4.addItem('')
        self.Cargar_Ubicaciones()
        
        for combobox in self.widget.findChildren(QComboBox):
            if(str(combobox.objectName) <= str(self.ui.comboBox_5.objectName) ):
                combobox.currentTextChanged.connect(self.Filtro3)
        
        for combobox in self.widget.findChildren(QComboBox):
            if(str(combobox.objectName) >= str(self.ui.comboBox_6.objectName) ):
                
                combobox.currentTextChanged.connect(self.Filtro3)

        self.ui.pushButton_3.clicked.connect(lambda: self.Limpiar(self.ui.pushButton_3))
        self.ui.pushButton_4.clicked.connect(self.AgregarPosi)

        self.ui.pushButton_5.clicked.connect(lambda: self.Limpiar(self.ui.pushButton_5))
        self.ui.pushButton_6.clicked.connect(self.AgregarPosi)

        self.ui.tableWidget.cellClicked.connect(self.seleccion2)
        
        self.ui.tableWidget_2.cellClicked.connect(self.seleccion2)

    def Limpiar(self,boton):
        if(boton == self.ui.pushButton_3):
            for combobox in self.widget.findChildren(QComboBox):
                if(str(combobox.objectName) <= str(self.ui.comboBox_5.objectName) ):
                    combobox.setCurrentIndex(0)
        elif(boton == self.ui.pushButton_5):
            for combobox in self.widget.findChildren(QComboBox):
                if(str(combobox.objectName) >= str(self.ui.comboBox_6.objectName) ):
                    combobox.setCurrentIndex(0)

    def AgregarPosi(self):
        
        lista_combobox = list()
        if( self.sender() == self.ui.pushButton_4 ):
            Objeto = ''
            Numero = ''
            Seccion = ''
            Puerta = ''
                      
            for combobox in self.widget.findChildren(QComboBox):
                if(str(combobox.objectName) <= str(self.ui.comboBox_5.objectName) ):
                    if(combobox.currentText() != ""):
                        if(combobox == self.ui.comboBox_3 ):
                            lista_combobox.append("P"+combobox.currentText())
                            Puerta = combobox.currentText()
                            
                        elif(combobox == self.ui.comboBox_4):
                            lista_combobox.append("Sec-"+combobox.currentText())
                            Seccion = combobox.currentText()
                            
                        elif(combobox == self.ui.comboBox_2):
                            Numero = combobox.currentText()
                            lista_combobox.append(combobox.currentText())
                                
                        elif(combobox == self.ui.comboBox):                        
                            Objeto = combobox.currentText()
                            lista_combobox.append(combobox.currentText())
                            
                        else:
                            lista_combobox.append(combobox.currentText())
                    
            filtro = ""
            for item in lista_combobox:
                if(filtro == ""):
                    filtro = item.strip()
                else: 
                    if(item != ""):
                        filtro = filtro + " " + item.strip()

            query = ("INSERT INTO movedb.ubicacionfisica (UbicacionFisicaName, Objeto, Numero, Seccion, Puerta)\
                    VALUES ('"+ filtro +"', '"+ Objeto +"','"+ Numero +"', '"+ Seccion +"','"+ Puerta +"');")
                
        elif( self.sender() == self.ui.pushButton_6 ):
            Objeto = ''
            Numero = ''
            Seccion = ''
            Puerta = ''
            Estante = ''
                      
            for combobox in self.widget.findChildren(QComboBox):
                if(str(combobox.objectName) >= str(self.ui.comboBox_6.objectName) ):
                    if(combobox.currentText() != ""):
                        if(combobox == self.ui.comboBox_8 ):
                            lista_combobox.append("P"+combobox.currentText())
                            Puerta = combobox.currentText()
                            
                        elif(combobox == self.ui.comboBox_9):
                            lista_combobox.append("Sec-"+combobox.currentText())
                            Seccion = combobox.currentText()
                            
                        elif(combobox == self.ui.comboBox_7):
                            Numero = combobox.currentText()
                            lista_combobox.append(combobox.currentText())
                                
                        elif(combobox == self.ui.comboBox_6):                        
                            Objeto = combobox.currentText()
                            lista_combobox.append(combobox.currentText())
                            
                        elif(combobox == self.ui.comboBox_10):                        
                            Estante = combobox.currentText()
                            lista_combobox.append("Estante " + combobox.currentText())
                            
                        else:
                            lista_combobox.append(combobox.currentText())
                    
            filtro = ""
            for item in lista_combobox:
                if(filtro == ""):
                    filtro = item.strip()
                else: 
                    if(item != ""):
                        filtro = filtro + " " + item.strip()

            query = ("INSERT INTO movedb.ubicacionexacta (UbicacionExactaName, Objeto, Numero, Seccion, Puerta, Estante)\
                    VALUES ('"+ filtro +"', '"+ Objeto +"','"+ Numero +"', '"+ Seccion +"','"+ Puerta +"','"+ Estante +"');")
            
        if(self.sender() == self.ui.pushButton_4 and self.ui.comboBox.currentText().strip() != '' or
            self.sender() == self.ui.pushButton_6 and self.ui.comboBox_6.currentText().strip() != ''):
            try:
                        self.cnx = mysql.connector.connect( user=self.conn['user'], 
                                                            password=self.conn['password'],
                                                            host=self.conn['host'],
                                                            database=self.conn['database'])

                        cursor = self.cnx.cursor()
                        

                                    
                        print(query)
                        #cursor.execute(query)
                        records = cursor.fetchall()
                                   
            except mysql.connector.Error as err:
                        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                                print("Something is wrong with your user name or password")
                        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                                print("Database does not exist")
                        else:
                                print(err)
            else:
                            cursor.close()
                       
    def seleccion2(self, value):
        
        tabla = self.sender()
        aux = list()
        if(value != NoneType and tabla == self.ui.tableWidget):
            for i in range(tabla.columnCount()):
                if( i!= 1 ):
                    aux.append(str(tabla.item(value,i).text() ) ) 

            i = 0 
            for combobox in self.widget.findChildren(QComboBox): 
                if(str(combobox.objectName) <= str(self.ui.comboBox_4.objectName)):
                    if(i == 0 ):
                        combobox.setCurrentText(aux[i].split()[0])
                    else:
                        if(aux[i] != NoneType):
                            combobox.setCurrentText(aux[i].strip())
                    i = i + 1 

        elif(value != NoneType and tabla == self.ui.tableWidget_2):

            for i in range(tabla.columnCount()):
                if( i!= 1 ):
                    aux.append(str(tabla.item(value,i).text() ) ) 

            i = 0 
            for combobox in self.widget.findChildren(QComboBox): 
                if(str(combobox.objectName) >= str(self.ui.comboBox_6.objectName)):
                    if(i == 0 ):
                        combobox.setCurrentText(aux[i].split()[0])
                    else:
                        combobox.setCurrentText(aux[i].strip())
                    i = i + 1 
                

    def Filtro3(self):

        combo = self.sender()
        lista_req = list()

        if( str(combo.objectName) <= str(self.ui.comboBox_5.objectName) ):
            
            while self.ui.tableWidget.rowCount() != 0:
                self.ui.tableWidget.removeRow(0)
            
            for combobox in self.widget.findChildren(QComboBox):
                if(str(combobox.objectName) <= str(self.ui.comboBox_5.objectName)):
                    combobox.currentTextChanged.disconnect()
                    save = combobox.currentText()
                    if(combobox != self.ui.comboBox):
                        combobox.clear()
                        combobox.addItem("")
                    combobox.setCurrentText(save)

            for combobox in self.widget.findChildren(QComboBox):
                if(str(combobox.objectName) <= str(self.ui.comboBox_5.objectName) ):
                    if(combobox.currentText() != ""):
                        if(combobox == self.ui.comboBox):
                            Ubicacion =  combobox.currentText().strip()
                            reqUbicacion = "UbicacionFisicaName like '%"+ Ubicacion +"%'"
                            lista_req.append(reqUbicacion)
                        elif(combobox == self.ui.comboBox_2):
                            Numero = combobox.currentText().strip()
                            reqNumero = "Numero like '%"+ Numero +"%'"
                            lista_req.append(reqNumero)
                        elif(combobox == self.ui.comboBox_3):
                            Puerta=combobox.currentText().strip()
                            reqPuerta = "Puerta like '%"+ Puerta +"%'"
                            lista_req.append(reqPuerta)
                        elif(combobox == self.ui.comboBox_4):
                            Seccion = combobox.currentText().strip()
                            reqSeccion = "Seccion like '%"+ Seccion +"%'"
                            lista_req.append(reqSeccion)
            filtro = ''
            aux = ''
            if (len(lista_req) == 1):
                
                filtro = 'where '+ lista_req[0]
            elif (len(lista_req) > 1):
                
                for reqpart in lista_req:
                    aux = aux + reqpart + " and "
                filtro ='where '+ aux[:-5]
            
            try:
                self.cnx = mysql.connector.connect( user=self.conn['user'], 
                                                    password=self.conn['password'],
                                                    host=self.conn['host'],
                                                    database=self.conn['database'])

                cursor = self.cnx.cursor()
                #ubiexacta
                query = ("SELECT UbicacionFisicaName,Objeto,Numero,Puerta,Seccion FROM movedb.ubicacionfisica\
                            "+ filtro +" \
                            order by ubicacionfisica.UbicacionFisicaName asc")
                
                cursor.execute(query)
                records = cursor.fetchall()
                self.Interprete2(records, self.ui.tableWidget)  

            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                        print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                        print("Database does not exist")
                else:
                        print(err)
            else:
                    cursor.close()

            for combobox in self.widget.findChildren(QComboBox):
                if(str(combobox.objectName) <= str(self.ui.comboBox_5.objectName) ):
                    combobox.currentTextChanged.connect(self.Filtro3)

            

        elif( str(combo.objectName) >= str(self.ui.comboBox_6.objectName) ):

            
            while self.ui.tableWidget_2.rowCount() != 0:
                self.ui.tableWidget_2.removeRow(0)
            
            for combobox in self.widget.findChildren(QComboBox):
                if(str(combobox.objectName) >= str(self.ui.comboBox_6.objectName)):
                    combobox.currentTextChanged.disconnect()
                    save = combobox.currentText()
                    if(combobox != self.ui.comboBox_6):
                        combobox.clear()
                        combobox.addItem("")
                    combobox.setCurrentText(save)

            for combobox in self.widget.findChildren(QComboBox):
                if(str(combobox.objectName) >= str(self.ui.comboBox_6.objectName) ):
                    if(combobox.currentText() != ""):
                        if(combobox == self.ui.comboBox_6):
                            Ubicacion =  combobox.currentText().strip()
                            reqUbicacion = "UbicacionExactaName like '%"+ Ubicacion +"%'"
                            lista_req.append(reqUbicacion)
                        elif(combobox == self.ui.comboBox_7):
                            Numero = combobox.currentText().strip()
                            reqNumero = "Numero like '%"+ Numero +"%'"
                            lista_req.append(reqNumero)
                        elif(combobox == self.ui.comboBox_8):
                            Puerta=combobox.currentText().strip()
                            reqPuerta = "Puerta like '%"+ Puerta +"%'"
                            lista_req.append(reqPuerta)
                        elif(combobox == self.ui.comboBox_9):
                            Seccion = combobox.currentText().strip()
                            reqSeccion = "Seccion like '%"+ Seccion +"%'"
                            lista_req.append(reqSeccion)
                        else:
                            Estante = combobox.currentText().strip()
                            reqEstante = "Estante like '%"+ Estante +"%'"
                            lista_req.append(reqEstante)

            filtro = ''
            aux = ''
            if (len(lista_req) == 1):
                
                filtro = 'where '+ lista_req[0]
            elif (len(lista_req) > 1):
                
                for reqpart in lista_req:
                    aux = aux + reqpart + " and "
                filtro ='where '+ aux[:-5]
            
            try:
                self.cnx = mysql.connector.connect( user=self.conn['user'], 
                                                    password=self.conn['password'],
                                                    host=self.conn['host'],
                                                    database=self.conn['database'])

                cursor = self.cnx.cursor()
                #ubiexacta
                query = ("SELECT UbicacionExactaName,Objeto,Numero,Puerta,Seccion,Estante FROM movedb.ubicacionexacta\
                            "+ filtro +" \
                            order by ubicacionexacta.UbicacionExactaName asc")
                
                cursor.execute(query)
                records = cursor.fetchall()
                self.Interprete2(records, self.ui.tableWidget_2)  
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                        print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                        print("Database does not exist")
                else:
                        print(err)
            else:
                    cursor.close()

            for combobox in self.widget.findChildren(QComboBox):
                if(str(combobox.objectName) >= str(self.ui.comboBox_6.objectName) ):
                    combobox.currentTextChanged.connect(self.Filtro3)


    def Cargar_Ubicaciones(self):
        self.ui.comboBox.addItem("")
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.comboBox_2.addItem("")
        self.ui.comboBox_2.setCurrentIndex(0)
        self.ui.comboBox_6.addItem("")
        self.ui.comboBox_7.addItem("")
        self.ui.comboBox_8.addItem("")

          
        try:
            self.cnx = mysql.connector.connect( user=self.conn['user'], 
                                                password=self.conn['password'],
                                                host=self.conn['host'],
                                                database=self.conn['database'])

            cursor = self.cnx.cursor()
            #ubifisica
            query = ("SELECT UbicacionFisicaName,Objeto,Numero,Puerta,Seccion FROM movedb.ubicacionfisica\
                        order by ubicacionfisica.UbicacionFisicaName asc")
            
            cursor.execute(query)
            records = cursor.fetchall()

            self.Interprete2(records, self.ui.tableWidget)

            #ubiexacta
            query = ("SELECT UbicacionExactaName,Objeto,Numero,Puerta,Seccion,Estante FROM movedb.ubicacionexacta\
                                order by ubicacionexacta.UbicacionExactaName asc")             
            cursor.execute(query)
            records = cursor.fetchall()

            self.Interprete2(records, self.ui.tableWidget_2)

            if( self.ui.comboBox_5.count() == 1):
                self.ui.comboBox_5.setDisabled(1)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
            else:
                    print(err)
        else:
                cursor.close()

                    
    def Interprete2(self,records, tabla: QTableWidget):
        if(tabla == self.ui.tableWidget):
            
            for row in records:
                rowPosition = tabla.rowCount()
                tabla.insertRow(rowPosition)
                for i,item in enumerate(row):
                    if(item == None):
                        tabla.setItem(rowPosition,i,QTableWidgetItem(str(" ")))
                    else:
                        tabla.setItem(rowPosition,i,QTableWidgetItem(str(item)))
                r = row[0].split()

                if(r[0] != None and self.ui.comboBox.findText(r[0]) < 0):
                    self.ui.comboBox.addItem(r[0] )

                if(row[2] != None and self.ui.comboBox_2.findText(row[2])<0):
                    self.ui.comboBox_2.addItem(row[2])

                if(row[3] != None and self.ui.comboBox_3.findText(row[3])<0):
                    self.ui.comboBox_3.addItem(row[3])

                if(row[4] != None and self.ui.comboBox_4.findText(row[4])<0):
                    self.ui.comboBox_4.addItem(row[4])

        if(tabla == self.ui.tableWidget_2):
            if( self.ui.comboBox_9.findText("") == -1):
                self.ui.comboBox_9.addItem("")
            if( self.ui.comboBox_10.findText("") == -1):
                self.ui.comboBox_10.addItem("")
            self.ui.comboBox_7.setInsertPolicy(QComboBox.InsertAlphabetically)
            
            for row in records:
                
                rowPosition = tabla.rowCount()
                tabla.insertRow(rowPosition)
                ### todas las columnas
                for i, column in enumerate(row ):
                        if(column == None):
                            tabla.setItem(rowPosition, i, QTableWidgetItem(str(" ")))
                        else:
                            tabla.setItem(rowPosition, i, QTableWidgetItem(str(column)))                 

                r = row[0].split()

                if(r[0] != None and self.ui.comboBox_6.findText(r[0]) < 0):
                    self.ui.comboBox_6.addItem(r[0] )

                if(row[2] != None and self.ui.comboBox_7.findText(row[2])<0):
                    self.ui.comboBox_7.addItem(row[2])

                if(row[3] != None and self.ui.comboBox_8.findText(row[3])<0):
                    self.ui.comboBox_8.addItem(row[3])

                if(row[4] != None and self.ui.comboBox_9.findText(row[4])<0):
                    self.ui.comboBox_9.addItem(row[4])

                if(row[5] != None and self.ui.comboBox_10.findText(row[5])<0):
                    self.ui.comboBox_10.addItem(row[5])

        tabla.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        tabla.horizontalHeader().setSectionResizeMode(0,QHeaderView.Stretch)

class Ubicacion_Fisica(object):

    def __init__(self,obj, Nombrenum = '', puerta = '', seccion = '', posi = '' ):
        self.Objeto = obj
        self.NombreNum = Nombrenum
        self.Puerta = puerta
        self.Seccion = seccion
        self.Posicion = posi

class Ubicacion_Exacta(object):

    def __init__(self,obj, num = '', puerta = '', seccion = '', estante = '' ):
        self.Objeto = obj
        self.Num = num
        self.Puerta = puerta
        self.Seccion = seccion
        self.Estante = estante