from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QHeaderView, QMenu, QWidget
from qts.Ui_ventana_nuevo import Ui_Form
import mysql.connector
from mysql.connector import errorcode


class clase_nuevo(QWidget):
    def __init__(self):
            super().__init__()
            self.widget = QWidget()
            self.ui = Ui_Form()
            self.ui.setupUi(self.widget)
            self.ui.pushButton_3.clicked.connect(self.Cargar_nuevo)

    def Cargar_tablas(self, cnx):
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
        try:
                self.cnx = cnx
                cursor = self.cnx.cursor()

                query = ("SELECT distinct UbicacionFisicaID,UbicacionFisicaName FROM movedb.ubicacionfisica\
                        order by ubicacionfisica.UbicacionFisicaID asc")
                
                cursor.execute(query)
                records = cursor.fetchall()
                
                
                self.ui.comboBox.addItem('')
                for row in records:
                        self.dicubifisica.update( {str(row[1]) : str(row[0]) } )
                        self.ui.comboBox.addItem(row[1])

                
                query = ("SELECT distinct categories.CategoryID,categories.CategoryName FROM movedb.categories\
                            order by categories.CategoryID asc")
                
                cursor.execute(query)
                records = cursor.fetchall()
                

                self.ui.comboBox_4.addItem('')
                for row in records:
                        self.diccateg.update( {str(row[1]) : str(row[0]) })
                        self.ui.comboBox_4.addItem(row[1])

                query = ("SELECT distinct UbicacionExactaID,UbicacionExactaName FROM movedb.ubicacionexacta\
                            order by ubicacionexacta.UbicacionExactaID asc")
                
                cursor.execute(query)
                records = cursor.fetchall()
                

                self.ui.comboBox_5.addItem('')
                for row in records:
                        self.dicubiexacta.update( {str(row[1]) : str(row[0]) })
                        self.ui.comboBox_5.addItem(row[1])

                query = ("SELECT distinct EstadoID,Estado FROM movedb.estado\
                            order by estado.EstadoID asc")
                
                cursor.execute(query)
                records = cursor.fetchall()
                

                self.ui.comboBox_3.addItem('')
                for row in records:
                        self.dicestado.update( {str(row[1]) : str(row[0]) })
                        self.ui.comboBox_3.addItem(row[1])

                query = ("SELECT distinct SecEquipoID,SecEquipoName FROM movedb.secequipo\
                            order by secequipo.SecEquipoID asc")
                
                cursor.execute(query)
                records = cursor.fetchall()
                

                self.ui.comboBox_2.addItem('')
                for row in records:
                        self.dicSecequip.update( {str(row[1]) : str(row[0]) })
                        self.ui.comboBox_2.addItem(row[1])

        except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)
        else:
                cursor.close() 

    def Cargar_nuevo(self):
            item = list()
            Serie = ''
            
            Nombre = self.ui.lineEdit_3.text()
            item.append(Nombre)

            cant = self.ui.lineEdit.text()
            item.append(cant)
        
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
            item.append(self.ui.comboBox.currentText())

            Secequipindex = self.dicSecequip[self.ui.comboBox_2.currentText()]
            item.append(self.ui.comboBox_2.currentText())
            
            print(item)
            
            try:

                cursor = self.cnx.cursor()

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
                        Values  ('" + Nombre +"', \
                                '" + Observacion +"',\
                                '" + descrip +"',\
                                '" + estadoindex +"',\
                                '" + Secequipindex +"',\
                                '" + catindex +"',\
                                '" + Serie +"',\
                                '" + Assy +"',\
                                '" + ubiexacindex +"',\
                                '" + ubifisindex +"');"

                
                rows = cursor.execute(query)
                data = cursor.fetchall()
               
            except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                        print("Something is wrong with your user name or password")
                    elif err.errno == errorcode.ER_BAD_DB_ERROR:
                        print("Database does not exist")
                    else:
                        print('Log:')
                        print(err)
            else:
                    cursor.close()
            '''
            while (self.ui.comboBox.count() > 0):
                    self.ui.comboBox.removeItem(0)
            self.cargar_tablas()
            '''