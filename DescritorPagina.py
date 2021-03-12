class DescritorPagina():
    def __init__(self, paginaNumero):
        self.valido = True
        self.paginaNumero = paginaNumero
        self.quadro = paginaNumero
        self.paginaAlteravel = True
        self.acessada = False
        self.alterada = False

    def __str__(self):
        return f"Pagina numero {self.paginaNumero}"
    
    def getNumeroPagina(self):
        return self.paginaNumero
    def getQuadro(self):
        return self.quadro
    def getPaginaValida(self):
        return self.valido
    def getPaginaAlterada(self):
        return self.alterada
    def getPaginaAcessada(self):
        return self.acessada

    def setPaginaAcessada(self, valor):
        self.acessada = valor
    def setPaginaAlterada(self, valor):
        self.alterada = valor
    def setPaginaValida(self, valor):
        self.valido = valor
    def setNumero(self, valor):
        self.paginaNumero = valor
    def setQuadro(self,valor):
        self.quadro = valor
