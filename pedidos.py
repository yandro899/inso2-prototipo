import FreeSimpleGUI as sg
from index import GoToWindow
from clases.clases_utiles import TiposUsuarios
from clases.clases_pedidos import PedidoAdquisicion
import defs as D

def CrearPedido():
    from datetime import datetime
    from globales import g_UsuarioActual, g_ListaPedidos
    from clases.clases_pedidos import PedidoAdquisicion, Concepto, Seguimiento

    layout_01 = [
        [sg.Text("Datos del solicitante*:"), sg.Input(key="in_username", disabled=True, default_text="{} {}".format(g_UsuarioActual.Dni, g_UsuarioActual.Nombre))],
        [sg.Text("Código pedido*:"), sg.Input(key="in_codpedido", disabled=True, default_text=g_ListaPedidos.ObtenerNuevoIDPedido())],
        [sg.Text("Sección*:"), sg.Input(key="Contaduria", disabled=True, default_text="Contaduria")],
        [sg.Text("Motivo*:")],
        [sg.Multiline(key="in_motivo", s=(None, 10))],
        [sg.Text("Observaciones:")],
        [sg.Multiline(key="in_observaciones", s=(None, 10))]
    ]

    layout_02 = [
        [sg.Button("Nuevo usuario", key="btn_newuser"), sg.Button("Generar pedido", key="btn_generarperdido")],
        [sg.Text("Lista de productos a pedir*:")],
        [sg.Text("Cantidad - Producto"), sg.Button("+", key="btn_crear_fila")],
        [sg.Text("1"), sg.Input(key="in_c1", s=10), sg.Input(key="in_p1", s=40)]
    ]
    
    layout = [
        [sg.Menu(D.GetUserMenuBar())],
        [sg.T("Nuevo Pedido")],
        [sg.Column(layout_01, p=0, vertical_alignment="top"), sg.VerticalSeparator(), sg.Column(layout_02, p=0, vertical_alignment="top")]
    ]

    window = sg.Window("Ventana principal", layout=layout)

    new_window = ""
    c = 1
    MAX_ROWS = 14

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Salir':
            break

        if event == "btn_crear_fila":
            if c >= MAX_ROWS:
                continue

            window.extend_layout(window['in_c1'].ParentContainer, [[sg.Text(f"{c+1}"), sg.Input(key=f"in_c{c+1}", s=10), sg.Input(key=f"in_p{c+1}", s=40)]])
            c += 1
            continue

        if event == "btn_generarperdido":
            # Controlar que la carga sea correcta
            if values["in_motivo"] == "":
                sg.popup("¡El motivo es obligatorio!")
                continue
            elif values["in_motivo"] == "":
                sg.popup("¡El motivo es obligatorio!")
                continue

            # Primero crear el pedido
            pedido = PedidoAdquisicion(g_ListaPedidos.ObtenerNuevoIDPedido(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), g_UsuarioActual.Dni, values["in_motivo"])
            pedido.Observaciones = values["in_observaciones"]
            # crear un seguimiento
            pedido.ListaSeguimientos.append(Seguimiento(
                1, 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                pedido
            ))
            error = False
            # guardar conceptos
            for i in range(1,c+1):
                nombre_concepto = values["in_p{}".format(i)]
                cant_concepto = str(values["in_c{}".format(i)])

                if len(cant_concepto) != 0 and len(nombre_concepto) != 0:
                    if not cant_concepto.isdigit():
                        sg.popup("¡Ingrese numeros en la cantidad!")
                        error = True
                        break

                    cant_concepto_int = int(cant_concepto)
                    if (cant_concepto_int <= 0):
                        sg.popup("¡No ingrese numeros menores o iguales a cero!")
                        error = True
                        break
                    
                    pedido.ListaConceptos.append(Concepto(
                        nombre_concepto,
                        cant_concepto_int
                    ))
                else:
                    error = True
                    sg.popup("¡No deje campos en blanco!")
                    break

            if error:
                continue

            # luego guardarlo en la lista
            g_ListaPedidos.AgregarPedidoALista(pedido)
            # guardarlo en DB
            g_ListaPedidos.GuardarPedidoADB(pedido)
            # mostrar el pedido
            new_window = "rp"
            # Avisar creacion de pedido
            sg.popup("¡El pedido se ha creado correctamente!")
            break

        if event == "Menu Principal":
            new_window = "vp"
            break

    window.close()

    GoToWindow(new_window)

