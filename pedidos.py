import FreeSimpleGUI as sg
from index import GoToWindow
from clases.clases_utiles import TiposUsuarios
import defs as D

def CrearPedido():
    from globales import g_UsuarioActual

    layout_01 = [
        [sg.Text("Datos del solicitante*:"), sg.Input(key="in_username", disabled=True, default_text="{} {}".format(g_UsuarioActual.Dni, g_UsuarioActual.Nombre))],
        [sg.Text("Código pedido*:"), sg.Input(key="in_codpedido")],
        [sg.Text("Sección*:"), sg.Input(key="Contaduria", disabled=True, default_text="Contaduria")],
        [sg.Text("Motivo*:")],
        [sg.Multiline(key="in_motivo", s=(None, 10))],
        [sg.Text("Observaciones:")],
        [sg.Multiline(key="in_observaciones", s=(None, 10))]
    ]

    layout_02 = [
        [sg.Button("Nuevo usuario", key="btn_newuser"), sg.Button("Generar pedido", key="btn_generarperdido")],
        [sg.Text("Lista de productos a pedir*:")],
        [sg.Input(key="in_c1", s=10), sg.Input(key="in_p1", s=40)],
        [sg.Input(key="in_c2", s=10), sg.Input(key="in_p2", s=40)],
        [sg.Input(key="in_c3", s=10), sg.Input(key="in_p3", s=40)],
        [sg.Input(key="in_c4", s=10), sg.Input(key="in_p4", s=40)],
        [sg.Input(key="in_c5", s=10), sg.Input(key="in_p5", s=40)],
    ]
    
    layout = [
        [sg.Menu([["Inicio", ["Menu Principal", "Cerrar sesión", "Salir"]], ["Pedidos de adquisición", ["Crear nuevo pedido", "Revisar pedidos"]], ["Usuarios", ["Ver usuarios"]]])],
        [sg.T("Nuevo Pedido")],
        [sg.Column(layout_01, p=0, vertical_alignment="top"), sg.VerticalSeparator(), sg.Column(layout_02, p=0, vertical_alignment="top")]
    ]

    window = sg.Window("Ventana principal", layout=layout)

    new_window = ""

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Salir':
            break

        if event == "Menu Principal":
            new_window = "vp"
            break

    window.close()

    GoToWindow(new_window)

def VerPedidos():
    import os
    from globales import g_ListaPedidos

    g_ListaPedidos.CargarPedidosDB()
    contenido = g_ListaPedidos.FormatearParaMuestra()

    layout = [
        [sg.Menu(D.GetUserMenuBar())],
        [
            sg.Button("Nuevo", key="btn_nuevopedido", visible=(TiposUsuarios.EsAdministrativo() and TiposUsuarios.EsDeContabilidad())), 
            sg.Button("Buscar", key="btn_buscarpedido"), 
            sg.Button("Resetear busqueda", key="btn_newbusqueda"),
            sg.Frame("Nro. Pedido", [[sg.Input(key="in_busqnro", s=10)]]),
            sg.Frame("Nombre del solicitante", [[sg.Input(key="in_busqnombre", s=25)]]),
            sg.Frame("Estado", [[sg.Input(key="in_busqest", s=10)]])
        ],
        [sg.Table(contenido, ['Datos del solicitante','Código','Estado','Creado','Concepto','Area actual'], num_rows=20, key="table_pedidos", enable_events=True)]
    ]

    window = sg.Window("Ver pedidos", layout=layout)

    new_window = ""

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Salir':
            break

        if event == "table_pedidos":
            selected_row_index = values['table_pedidos'][0]
            cod = contenido[selected_row_index][1]
            RevisarPedido(cod)

        if event == "btn_nuevopedido":
            new_window = "np"
            break

        if event == "Menu Principal":
            new_window = "vp"
            break

    window.close()

    GoToWindow(new_window)

