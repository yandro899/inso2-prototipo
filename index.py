def GoToWindow(new_window: str):
    from pedidos import VerPedidos, CrearPedido
    from ventana_principal import VentanaPrincipal
    from usuarios import VerUsuarios

    if new_window == "np":
        CrearPedido()
    elif new_window == "rp":
        VerPedidos()
    elif new_window == "vp":
        VentanaPrincipal()
    # elif new_window == "vprod":
    #     C.VerProductos()
    # elif new_window == "dprod":
    #     C.DevolverProductos()
    elif new_window == "u":
        VerUsuarios()