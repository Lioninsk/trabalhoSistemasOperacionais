import DescritorPagina as dp
import Memoria

class Mmu():
    fila = []
    def __init__(self, memoria, escalonador, mapaMemoria):
        self.memoria = memoria
        self.escalonador = escalonador
        self.tamanhoPagina = memoria.getTamanhoQuadro()
        self.mapaMemoria = mapaMemoria


    def setTabela(self, tabela):
        self.tabela = tabela
    
    def traduzEndereco(self, enderecoLogico):
        print(f"==========TRADUZ==============")
        posicao = enderecoLogico[1]
        pagina = enderecoLogico[0][0]
        numero =  self.escalonador.getProcessoPagina(pagina).getJob().getData()
        print(f"Processo:{numero} posicao:{posicao}")
        for pos in self.mapaMemoria:
            if (pos[0] == None) or (pos[0] == numero and pos[1] == posicao):
                print(f"RETORNANDO POSICAO {posicao}")
                return pos[2]
        for pos in self.mapaMemoria:
            if(pos[0] == numero and pos[1] == None):
                return pos[2]
        print(f"==========DEU RUIMMMMMM==============")
        return None
                    

    
    def isPaginaDisponivel(self, numero):
        for pos in self.mapaMemoria:
            if pos[0] == None or (pos[0] == numero and pos[1] == None):
                return True
        return False
            
    
    def getNumeroMemoria(self, enderecoLogico):
        enderecoFisico = self.traduzEndereco(enderecoLogico)
        self.acessaPagina(enderecoLogico[0], enderecoLogico[1])
        retorno = self.memoria.getValorMemoriaDeDados(enderecoFisico)
        if retorno == None:
            retorno = self.getValorMemoriaVirtual(enderecoLogico[1])
        return retorno
    
    def setNumeroMemoria(self, enderecoLogico, valor):
        print(f"=========AQUI O VALOR:{valor}")
        self.setPaginaMapa(enderecoLogico[1])
        enderecoFisico = self.traduzEndereco(enderecoLogico)
        self.memoria.setNumeroMemoriaDeDados(enderecoFisico, valor)
        self.alteraPagina(enderecoLogico[0], enderecoLogico[1])


    def getInstrucao(self,pc):
        return self.memoria.getInstrucao(pc)
    
    def getTabela(self):
        return self.tabela
    
    def acessaPagina(self,paginas, posicao):
        for pagina in paginas:
            print(f"{pagina} Quadro:{pagina.getQuadro()}")
        pagina = self.getPaginaPosicao(paginas, posicao)
        pagina.setPaginaAcessada(True)
        
    def alteraPagina(self,paginas, posicao):
        pagina = self.getPaginaPosicao(paginas, posicao)
        pagina.setPaginaAlterada(True)
    


    def getFila(self):
        return self.fila
    
    def invalidaPagina(self, enderecoLogico):
        print(f"logico:{enderecoLogico[0]}")
        pagina = self.getPaginaPosicao(enderecoLogico[0], enderecoLogico[1])
        pagina.setPaginaValida(False)
    
    
    def getValorMemoriaVirtual(self, valor):
        pag = self.tabela[0]
        processo = self.escalonador.getProcessoPagina(pag)
        memoriaVirtual = processo.getMemoriaDados()
        print("GET THIS FAR")
        return memoriaVirtual[valor]

    def autentificaPagina(self, posicao):
        for pagina in self.tabela:
            if not pagina.getPaginaValida() or pagina.getQuadro() == posicao:
                pagina.setQuadro(posicao)
                pagina.setPaginaValida(True)
                return pagina

    def getPaginaPosicao(self, paginas, posicao):
        for pagina in paginas:
            if pagina.getQuadro() == posicao:
                return pagina

    def setPaginaMapa(self, posicao):
        pagina = self.tabela[0]
        programa = self.escalonador.getProcessoPagina(pagina)
        if self.isPaginaDisponivel(programa.getJob().getData()):
            for posMemoria in self.mapaMemoria:
                if (posMemoria[0] == None or posMemoria[1] == None) and not self.isPositionConfirmed(posicao, programa.getJob().getData()):
                    pagina = self.autentificaPagina(posicao)
                    posMemoria[0] = programa.getJob().getData()
                    posMemoria[1] =  posicao
                    if posMemoria[2] not in self.fila:
                        self.fila.append(posMemoria[2])
                    print(f"Posicao:{posicao} marcada no mapa com o processo:{programa.getJob().getData()}")
                    print(self.mapaMemoria)
                    return

    def isPositionConfirmed(self, posicao, numero):
        for pos in self.mapaMemoria:
            if pos[0] == numero and pos[1] == posicao:
                print("\nYES YES YESSSSSSSSSSSSSSSSSSSSSSSSSSS\n")
                return True
        print("\nNO NO NOOOOOOOOOOOOOOOOOOOOOOOOO\n")
        return False