def RevisarPedido(cod):
    import json

    f = open("pedidos/{}.json".format(cod))
    pedidojson = json.load(f)

    layout_01 = [
        [sg.Text("DETALLE PEDIDO")],
        [sg.Text("Fecha creacion: {}".format(pedidojson["fecha_creacion"]))],
        [sg.Text("Código: {}".format(pedidojson["cod"]))],
        [sg.Text("DNI: {}".format(pedidojson["dni"]))],
        [sg.Text("Apellido y nombre: {}".format(pedidojson["nombre"]))],
        [sg.Text("Estado actual: {}".format(D.GetEstadoStr(pedidojson["estado"])))],
        [sg.Text("Area actual: {}".format(pedidojson["area"]))],
    ]

    layout_02 = [
        [sg.Text("MOTIVO")],
        [sg.Multiline(pedidojson["motivo"], disabled=True, s=(None, 5))],
        [sg.Text("OBSERVACIONES")],
        [sg.Multiline(pedidojson["observaciones"], disabled=True, s=(None, 5))]
    ]

    concepto = []
    for prod in pedidojson["concepto"]:
        concepto.append([prod["cant"], prod["prod"]])

    # Adm cont
    # si 0 o 1 Anular
    # resto NADA

    # dir cont
    # si 1 Preaprovar o no
    # resto NADA

    # sec 
    # si 4 aprobar o no
    # resto NADA

    buttons = []

    if TiposUsuarios.EsDeContabilidad() or TiposUsuarios.EsSecretario():
        if TiposUsuarios.EsSecretario() and pedidojson["estado"] == "4":
            buttons = [sg.Button("Aprobar", k="btn_aprobar"), sg.Button("Anular", k="btn_anular")]
        elif TiposUsuarios.EsAdministrativo() and pedidojson["estado"] in ["0", "1"]:
            buttons = [sg.Button("Cancelar", k="btn_cancelar")]
        elif TiposUsuarios.EsDirectivo() and pedidojson["estado"] == "1":
            buttons = [sg.Button("Preaprobar", k="btn_preap"), sg.Button("Anular", k="btn_anular")]

    layout_03 = [
        [sg.Text("LISTA PEDIDOS")],
        [sg.Table(concepto, ['Cantidad','Producto'], num_rows=10)],
        buttons
    ]

    # Estados por celda
    # + 0, 1, 2, (11) Primera celda
    # + 3, 4 Segunda celda
    # + 5, (6) Tercera celda
    # + 7, 8 Cuarta celda
    # + 9 Quinta celda
    # + 10 Sexta celda

    seguimiento = []
    color_seguimiento = ["b", "b", "b", "b", "b", "b"]
    for seg in pedidojson["seguimiento"]:

        if seg["estado"] == "11":
            color_seguimiento[0] = "c"
            break

        if seg["estado"] == "6":
            color_seguimiento[0] = "c"
            color_seguimiento[1] = "c"
            color_seguimiento[2] = "c"
            break

        if seg["estado"] in ["0", "1", "2"]:
            color_seguimiento[0] = "a"

        if seg["estado"] in ["3", "4"]:
            color_seguimiento[1] = "a"

        if seg["estado"] in ["5"]:
            color_seguimiento[2] = "a"

        if seg["estado"] in ["7", "8"]:
            color_seguimiento[3] = "a"

        if seg["estado"] in ["9"]:
            color_seguimiento[4] = "a"

        if seg["estado"] in ["10"]:
            color_seguimiento[4] = "a"
            color_seguimiento[5] = "a"

        seguimiento.append([D.GetEstadoStr(seg["estado"]), seg["fecha_cambio"]])

    if TiposUsuarios.EsDeContabilidad() or TiposUsuarios.EsSecretario():
        parte_baja = [
            sg.Image(filename="imagenes/seguimiento/inso_seguimiento_1{}.png".format(color_seguimiento[0]), pad=(0,0)),
            sg.Image(filename="imagenes/seguimiento/inso_seguimiento_2{}.png".format(color_seguimiento[1]), pad=(0,0)),
            sg.Image(filename="imagenes/seguimiento/inso_seguimiento_3{}.png".format(color_seguimiento[2]), pad=(0,0)),
            sg.Image(filename="imagenes/seguimiento/inso_seguimiento_4{}.png".format(color_seguimiento[3]), pad=(0,0)),
            sg.Image(filename="imagenes/seguimiento/inso_seguimiento_5{}.png".format(color_seguimiento[4]), pad=(0,0)),
            sg.Image(filename="imagenes/seguimiento/inso_seguimiento_6{}.png".format(color_seguimiento[5]), pad=(0,0)),
            sg.Table(seguimiento, ['Fecha y Hora','Estado'], num_rows=8)
        ]
    elif TiposUsuarios.EsDeCompras():
        parte_baja = [
            [sg.Column(layout=[
                [sg.Text("Nombre y apellido del destinatario*:"), sg.Input(key="in_destname")],
                [sg.Text("DNI del destinatario*:"), sg.Input(key="in_destdni")],
                [sg.Button("Entregar pedido", k="btn_entregar"), sg.Button("Cambiar estado a Pedido a Proveedor", k="btn_proveedor"), sg.Button("Cancelar", k="btn_cancelar")]
            ], p=0)],
        ]

    layout = [
        [sg.Column(layout=layout_01, p=0), sg.Column(layout=layout_02, p=0), sg.Column(layout=layout_03, p=0)],
        parte_baja
    ]

    window = sg.Window("Ver pedido {}".format(pedidojson["cod"]), layout=layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

    window.close()
