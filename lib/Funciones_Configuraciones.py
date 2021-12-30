



from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode

from qts.Ui_ventana_configuraciones import Ui_Form


class clase_configuraciones(QWidget):
        procCargar = QtCore.pyqtSignal(dict)
        procEstado = QtCore.pyqtSignal(bool)
        
        def __init__(self):
                super().__init__()
                self.widget = QWidget()
                self.ui = Ui_Form()
                self.ui.setupUi(self.widget)
                self.data = ''
                self.getsettingsvalues()
                

                self.ui.pushButton.clicked.connect(self.Prueba_conexion)
                self.ui.pushButton_3.clicked.connect(self.Guardar_datos)
        def getsettingsvalues(self):
                self.settings_conn = QtCore.QSettings('Base','Variables')
                self.aux = self.settings_conn.value('dict') 
                try:
                        self.ui.lineEdit.setText( self.aux['user'] )
                        self.ui.lineEdit_2.setText(self.aux['password'] )
                        self.ui.lineEdit_3.setText(self.aux['host'] )
                        self.ui.lineEdit_4.setText(self.aux['database'] )
                except:
                        self.connector = {}
                        self.connector['user'] = 'root'
                        self.connector['password'] = '12345678'
                        self.connector['host'] = '10.0.0.50'
                        self.connector['database'] = 'movedb'
                        self.ui.lineEdit.setText(self.connector['user'] )
                        self.ui.lineEdit_2.setText(self.connector['password'] )
                        self.ui.lineEdit_3.setText(self.connector['host'] )
                        self.ui.lineEdit_4.setText(self.connector['database'] )
                else:
                        self.connector = self.aux



        def Guardar_datos(self):
                self.connector['user'] = self.ui.lineEdit.text()
                self.connector['password'] = self.ui.lineEdit_2.text()
                self.connector['host'] = self.ui.lineEdit_3.text()
                self.connector['database'] = self.ui.lineEdit_4.text()
                self.settings_conn.setValue('dict',self.connector)
                self.procCargar.emit(self.connector)
                

        def Prueba_conexion(self):
                
                try:
                        self.cnx = mysql.connector.connect(user= self.ui.lineEdit.text(), 
                                                        password=self.ui.lineEdit_2.text(),
                                                        host=    self.ui.lineEdit_3.text(),
                                                        database= self.ui.lineEdit_4.text())
                        cursor = self.cnx.cursor()
                except mysql.connector.Error as err:
                        self.procEstado.emit(False)
                        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                                print("Something is wrong with your user name or password")
                        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                                print("Database does not exist")
                        else:
                                print(err)
                        QMessageBox.critical(self, 'Error de conexion ', str(err))
                else:
                        self.procEstado.emit(True)
                        QMessageBox.information(self, 'Info', 'Conexion Exitosa')
                        cursor.close()