import errno
from msilib.schema import ListView
import string
from xml.dom.minidom import TypeInfo
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QWidget,QComboBox
from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from functools import partial
from qts.Ui_ventana_tablas import Ui_Form

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
        
        '''
        self.ui.comboBox.currentIndexChanged.connect(  partial(self.Filtro, self.ui.comboBox) )
        self.ui.comboBox_2.currentIndexChanged.connect(partial(self.Filtro, self.ui.comboBox_2) )
        self.ui.comboBox_3.currentIndexChanged.connect(partial(self.Filtro, self.ui.comboBox_3) )
        self.ui.comboBox_4.currentIndexChanged.connect(partial(self.Filtro, self.ui.comboBox_4) )
        self.ui.comboBox_5.currentIndexChanged.connect(partial(self.Filtro, self.ui.comboBox_5) )
        '''
        for combobox in self.widget.findChildren(QComboBox):
            if(str(combobox.objectName) <= str(self.ui.comboBox_5.objectName) ):
                combobox.currentTextChanged.connect(self.Filtro)
        self.ui.pushButton_3.clicked.connect(self.Limpiar)
        self.ui.pushButton_4.clicked.connect(self.AgregarPosi)

        #self.ui.listWidget.currentItemChanged.connect(self.seleccion)

    def Limpiar(self):
        for combobox in self.widget.findChildren(QComboBox):
            if(str(combobox.objectName) <= str(self.ui.comboBox_5.objectName) ):
                combobox.setCurrentIndex(0)

    def AgregarPosi(self):
        
        lista_combobox = list()

        for combobox in self.widget.findChildren(QComboBox):
            if(str(combobox.objectName) <= str(self.ui.comboBox_5.objectName) ):
                if(combobox == self.ui.comboBox_3 and combobox.currentText() != ""):
                    lista_combobox.append("P"+combobox.currentText())
                elif(combobox == self.ui.comboBox_4 and combobox.currentText() != ""):
                    lista_combobox.append("Sec-"+combobox.currentText())
                else:
                    lista_combobox.append(combobox.currentText())
                
        filtro = ""
        for item in lista_combobox:
            if(filtro == ""):
                filtro = item
            else: 
                if(item != ""):
                    filtro = filtro + " " + item 

        filtro = filtro[0:-2]
        #print(filtro)
        if(filtro != ""):
            #self.ui.listWidget.addItem(filtro)
           
            aux = [(filtro,)]
            #print(aux)
            
            #self.Interprete(aux, self.ui.listWidget)
            try:
                self.cnx = mysql.connector.connect( user=self.conn['user'], 
                                                    password=self.conn['password'],
                                                    host=self.conn['host'],
                                                    database=self.conn['database'])

                cursor = self.cnx.cursor()
                #ubifisica
                query = ("INSERT INTO movedb.ubicacionfisica (UbicacionFisicaName)\
                            VALUES ('"+ filtro +"');")
                            
                
                cursor.execute(query)
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


    def seleccion(self, value):
        print(value.text())
        self.ui.listWidget.se

    def Filtro(self):
        
        lista_combobox = list()
        self.ui.listWidget.clear()
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
                if(combobox == self.ui.comboBox_3 and combobox.currentText() != ""):
                    lista_combobox.append("P"+combobox.currentText())
                elif(combobox == self.ui.comboBox_4 and combobox.currentText() != ""):
                    lista_combobox.append("Sec-"+combobox.currentText())
                else:
                    lista_combobox.append(combobox.currentText())
                
        filtro = ""
        for item in lista_combobox:
            if(filtro == ""):
                filtro = item
            else: 
                if(item != ""):
                    filtro = filtro + " " + item 

        filtro = filtro[0:-2]
        
        #print("filtro: "+ filtro)


        try:
            self.cnx = mysql.connector.connect( user=self.conn['user'], 
                                                password=self.conn['password'],
                                                host=self.conn['host'],
                                                database=self.conn['database'])

            cursor = self.cnx.cursor()
            #ubifisica
            query = ("SELECT distinct UbicacionFisicaName FROM movedb.ubicacionfisica\
                        where UbicacionFisicaName like '%"+ filtro +"%'\
                        order by ubicacionfisica.UbicacionFisicaName asc")
            
            cursor.execute(query)
            records = cursor.fetchall()
            self.Interprete(records, self.ui.listWidget)
            
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
                combobox.currentTextChanged.connect(self.Filtro)
                pass
                '''
                if(combobox.count() == 1 and combobox.currentText()== ""):
                    combobox.setDisabled(1)
                else:
                    combobox.setDisabled(0)
                '''

    def Cargar_Ubicaciones(self):
        self.ui.comboBox.addItem("")
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.comboBox_2.addItem("")
        self.ui.comboBox_2.setCurrentIndex(0)
        self.ui.comboBox_6.addItem("")
        self.ui.comboBox_7.addItem("")
        self.ui.comboBox_8.addItem("")
        #Ubi_fisica = QListWidgetItem("Prueba")
        #self.ui.listWidget.addItem(Ubi_fisica)
          
        try:
            self.cnx = mysql.connector.connect( user=self.conn['user'], 
                                                password=self.conn['password'],
                                                host=self.conn['host'],
                                                database=self.conn['database'])

            cursor = self.cnx.cursor()
            #ubifisica
            query = ("SELECT distinct UbicacionFisicaName FROM movedb.ubicacionfisica\
                        order by ubicacionfisica.UbicacionFisicaName asc")
            
            cursor.execute(query)
            records = cursor.fetchall()

            self.Interprete(records, self.ui.listWidget)

            #ubiexacta
            query = ("SELECT distinct UbicacionExactaID,UbicacionExactaName FROM movedb.ubicacionexacta\
                                order by ubicacionexacta.UbicacionExactaID asc")             
            cursor.execute(query)
            records = cursor.fetchall()
            
            self.Interprete(records, self.ui.listWidget_2)

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

    def Interprete(self, records, lista):
        if(lista == self.ui.listWidget):
            
            for row in records:  
                        aux = list(['','',' ',' ',' '])
                        
                        r = row[0].split()
                        #print(r)
                        Ubifis = Ubicacion_Fisica(r[0])
                        
                        for p in range(len(r)):
                            aux[p] = r[p]
                            
                        lista.addItem(row[0])
                                 
                        #Objeto
                        if(self.ui.comboBox.findText(Ubifis.Objeto)< 0):

                            self.ui.comboBox.addItem(Ubifis.Objeto)
                            self.ListaUbiFis.append(Ubifis)

                        #Nombre num
                        if(self.ui.comboBox_2.findText(aux[1]) < 0):
                            self.ui.comboBox_2.addItem(aux[1])

                        #Puerta
                        if(self.ui.comboBox_3.findText(aux[2][1:]) < 0):

                            Puerta = aux[2]    
                            if(Puerta[0] == 'P' ):
                                self.ui.comboBox_3.addItem(aux[2][1:])
                            if(Puerta[0:3] == 'Sec'):
                                self.ui.comboBox_4.addItem(Puerta[4:])

                        #Seccion
                        if(self.ui.comboBox_4.findText(aux[3]) < 0):
                            Sec = aux[3]
                            if(Sec[0:3] == 'Sec'):       
                                self.ui.comboBox_4.addItem(aux[3])

                        #Posicion
                        if(self.ui.comboBox_5.findText(aux[4]) < 0):
                            self.ui.comboBox_5.addItem(aux[4])

        elif(lista == self.ui.listWidget_2):
            
            for row in records:
                        aux = list(['','',' ',' ',' ',' '])
                        
                        r = row[1].split()
                        #print(r)
                        Ubiexac = Ubicacion_Exacta(r[0])
                        
                        for p in range(len(r)):
                            aux[p] = r[p]
                            
                        lista.addItem(row[1])
                                 
                        #Objeto
                        if(self.ui.comboBox_6.findText(Ubiexac.Objeto) < 0):

                            self.ui.comboBox_6.addItem(Ubiexac.Objeto)
                            self.ListaUbiexac.append(Ubiexac)

                        #Nombre num
                        if(self.ui.comboBox_7.findText(aux[1]) < 0):
                            self.ui.comboBox_7.addItem(aux[1])

                        #Puerta
                        if(self.ui.comboBox_8.findText(aux[2][1:]) < 0):

                            Puerta = aux[2]    
                            if(Puerta[0] == 'P' ):
                                self.ui.comboBox_8.addItem(aux[2][1:])
                            if(Puerta[0:3] == 'Sec'):
                                self.ui.comboBox_9.addItem(Puerta[4:])

                        #Seccion
                        if(self.ui.comboBox_9.findText(aux[3]) < 0):
                            Sec = aux[3]
                            if(Sec[0:3] == 'Sec-'):       
                                self.ui.comboBox_9.addItem(aux[3])

                        #Posicion
                        if(self.ui.comboBox_10.findText(aux[4]) < 0):
                            self.ui.comboBox_10.addItem(aux[4])
                    


class Ubicacion_Fisica(object):

    def __init__(self,obj, Nombrenum = '', puerta = '', seccion = '', posi = '' ):
        self.Objeto = obj
        self.NombreNum = Nombrenum
        self.Puerta = puerta
        self.Seccion = seccion
        self.Posicion = posi

class Ubicacion_Exacta(object):

    def __init__(self,obj, Nombrenum = '', puerta = '', seccion = '', posi = '' ):
        self.Objeto = obj
        self.NombreNum = Nombrenum
        self.Puerta = puerta
        self.Seccion = seccion
        self.Posicion = posi