def VerPedidos():
    from globales import g_ListaPedidos

    g_ListaPedidos.CargarPedidosDB()
    contenido = g_ListaPedidos.FormatearParaMuestra()

    if (TiposUsuarios.EsDirectivo() and TiposUsuarios.EsDeContabilidad()):
        new_contenido = contenido.copy()
        for prod in contenido:
            if prod[2] != D.GetEstadoStr("1"):
                new_contenido.remove(prod)
        contenido = new_contenido
    elif (TiposUsuarios.EsDeCompras()):
        new_contenido = contenido.copy()
        for prod in contenido:
            if prod[2] != D.GetEstadoStr("8") and prod[2] != D.GetEstadoStr("9") and prod[2] != D.GetEstadoStr("10"):
                new_contenido.remove(prod)
        contenido = new_contenido
    elif (TiposUsuarios.EsSecretario()):
        new_contenido = contenido.copy()
        for prod in contenido:
            if prod[2] != D.GetEstadoStr("2"):
                new_contenido.remove(prod)
        contenido = new_contenido

    contenido_colors = []

    for x in range(len(contenido)):
        if contenido[x][2] == D.GetEstadoStr(11):
            contenido_colors.append((x, "white", "black"))
        elif contenido[x][2] == D.GetEstadoStr(1):
            contenido_colors.append((x, "white", "#F58634"))
        elif contenido[x][2] == D.GetEstadoStr(2):
            contenido_colors.append((x, "black", "#FFC34C"))
        elif contenido[x][2] == D.GetEstadoStr(5):
            contenido_colors.append((x, "black", "#51FF00"))
        elif contenido[x][2] == D.GetEstadoStr(6):
            contenido_colors.append((x, "white", "red"))

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
        [sg.Table(
            contenido, 
            ['Datos del solicitante','Código','Estado','Creado','Concepto','Area actual'], 
            num_rows=20, 
            key="table_pedidos",
            row_colors=contenido_colors,
            enable_events=True
            )]
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
            new_window = "rp"
            RevisarPedido(cod)
            break

        if event == "btn_nuevopedido":
            new_window = "np"
            break

        if event == "Menu Principal":
            new_window = "vp"
            break

    window.close()

    GoToWindow(new_window)

