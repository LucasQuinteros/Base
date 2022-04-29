import mysql.connector

class item_Prod ():
        def __init__(self, ProductName, ProductID = '', Cantidad = 0, Estado = '', Observacion = '', Nserie = '',
                Assy = '',Descripcion = '', Categoria = '',UbiExac = '',UbiFis = '',SeccEqui = '')-> None:
            
                self.ProductID = ProductID
                self.ProductName = ProductName
                self.Cantidad = Cantidad
                self.Estado = Estado
                self.Observacion = Observacion
                self.Nserie = Nserie
                self.PartNum = Assy
                self.Descrip = Descripcion
                self.Cat = Categoria
                self.UbiExac = UbiExac
                self.UbiFis = UbiFis
                self.SeccEquip = SeccEqui

                self.Movimientos = list()

        def __init__(self, row ) -> None:
            
                self.ProductID = row[0]
                self.ProductName = row[1]
                self.Cantidad = row[2]
                self.Estado = row[3]
                self.Observacion = row[4]
                self.Nserie = row[5]
                self.PartNum = row[6]
                self.Descrip = row[7]
                self.Cat = row[8]
                self.UbiExac = row[9]
                self.UbiFis = row[10]
                self.SeccEquip = row[11]

                self.Movimientos = list()

    

class item_Mov():
        def __init__(self, *args):
                self.ID = ''
                self.Date = ''
                self.Descr= ''
                self.Urec = ''
                self.Usold= ''
                self.Ush = ''
                self.Usto = ''
                self.Ori = ''
                self.Dest= ''
                self.NumMov = ''
                if isinstance(args[0],mysql.connector.CMySQLConnection):
                        self.Cnx = args[0]
                        
                elif isinstance(args[0], list):
                        
                        self.ID =   args[0][0]
                        self.Date = args[0][1]
                        self.Descr = args[0][2]
                        self.Urec = args[0][3]
                        self.Usold = args[0][4]
                        self.Ush = args[0][5]
                        self.Usto = args[0][6]
                        self.Ori = args[0][7]
                        self.Dest = args[0][8]
                        self.NumMov = args[0][9]
                        
        '''                
        def __init__(self,cnx , ID = '',
                     Date = '',Descr = '',Urec = 0,Usold = 0,Ush = 0,Usto = 0,Ori = '',
                     Dest = '',NumMov = ''):
                self.Cnx = cnx
                self.ID = ID
                self.Date = Date
                self.Descr = Descr
                self.Urec = Urec
                self.Usold = Usold
                self.Ush = Ush
                self.Usto = Usto
                self.Ori = Ori
                self.Dest = Dest
                self.NumMov = NumMov

        def __init__(self, row: list):
                self.ID = row[0]
                self.Date = row[1]
                self.Descr = row[2]
                self.Urec = row[3]
                self.Usold = row[4]
                self.Ush = row[5]
                self.Usto = row[6]
                self.Ori = row[7]
                self.Dest = row[8]
                self.NumMov = row[9]
'''