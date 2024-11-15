class Usuario:
    """
    Clase que aloja a un usuario
    """


    def __init__(self, dni: str, passw: str, nombre: str, rol: int, area: int, legajo: str, mail: str) -> None:
        self.__dni = dni
        self.__passw = passw
        self.__nombre = nombre
        self.__rol = rol
        self.__area = area
        self.__legajo = legajo
        self.__mail = mail

    @classmethod
    def Vacio(self):
        return self("","","",0,0,"","")


    @property
    def Dni(self):
        """DNI del usuario"""
        return self.__dni
    
    @property
    def Password(self):
        """Contraseña del usuario"""
        return self.__passw
    
    @property
    def Nombre(self):
        """Nombre del usuario"""
        return self.__nombre
    
    @property
    def Rol(self):
        """
        Tipo de rol de usuario.

        * 0: Administrativo
        * 1: Directivo
        * 2: Secretario
        """
        return self.__rol
    
    @property
    def Area(self):
        """
        Tipo de rol de usuario.

        * 0: Contabilidad
        * 1: Compras y suministro
        """
        return self.__area
    
    @property
    def Legajo(self):
        """Legajo del usuario"""
        return self.__legajo
    
    @property
    def Mail(self):
        """Mail del usuario"""
        return self.__mail
    
    def EsContrasena(self, passw: str) -> bool:
        """Comprueba si la contraseña ingresada es correcta"""
        return self.Password == passw

class ListaUsuarios:
    """
    Aloja a todos los usuarios y hace operaciones comunes.
    """

    def __init__(self) -> None:
        self.__usuarios = []

    def AgregarUsuarioALista(self, usuario: Usuario):
        """
        Agregar un objeto Usuario a la lista.
        """
        self.__usuarios.append(usuario)

    def AutenticarUsuario(self, dni: str, passw: str) -> bool:
        from globales import setUsuarioActual

        usuario = self.BuscarUsuarioPorDNI(dni)
        
        if usuario is None:
            return False
        
        if usuario.EsContrasena(passw):
            setUsuarioActual(usuario)
            return True
        else:
            return False

    
    def BuscarUsuarioPorDNI(self, dni: str) -> Usuario:
        """
        Busca un usuario por DNI.

        Si lo encuentra, devuelve un objeto Usuario, sino devuelve None.
        """
        for usuario in self.__usuarios:
            if not isinstance(usuario, Usuario):
                continue
            
            if usuario.Dni == dni:
                return usuario
        
        return None
    
    def FormatearParaMuestra(self) -> list:
        import defs as D
        contenido = []
        for usr in self.__usuarios:
            if not isinstance(usr, Usuario):
                continue

            contenido.append({
                "dni" : usr.Dni, 
                "name" : usr.Nombre, 
                "rol" : usr.Rol, 
                "area" : usr.Area
                })
            
        return contenido

    def CargarUsuariosDB(self):
        """
        Carga datos desde la base de datos de mongo DB online
        """

        from pymongo import MongoClient
        from pymongo.cursor import Cursor

        # Reemplaza <username>, <password> y <cluster-url> con tus credenciales y URL del clúster
        client = MongoClient("mongodb+srv://41653328:7cptheLz4s2LlvsN@clusterinso2g6.rqpj2.mongodb.net/?retryWrites=true&w=majority&appName=ClusterINSO2G6")

        # Selecciona la base de datos
        db = client["inso2_SIGEAD"]

        # Selecciona la colección
        collection = db["usuarios"]

        # Iterar sobre todos los documentos de la colección
        for documento in collection.find():
            userclass = Usuario(
                documento.get("dni"), 
                documento.get("pass"), 
                documento.get("name"), 
                int(documento.get("rol")), 
                int(documento.get("area")), 
                documento.get("legajo"), 
                documento.get("mail")
                )
            self.__usuarios.append(userclass)
        