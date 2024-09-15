VENTANA_PRINCIPAL = "vp"

def GetUserMenuBar() -> list: 
    from globales import g_UsuarioActual
    return [
        ["Inicio", ["Menu Principal", "Cerrar sesión", "Salir"]], 
        ["Pedidos de adquisición", ["Crear nuevo pedido", "Revisar pedidos"]], 
        ["Usuarios", ["Ver usuarios"]],
        [g_UsuarioActual.Nombre, ["DNI {}".format(g_UsuarioActual.Dni)]],
        ObtenerNotificaciones()
        ]

def GetEstadoStr(cod: int) -> str:
    import json

    f = open("defs/estados.json")
    estados = json.load(f)

    return estados[str(cod)]

def ObtenerNotificaciones() -> list:
    """
    Obtiene notificaciones de pedidos con cambio de estado.
    """
    from globales import g_ListaPedidos
    from clases.clases_utiles import TiposUsuarios

    # Directivo de contabilidad
    if TiposUsuarios.EsDirectivo() and TiposUsuarios.EsDeContabilidad():
        pedidos = g_ListaPedidos.BuscarPorEstado([1])
        if len(pedidos) != 0:
            return ["HAY NUEVAS NOTIFICACIONES", ["Tiene nuevos pedidos para revisar::vp"]]
        
    # Secretario
    if TiposUsuarios.EsSecretario():
        pedidos = g_ListaPedidos.BuscarPorEstado([2])
        if len(pedidos) != 0:
            return ["HAY NUEVAS NOTIFICACIONES", ["Tiene nuevos pedidos para revisar::vp"]]
        
    return ["Sin notificaciones"]
