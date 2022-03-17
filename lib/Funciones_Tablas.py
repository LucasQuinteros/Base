from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QWidget
from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode

from qts.Ui_ventana_tablas import Ui_Form

class clase_tablas(QWidget):
    
    def __init__(self, conn):
        super().__init__()
        self.widget = QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.widget)
        self.conn = conn
        self.ListaUbiFis = list()
        self.ui.comboBox_3.addItem('')
        self.ui.comboBox_4.addItem('')
        self.Cargar_Ubicaciones()

        self.ui.pushButton_3.clicked.connect(self.Buscar_Filtrar)
        

    def Cargar_Ubicaciones(self):

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

            for row in records:  
                        aux = list(['','',' ',' ',' '])
                        
                        r = row[0].split()
                        #print(r)
                        Ubifis = Ubicacion_Fisica(r[0])
                        
                        for p in range(len(r)):
                            aux[p] = r[p]
                            
                        
                        self.ui.listWidget.addItem(row[0])
                       
                                                
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
                            print(Puerta[0:3])
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

            #ubiexacta
            query = ("SELECT distinct UbicacionExactaID,UbicacionExactaName FROM movedb.ubicacionexacta\
                                order by ubicacionexacta.UbicacionExactaID asc")             
            cursor.execute(query)
            records = cursor.fetchall()
            
            for row in records:
                        self.ui.listWidget_2.addItem(row[1])

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
            else:
                    print(err)
        else:
                cursor.close()

    def Buscar_Filtrar(self):
        self.ui.listWidget.clear()
        try:
            self.cnx = mysql.connector.connect( user=self.conn['user'], 
                                                password=self.conn['password'],
                                                host=self.conn['host'],
                                                database=self.conn['database'])

            cursor = self.cnx.cursor()
            #ubifisica
            filter = self.ui.comboBox.currentText()
            
            if(self.ui.comboBox_2.currentText() != ' '):
                        filter = filter + ' ' +self.ui.comboBox_2.currentText()
                        self.ui.comboBox_3.currentText() 

            query = ("SELECT distinct UbicacionFisicaName FROM movedb.ubicacionfisica\
                        where UbicacionFisicaName Like '%" + filter +"%' \
                        order by ubicacionfisica.UbicacionFisicaName asc")

            cursor.execute(query)
            records = cursor.fetchall()
            for row in records:
                        self.ui.listWidget.addItem(row[0])

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
            else:
                    print(err)
        else:
                cursor.close()


class Ubicacion_Fisica(object):

    def __init__(self,obj, Nombrenum = '', puerta = '', seccion = '', posi = '' ):
        self.Objeto = obj
        self.NombreNum = Nombrenum
        self.Puerta = puerta
        self.Seccion = seccion
        self.Posicion = posi