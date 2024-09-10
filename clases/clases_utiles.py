from globales import g_UsuarioActual

class TiposUsuarios:
    @staticmethod
    def EsSecretario():
        global g_UsuarioActual
        return g_UsuarioActual.Rol == 2
    
    @staticmethod
    def EsDirectivo():
        global g_UsuarioActual
        return g_UsuarioActual.Rol == 1
    
    @staticmethod
    def EsAdministrativo():
        global g_UsuarioActual
        return g_UsuarioActual.Rol == 0
    
    @staticmethod
    def EsDeContabilidad():
        global g_UsuarioActual
        return g_UsuarioActual.Area == 0

    @staticmethod    
    def EsDeCompras():
        global g_UsuarioActual
        return g_UsuarioActual.Area == 1