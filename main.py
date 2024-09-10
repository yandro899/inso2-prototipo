from inicio_sesion import VentanaInicioSesion
from globales import g_ListaUsuarios
from ventana_principal import VentanaPrincipal

g_ListaUsuarios.CargarUsuariosDB()

if VentanaInicioSesion():
    print("se inicio sesion")
    VentanaPrincipal()
else:
    print("no")