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
        self.Cargar_Ubicaciones()

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
                        self.ui.listWidget.addItem(row[0])
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