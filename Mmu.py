import DescritorPagina as dp
import Memoria

class Mmu():
    tabela = []
    fila = []
    def __init__(self, memoria):
        self.memoria = memoria
        self.tamanhoPagina = memoria.getTamanhoQuadro()

    def setTabela(self, tabela):
        self.tabela = tabela
    
    def traduzEndereco(self, enderecoLogico):
        posicao = enderecoLogico[1]
        tamanho = self.tamanhoPagina
        pagina = self.getTabela()[0]
        cont = 1
        while posicao >= tamanho:
            try:
                pagina = self.getTabela()[cont]
            except:
                print("Erro de pagina")
                exit(-1)
            cont+=1
            posicao -= tamanho
        return (pagina.getQuadro()-1) * self.tamanhoPagina + posicao
    
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
        enderecoFisico = self.traduzEndereco(enderecoLogico)
        pagina = self.getPaginaPosicao(enderecoLogico[0], enderecoLogico[1])
        pagina.setPaginaValida(False)
        self.memoria.setNumeroMemoriaDeDados(enderecoFisico, valor)
        pagina.setPaginaValida(True)
        self.alteraPagina(enderecoLogico[0], enderecoLogico[1])
        numeroPagina = pagina.getQuadro()
        if numeroPagina not in self.fila: 
            self.fila.append(numeroPagina)
        print(f"Fila {self.fila}")

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
        tamanho = self.memoria.getTamanhoQuadro()
        cont = 0
        if posicao < tamanho:
            pagina = paginas[0]
        else:
            while(posicao > tamanho):
                cont += 1
                pagina = pagina[cont]
                tamanho += 4
        return pagina

    def getFila(self):
        return self.fila
 



