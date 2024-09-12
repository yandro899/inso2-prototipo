import FreeSimpleGUI as sg

def RecuperarCuenta():
    """
        Ventana para recuperar la clave de usuario.
        Por ahora no va a funcionar. Se va a reservar para el otro
        cuatrimestre.

        Entrega: Nada
    """
    layout = [
        [sg.T("Recuperar cuenta")],
        [sg.Text("DNI: ") ,sg.Input(key="in_userdni_rec")],
        [sg.Text("", key="tx_send_mail", text_color="#000000")],
        [sg.Button("Enviar a correo", key="btn_sendmail"), sg.Button("Volver")]
    ]

    window = sg.Window("Recuperar cuenta", layout=layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Volver':
            break

        if event == "btn_sendmail":
            window["tx_send_mail"].update("¡Correo enviado!")

    window.close()

def VentanaInicioSesion() -> bool:
    """
        Ventana que inicia sesion de usuario. Por ahora va a funcionar por solicitudes POST
        usando archivos json.

        Entrega: Si inicia sesion, un diccionario con los valores necesarios del usuario,
        sino None si se cierra la ventana.
    """
    from globales import g_UsuarioActual, g_ListaUsuarios

    layout = [
        [sg.T("SI.GE.AD.")],
        [sg.Text("DNI: ") ,sg.Input(key="in_userdni")],
        [sg.Text("Contraseña: ") ,sg.Input(key="in_passw", password_char="*")],
        [sg.Text("", key="tx_incorrectinp", text_color="#ff0000")],
        [sg.Text("Recuperar cuenta", key="tx_recover_acc", text_color="#0000ff", enable_events=True)],
        [sg.Button("Iniciar sesión"), sg.Button("Cerrar")]
    ]

    window = sg.Window("SIGEAD", layout=layout)
    success = False

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cerrar':
            break

        if event == "tx_recover_acc":
            RecuperarCuenta()
            continue

        if event == "Iniciar sesión":
            dni = values["in_userdni"]
            passw = values["in_passw"]

            if not g_ListaUsuarios.AutenticarUsuario(dni, passw):
                print("El usuario o la contraseña son incorrectos.")
                continue

            success = True

            print("Hola {}. Tu DNI es {}.".format(g_UsuarioActual.Nombre, g_UsuarioActual.Dni))
            break

    window.close()
    return success