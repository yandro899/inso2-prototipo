VENTANA_PRINCIPAL = "vp"

def GetUserMenuBar() -> list: 
    from globales import g_UsuarioActual
    return [
        ["Inicio", ["Menu Principal", "Cerrar sesión", "Salir"]], 
        ["Pedidos de adquisición", ["Crear nuevo pedido", "Revisar pedidos"]], 
        ["Usuarios", ["Ver usuarios"]],
        [g_UsuarioActual.Nombre, ["DNI {}".format(g_UsuarioActual.Dni)]]
        ]

def GetEstadoStr(cod):
    import json

    f = open("defs/estados.json")
    estados = json.load(f)

    return estados[cod]