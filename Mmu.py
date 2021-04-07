import DescritorPagina as dp
import Memoria

class Mmu():
    fila = []
    def __init__(self, memoria):
        self.memoria = memoria
        self.tamanhoPagina = memoria.getTamanhoQuadro()

    def setTabela(self, tabela):
        self.tabela = tabela
    
    def traduzEndereco(self, enderecoLogico):
        posicao = enderecoLogico[1]
        tamanho = self.tamanhoPagina
        # cont = 1
        for pag in self.tabela:
            if pag.getQuadro() - 1 == posicao:
                pagina = pag
        # print(f"posicao:{posicao} tamanho:{tamanho} cont:{cont} pagina:{pagina} quadro:{pagina.getQuadro()}")
        # while posicao + 1 != pagina.getQuadro():
        #     try:
        #         pagina = self.getTabela()[cont]
        #         print(f"posicao:{posicao} tamanho:{tamanho} cont:{cont} pagina:{pagina} quadro:{pagina.getQuadro()}")
        #     except:
        #         print(f"Erro de paginaaaa, cont:{cont}, pos:{posicao} tamanho:{tamanho}")
        #         exit(-1)
        #     cont+=1
        
        print(f"pos:{posicao} tam:{tamanho}")
        if not pagina.getPaginaValida():
            print("=================MMU - TRADUÇÃO===============")
            for pag in self.tabela:
                    print(f"\n{pag}, Valida:{pag.getPaginaValida()}")
            print(f"\nOh não, a {pagina} com quadro:{pagina.getQuadro()} não é valida!!!!\n")
            print("================================")
            return None
        print(f"==========Tradução=============")
        for pag in self.tabela:
            print(f"\n{pag}, Valida:{pag.getPaginaValida()}")
        resultado = (pagina.getQuadro()-1) * self.tamanhoPagina
        print(f"=-=-=- Colocando valor na posicao:{resultado}")
        return resultado
    
    def checkPosicao(self, posicao):
        return posicao < 0
    
    def getNumeroMemoria(self, enderecoLogico):
        if self.checkPosicao(enderecoLogico[1]):
            exit(-1)
        enderecoFisico = self.traduzEndereco(enderecoLogico)
        self.acessaPagina(enderecoLogico[0], enderecoLogico[1])
        return self.memoria.getValorMemoriaDeDados(enderecoFisico)
    
    def setNumeroMemoria(self, enderecoLogico, valor):
        if self.checkPosicao(enderecoLogico[1]):
            exit(-1)
        pagina = self.getPaginaPosicao(enderecoLogico[0], enderecoLogico[1])
 
        enderecoFisico = self.traduzEndereco(enderecoLogico)
        # pagina.setPaginaValida(False)
        self.memoria.setNumeroMemoriaDeDados(enderecoFisico, valor)
        pagina.setPaginaValida(True)
        self.alteraPagina(enderecoLogico[0], enderecoLogico[1])
        print(f"=-=-=- {pagina} com quadro:{pagina.getQuadro()} utilizada! ")

    def getInstrucao(self,pc):
        return self.memoria.getInstrucao(pc)
    
    def getTabela(self):
        return self.tabela
    
    def acessaPagina(self,paginas, posicao):
        pagina = self.getPaginaPosicao(paginas, posicao)
        pagina.setPaginaAcessada(True)
        
    def alteraPagina(self,paginas, posicao):
        pagina = self.getPaginaPosicao(paginas, posicao)
        pagina.setPaginaAlterada(True)
    
    def getPaginaPosicao(self, paginas, posicao):
        for pagina in paginas:
            if pagina.getQuadro()-1 == posicao: 
                break
        return pagina

    def getFila(self):
        return self.fila
    
    def invalidaPagina(self, enderecoLogico):
        
        pagina = self.getPaginaPosicao(enderecoLogico[0], enderecoLogico[1])
        print(f"\n@+@+@++@+@{pagina}, Valida:{pagina.getPaginaValida()} - APAGADAAAAAAAAAA")
        pagina.setPaginaValida(False)
 



