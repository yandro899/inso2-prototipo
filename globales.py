from clases.clases_usuarios import ListaUsuarios, Usuario
from clases.clases_pedidos import ListaPedidos

g_ListaUsuarios = ListaUsuarios()
"""Objeto global ListaUsuarios"""
g_ListaPedidos = ListaPedidos()
"""Objeto global ListaPedidos"""
g_UsuarioActual = Usuario.Vacio()
"""Usuario actual"""

def setUsuarioActual(usuario: Usuario):
    global g_UsuarioActual
    """
    Setea este usuario como el usuario que inició sesion.
    """
    g_UsuarioActual = usuario
