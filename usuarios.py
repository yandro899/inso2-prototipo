import FreeSimpleGUI as sg
import defs as D

def VerUsuarios():
    from globales import g_ListaUsuarios
    from clases.clases_utiles import TiposUsuarios
    from index import GoToWindow

    treedata = sg.TreeData()

    for usr in g_ListaUsuarios.FormatearParaMuestra():
        
        if usr["area"] == 1:
            area = "COMP"
        else:
            area = "CONT"

        if usr["rol"] == 2:
            treedata.Insert("", '_S_', 'Sec. Hac: {}'.format(usr["name"]), [usr["dni"]])
        elif usr["rol"] == 1:
            treedata.Insert("_S_", '_D{}_'.format(usr["area"]), 'Dir. {}: {}'.format(area, usr["name"]), [usr["dni"]])
        elif usr["rol"] == 0:
            treedata.Insert('_D{}_'.format(usr["area"]), '_A{}_'.format(usr["area"]), 'Adm. {}: {}'.format(area, usr["name"]), [usr["dni"]])

    layout_01 = [
        [sg.Tree(treedata, headings=["DNI"], col0_width=40, auto_size_columns=True, show_expanded=True)]
    ]

    btn_guardarusuario = sg.Button("Guardar usuario", key="btn_guardarusuario")
    btn_historial = sg.Button("Ver historial", key="btn_historial")
    btn_eliminarusuario = sg.Button("Eliminar usuario", key="btn_eliminarusuario")

    botones = []

    if TiposUsuarios.EsAdministrativo():
        if TiposUsuarios.EsDeContabilidad():
            botones = [btn_historial]
    elif TiposUsuarios.EsDirectivo():
        if TiposUsuarios.EsDeContabilidad():
            botones = [btn_guardarusuario, btn_historial, btn_eliminarusuario]
        else:
            botones = [btn_guardarusuario, btn_eliminarusuario]
    elif TiposUsuarios.EsSecretario():
        botones = [btn_guardarusuario, btn_historial, btn_eliminarusuario]

    layout_02 = [
        [sg.Text("MODIFICAR USUARIO")],
        [sg.Text("Nombres*:"), sg.Input(key="in_nombres")],
        [sg.Text("DNI*:"), sg.Input(key="in_dni")],
        [sg.Text("Contraseña*:"), sg.Input(key="in_pass")],
        [sg.Text("Legajo*:"), sg.Input(key="in_legajo")],
        [sg.Text("Área*:"), sg.Input(key="in_area")],
        [sg.Text("Rol*:"), sg.Input(key="in_rol")],
        botones
    ]
    
    layout = [
        [sg.Menu(D.GetUserMenuBar())],
        [sg.T("Nuevo Pedido"), sg.Button("Nuevo usuario", k="btn_nuevousuario", visible=(not TiposUsuarios.EsAdministrativo()))],
        [sg.Column(layout_01, p=0, vertical_alignment="top"), sg.VerticalSeparator(), sg.Column(layout_02, p=0, vertical_alignment="top")]
    ]

    window = sg.Window("Ventana principal", layout=layout)

    new_window = ""

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Salir':
            break

        if event == "btn_nuevousuario":
            NuevoUsuario()

        if event in ["Menu Principal"]:
            new_window = "vp"
            break

    window.close()

    GoToWindow(new_window)

def NuevoUsuario():
    new_dni = sg.popup_get_text('Ingrese el DNI a buscar')
    print(new_dni)