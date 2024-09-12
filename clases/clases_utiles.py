class TiposUsuarios:
    @staticmethod
    def EsSecretario():
        from globales import g_UsuarioActual
        return g_UsuarioActual.Rol == 2
    
    @staticmethod
    def EsDirectivo():
        from globales import g_UsuarioActual
        return g_UsuarioActual.Rol == 1
    
    @staticmethod
    def EsAdministrativo():
        from globales import g_UsuarioActual
        return g_UsuarioActual.Rol == 0
    
    @staticmethod
    def EsDeContabilidad():
        from globales import g_UsuarioActual
        return g_UsuarioActual.Area == 0

    @staticmethod    
    def EsDeCompras():
        from globales import g_UsuarioActual
        return g_UsuarioActual.Area == 1