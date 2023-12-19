from ..config.mysqlconnect import connectToMySQL
import re 

class Usuario:
    def __init__(self, data):
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.edad = data['edad']
        self.fecha_nacimiento = data['fecha_nacimiento']
        self.contrasena = data['contrasena']

    #función para validar campos
    def validar_campos(self):
        errores = []
        if not re.match(r'^[a-zA-ZñÑ\s]+$', self.nombre):
            errores.append('El nombre solo puede contener letras y espacios')
        if not re.match(r'^[a-zA-ZñÑ\s]+$', self.apellido):
            errores.append('El apellido solo puede contener letras y espacios')

        return errores
    
    @classmethod
    def save(cls, data):
        usuario = cls(data)
        errores = usuario.validar_campos()
        if errores:
            return {'success':False, 'errors':errores}
        query = 'insert into usuarios (nombre,apellido,edad,fecha_nacimiento,contrasena) values (%(nombre)s,%(apellido)s,%(edad)s,%(fecha_nacimiento)s,%(contrasena)s ) ;'
        results = connectToMySQL('ej_friend').query_db(query, data)
        return {'success': True, 'user_id':results}