def EstructuraRevisarPedido(pedido: PedidoAdquisicion) -> list:
    from clases.clases_pedidos import Concepto, Seguimiento

    layout_01 = [
        [sg.Text("DETALLE PEDIDO")],
        [sg.Text("Fecha creacion: {}".format(pedido.FechaGeneracion))],
        [sg.Text("Código: {}".format(pedido.Id))],
        [sg.Text("DNI: {}".format(pedido.Usuario.Dni))],
        [sg.Text("Apellido y nombre: {}".format(pedido.Usuario.Nombre))],
        [sg.Text("Estado actual: {}".format(D.GetEstadoStr(pedido.UltimoSeguimiento.Estado)))],
        [sg.Text("Area actual: {}".format("Contabilidad"))],
    ]

    layout_02 = [
        [sg.Text("MOTIVO")],
        [sg.Multiline(pedido.Motivo, disabled=True, s=(None, 5))],
        [sg.Text("OBSERVACIONES")],
        [sg.Multiline(pedido.Observaciones, disabled=True, s=(None, 5))]
    ]

    concepto = []
    for prod in pedido.ListaConceptos:
        if not isinstance(prod, Concepto):
            continue

        concepto.append([prod.CantidadProducto, prod.NombreProducto])

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
        if TiposUsuarios.EsSecretario() and pedido.UltimoSeguimiento.Estado in [2, 3, 4]:
            buttons = [sg.Button("Aprobar", k="btn_aprobar"), sg.Button("Anular", k="btn_anular")]
        elif TiposUsuarios.EsAdministrativo() and pedido.UltimoSeguimiento.Estado in [0, 1]:
            buttons = [sg.Button("Cancelar", k="btn_cancelar")]
        elif TiposUsuarios.EsDirectivo() and pedido.UltimoSeguimiento.Estado == 1:
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
    for seg in pedido.ListaSeguimientos:
        if not isinstance(seg, Seguimiento):
            continue

        seguimiento.append([D.GetEstadoStr(seg.Estado), seg.FechaHoraEstado])
        
        if seg.Estado == 11:
            color_seguimiento[0] = "c"
            for i in range(len(color_seguimiento)):
                if color_seguimiento[i] == "a":
                    color_seguimiento[i] = "c"
            break

        if seg.Estado == 6:
            color_seguimiento[0] = "c"
            break

        if seg.Estado in [0, 1]:
            color_seguimiento[0] = "a"

        if seg.Estado in [2, 3, 4]:
            color_seguimiento[1] = "a"

        if seg.Estado in [5]:
            color_seguimiento[2] = "a"

        if seg.Estado in [7, 8]:
            color_seguimiento[3] = "a"

        if seg.Estado in [9]:
            color_seguimiento[4] = "a"

        if seg.Estado in [10]:
            color_seguimiento[4] = "a"
            color_seguimiento[5] = "a"


    if TiposUsuarios.EsDeContabilidad() or TiposUsuarios.EsSecretario():
        parte_baja = [
            sg.Image(filename="imagenes/seguimiento/inso_seguimiento_1{}.png".format(color_seguimiento[0]), pad=(0,0)),
            sg.Image(filename="imagenes/seguimiento/inso_seguimiento_2{}.png".format(color_seguimiento[1]), pad=(0,0)),
            sg.Image(filename="imagenes/seguimiento/inso_seguimiento_3{}.png".format(color_seguimiento[2]), pad=(0,0)),
            sg.Image(filename="imagenes/seguimiento/inso_seguimiento_4{}.png".format(color_seguimiento[3]), pad=(0,0)),
            sg.Image(filename="imagenes/seguimiento/inso_seguimiento_5{}.png".format(color_seguimiento[4]), pad=(0,0)),
            sg.Image(filename="imagenes/seguimiento/inso_seguimiento_6{}.png".format(color_seguimiento[5]), pad=(0,0)),
            sg.Table(seguimiento, ['Estado', 'Fecha y Hora'], num_rows=8)
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

    return layout

def RevisarPedido(cod):
    from globales import g_ListaPedidos

    pedido = g_ListaPedidos.BuscarPedidoAdquision(cod)

    layout = EstructuraRevisarPedido(pedido)

    window = sg.Window("Ver pedido {}".format(pedido.Id), layout=layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event == "btn_preap":
            result = sg.popup_ok_cancel("¿Estas seguro de preaprobar este pedido?")

            if result == None or result == "Cancel":
                break
            elif result == "OK":
                pedido.PreaprobarPedido()
                g_ListaPedidos.GuardarPedidoADB(pedido)
                sg.popup("¡Pedido preaprobado con exito!")
                break

        if event == "btn_aprobar":
            result = sg.popup_ok_cancel("¿Estas seguro de aprobar este pedido?")

            if result == None or result == "Cancel":
                break
            elif result == "OK":
                pedido.AprobarPedido()
                g_ListaPedidos.GuardarPedidoADB(pedido)
                sg.popup("¡Pedido aprobado con exito!")
                break

        if event == "btn_anular":
            result = sg.popup_ok_cancel("¿Estas seguro de anular este pedido?")

            if result == None or result == "Cancel":
                break
            elif result == "OK":
                pedido.AnularPedido()
                g_ListaPedidos.GuardarPedidoADB(pedido)
                sg.popup("¡Pedido anulado con exito!")
                break

        if event == "btn_cancelar":
            result = sg.popup_ok_cancel("¿Estas seguro de cancelar este pedido?")

            if result == None or result == "Cancel":
                break
            elif result == "OK":
                pedido.CancelarPedido()
                g_ListaPedidos.GuardarPedidoADB(pedido)
                sg.popup("¡Pedido cancelado con exito!")
                break

    window.close()
