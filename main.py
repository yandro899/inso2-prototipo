from inicio_sesion import VentanaInicioSesion
from globales import g_ListaUsuarios, g_ListaPedidos
from ventana_principal import VentanaPrincipal

g_ListaUsuarios.CargarUsuariosDB()

if VentanaInicioSesion():
    g_ListaPedidos.CargarPedidosDB()
    VentanaPrincipal()