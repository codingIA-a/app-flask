from ..config.mysqlconnect import connectToMySQL
import re 

class Usuario:
    db = 'ej_friend'
    def __init__(self, data):
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.edad = data['edad']
        self.fecha_nacimiento = data['fecha_nacimiento']
        self.contrasena = data['contrasena']
        self.email = data['email']

    #función para validar campos
    def validar_campos(self):
        errores = []
        if not re.match(r'^[a-zA-Z\u00E0-\u00FC\s]+$', self.nombre):
            errores.append('El nombre solo puede contener letras y espacios')
        if not re.match(r'^[a-zA-Z\u00E0-\u00FC\s]+$', self.apellido):
            errores.append('El apellido solo puede contener letras y espacios')

        return errores
    
    @classmethod
    def save(cls, data):
        usuario = cls(data)
        errores = usuario.validar_campos()
        if errores:
            return {'success':False, 'errors':errores}
        query = 'insert into usuarios (nombre,apellido,edad,fecha_nacimiento,contrasena,email) values (%(nombre)s,%(apellido)s,%(edad)s,%(fecha_nacimiento)s,%(contrasena)s, %(email)s ) ;'
        results = connectToMySQL('ej_friend').query_db(query, data)
        return {'success': True, 'user_id':results}
    
    #obtener email usuario
    @classmethod
    def get_by_email(cls, data):
        query = 'select * from usuarios where email = %(email)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])