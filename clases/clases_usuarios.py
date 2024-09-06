class Usuario:
    """
    Clase que aloja a un usuario
    """

    def __init__(self) -> None:
        self.__dni = ""
        self.__passw = ""
        self.__nombre = ""
        self.__rol = 0
        self.__area = 0
        self.__legajo = ""
        self.__mail = ""

    def __init__(self, dni: str, passw: str, nombre: str, rol: int, area: int, legajo: str, mail: str) -> None:
        self.__dni = dni
        self.__passw = passw
        self.__nombre = nombre
        self.__rol = rol
        self.__area = area
        self.__legajo = legajo
        self.__mail = mail

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

    def AutenticarUsuario(self, dni: str, passw: str):
        from globales import setUsuarioActual
        usuario = self.BuscarUsuarioPorDNI(dni)
        
        if usuario is None:
            return False
        
        if usuario.EsContrasena(passw):
            setUsuarioActual(usuario)
            return True
        else:
            return False

    
    def BuscarUsuarioPorDNI(self, dni: str) -> Usuario | None:
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

    def CargarUsuariosDB(self):
        """
        TODO: debe cargar todos los usuarios de alguna base de datos.
        """
        pass