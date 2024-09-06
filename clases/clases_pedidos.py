class PedidoAdquisicion:
    """
    Clase que guarda los datos de un pedido de adquisicion.
    """
    def __init__(self, id: str, fecha_hora_gen: str, dni: str) -> None:
        from globales import g_ListaUsuarios

        self.__id = id
        self.__fechaHoraGen = fecha_hora_gen
        self.__usuario = g_ListaUsuarios.BuscarUsuarioPorDNI(dni)
        self.__seguimientos = []
        self.__conceptos = []

    @property
    def Id(self):
        """ID del pedido de adquisicion"""
        return self.__id
    
    @property
    def FechaGeneracion(self):
        """Fecha y hora de generacion del pedido de adquisicion"""
        return self.__fechaHoraGen
    
    @property
    def GetUsuario(self):
        """Obtener usuario que creo el pedido de adquisicion"""
        return self.__usuario
    
    @property
    def ListaSeguimientos(self):
        """Lista de seguimientos"""
        return self.__seguimientos
    
    @property
    def ListaConceptos(self):
        """Lista de conceptos"""
        return self.__conceptos
    
class Concepto:
    """
    Clase que aloja los conceptos.
    """

    def __init__(self, nombreProducto: str, cantidad: int) -> None:
        self.__nombreProducto = nombreProducto
        self.__cantidad = cantidad

    def __init__(self, codProducto: str, cantidad: int) -> None:
        self.__codProducto = codProducto
        self.__cantidad = cantidad

    @property
    def NombreProducto(self):
        """Nombre del producto"""
        return self.__nombreProducto
    
    @property
    def CodigoProducto(self):
        """Codigo del producto"""
        return self.__codProducto
    
    @property
    def NombreProducto(self):
        """Cantidad del producto"""
        return self.__cantidad
    

class Seguimiento:
    """
    Clase que almacena el seguimiento.
    """
    def __init__(self, estado: int, fechaHora: str, pedido: PedidoAdquisicion) -> None:
        self.__estado = estado
        self.__fechaHoraEstado = fechaHora
        self.__pedido = pedido

    @property
    def Estado(self):
        """Estado del seguimiento"""
        return self.__estado
    
    @property
    def FechaHoraEstado(self):
        """Fecha y hora de este estado"""
        return self.__fechaHoraEstado
    
    @property
    def Pedido(self):
        """Pedido relacionado a este seguimiento"""
        return self.__pedido

class ListaPedidos:
    """
    Aloja a todos los los pedidos de adquisicion y operaciones comunes.
    """

    def __init__(self) -> None:
        self.__pedidos = []

    def AgregarPedidoALista(self, pedido: PedidoAdquisicion):
        """Agrega un pedido a la lista"""
        self.__pedidos.append(pedido)
    
    def BuscarPedidoAdquision(self, id: str) -> PedidoAdquisicion | None:
        """
        Buscar pedido por ID.

        Devuelve un objeto Pedido si lo encuentra. None si no lo encuentra.
        """
        for pedido in self.__pedidos:
            if not isinstance(pedido, PedidoAdquisicion):
                continue
            
            if pedido.Dni == id:
                return pedido
        
        return None

    def CargarPedidosDB(self):
        """
        TODO: Implementar DB vagos.
        """
        pass
    