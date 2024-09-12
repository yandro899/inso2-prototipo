class PedidoAdquisicion:
    """
    Clase que guarda los datos de un pedido de adquisicion.
    """
    def __init__(self, id: str, fecha_hora_gen: str, dni: str, motivo: str) -> None:
        from globales import g_ListaUsuarios

        self.__id = id
        self.__fechaHoraGen = fecha_hora_gen
        self.__usuario = g_ListaUsuarios.BuscarUsuarioPorDNI(dni)
        self.__motivo = motivo
        self.__observaciones = ""
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
    def Usuario(self):
        """Obtener usuario que creo el pedido de adquisicion"""
        return self.__usuario
    
    @property
    def Motivo(self):
        """Obtener motivo del pedido de adquisicion"""
        return self.__motivo
    
    @property
    def Observaciones(self):
        """Obtener observaciones del pedido de adquisicion"""
        return self.__observaciones
    
    @property
    def UltimoSeguimiento(self):
        """Obtener ultimo seguimiento del pedido de adquisicion"""
        seguimiento = self.__seguimientos[len(self.__seguimientos)-1]
        
        if not isinstance(seguimiento, Seguimiento):
            return None
        
        return seguimiento
    
    @Observaciones.setter
    def Observaciones(self, observ: str):
        self.__observaciones = observ

    @property
    def PrimerConcepto(self):
        """Obtener primer concepto del pedido de adquisicion"""
        concepto = self.__conceptos[0]
        
        if not isinstance(concepto, Concepto):
            return None
        
        return concepto
    
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
        self.__codProducto = ""
        self.__nombreProducto = nombreProducto
        self.__cantidad = cantidad

    @classmethod    
    def Codigo(self, codigoProducto: str, cantidad: int):
        self.__nombreProducto = ""
        self.__cantidad = cantidad
        self.__codProducto = codigoProducto
        return self

    @property
    def NombreProducto(self):
        """Nombre del producto"""
        return self.__nombreProducto
    
    @property
    def CodigoProducto(self):
        """Codigo del producto"""
        return self.__codProducto
    
    @property
    def CantidadProducto(self):
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
    
    def BuscarPedidoAdquision(self, id: str) -> PedidoAdquisicion:
        """
        Buscar pedido por ID.

        Devuelve un objeto Pedido si lo encuentra. None si no lo encuentra.
        """
        for pedido in self.__pedidos:
            if not isinstance(pedido, PedidoAdquisicion):
                continue
            
            if pedido.Id == id:
                return pedido
        
        return None
    
    def FormatearParaMuestra(self) -> list:
        import defs as D
        contenido = []
        for pedido in self.__pedidos:
            if not isinstance(pedido, PedidoAdquisicion):
                continue

            contenido.append([
                "{} {}".format(pedido.Usuario.Dni, pedido.Usuario.Nombre), 
                pedido.Id, 
                D.GetEstadoStr(pedido.UltimoSeguimiento.Estado), 
                pedido.UltimoSeguimiento.FechaHoraEstado, 
                "{}x {}...".format(pedido.PrimerConcepto.CantidadProducto, pedido.PrimerConcepto.NombreProducto), 
                "Contabilidad"
                ])
            
        return contenido


    def CargarPedidosDB(self):
        """
        TODO: Implementar DB vagos.
        """
        import os
        import json
        
        self.__pedidos.clear()

        # Iterar sobre todos los archivos en la carpeta
        carpeta = "pedidos"
        for archivo in os.listdir(carpeta):
            if archivo.endswith('.json'):
                ruta_archivo = os.path.join(carpeta, archivo)

                f = open(ruta_archivo)
                pedidojson = json.load(f)
                pedido = PedidoAdquisicion(pedidojson["cod"], pedidojson["fecha_creacion"], pedidojson["dni"], pedidojson["motivo"])

                for concepto_json in pedidojson["concepto"]:
                    concepto = Concepto(concepto_json["prod"], concepto_json["cant"])
                    pedido.ListaConceptos.append(concepto)
                
                for seguimiento_json in pedidojson["seguimiento"]:
                    seguimiento = Seguimiento(seguimiento_json["estado"], seguimiento_json["fecha_cambio"], pedido)
                    pedido.ListaSeguimientos.append(seguimiento)
                
                self.__pedidos.append(pedido)
    