



class Objmov():
        def __init__(self, cnx, id, date, descr = '', uniIngre = '0', uniEgre = '0', uniDesechadas = '',
                     uniStock = '', numberMov = '',origen = '', destino = '') -> None:
            self.cnx = cnx
            self.id = id
            self.date = date
            self.desc = descr
            self.uniIngre = uniIngre
            self.uniEgre = uniEgre
            self.uniDesechadas = uniDesechadas
            self.uniStock = uniStock
            self.numberMov = numberMov
            self.origen = origen
            self.destino = destino
            
        