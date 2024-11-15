from pymongo import MongoClient
from pymongo.database import Database
from clases.clases_usuarios import ListaUsuarios, Usuario
from clases.clases_pedidos import ListaPedidos

g_ListaUsuarios = ListaUsuarios()
"""Objeto global ListaUsuarios"""
g_ListaPedidos = ListaPedidos()
"""Objeto global ListaPedidos"""
g_UsuarioActual = Usuario.Vacio()
"""Usuario actual"""

def conectarDB() -> Database:
    # Reemplaza <username>, <password> y <cluster-url> con tus credenciales y URL del clúster
    client = MongoClient("mongodb+srv://41653328:7cptheLz4s2LlvsN@clusterinso2g6.rqpj2.mongodb.net/?retryWrites=true&w=majority&appName=ClusterINSO2G6")

    # Selecciona la base de datos
    db = client["inso2_SIGEAD"]

    return db

g_MongoDBClient = conectarDB()
"""Conexion a la base de datos"""

def setUsuarioActual(usuario: Usuario):
    global g_UsuarioActual
    """
    Setea este usuario como el usuario que inició sesion.
    """
    g_UsuarioActual = usuario
