import FreeSimpleGUI as sg
from clases.clases_utiles import TiposUsuarios
from defs import GetUserMenuBar

def VentanaPrincipal():
    layout = [
        [sg.Menu(GetUserMenuBar())],
        [
            sg.Button(image_filename="imagenes/inso7.png", image_size=(256,256), key="btn_nuevopedido", visible=(TiposUsuarios.EsDeContabilidad() and TiposUsuarios.EsAdministrativo())), 
            sg.Button(image_filename="imagenes/inso6.png", image_size=(256,256), key="btn_revisarpedidos", visible=(not (TiposUsuarios.EsDeCompras() and TiposUsuarios.EsDirectivo())))
            ],
        [
            sg.Button(image_filename="imagenes/inso5.png", image_size=(256,256), key="btn_usuarios"),
            sg.Button(image_filename="imagenes/inso4.png", image_size=(256,256), key="btn_verproductos", visible=(TiposUsuarios.EsDeCompras() and TiposUsuarios.EsAdministrativo())),
            sg.Button(image_filename="imagenes/inso2.png", image_size=(256,256), key="btn_devproductos", visible=(TiposUsuarios.EsDeCompras() and TiposUsuarios.EsAdministrativo()))
        ]
    ]

    window = sg.Window("Ventana principal", layout=layout)

    new_window = ""

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Salir':
            break

        if event == "btn_nuevopedido":
            new_window = "np"
            break

        if event == "btn_revisarpedidos":
            new_window = "rp"
            break

        if event == "btn_usuarios":
            new_window = "u"
            break

        if event == "btn_verproductos":
            new_window = "vprod"
            break

        if event == "btn_devproductos":
            new_window = "dprod"
            break

    window.close()

    # if new_window == "np":
    #     C.NuevoPedido()
    # elif new_window == "rp":
    #     P.VerPedidos()
    # elif new_window == "vprod":
    #     C.VerProductos()
    # elif new_window == "dprod":
    #     C.DevolverProductos()
    # elif new_window == "u":
    #     C.VerUsuarios()