import Mmu


class Cpu:
    pc = 0
    acumulador = 0
    estado = "normal"
    
    def __init__(self, mmu):
        self.mmu = mmu

    def save(self, pc, acumulador, estado):
        self.pc = pc
        self.acumulador = acumulador
        self.estado = estado

    def setPc(self, pc):
        self.pc = pc

    def setAcumulador(self, acumulador):
        self.acumulador = acumulador

    def setEstado(self, estado):
        self.estado = estado

    def getInstrucao(self):
        return self.mmu.getInstrucao(self.pc)
    
    def memoryViolation(self):
        self.estado = "memory violationn"
        print(self.estado)
        exit(-1)

    def getPc(self):
        return self.pc

    def getAcumulador(self):
        return self.acumulador

    def getEstado(self):
        return self.estado
    
    def getValorMemoriaDeDados(self, posicao):
        enderecoLogico = [self.mmu.getTabela(), posicao]
        try:
            valor = self.mmu.getNumeroMemoria(enderecoLogico)
        except:
            self.mmu.invalidaPagina(enderecoLogico)
            self.estado = "pagina indisponivel"
            return 0
            
        if valor == None:
            # self.mmu.invalidaPagina(enderecoLogico)
            self.estado = "pagina indisponivel"
            return 0
        else:
            return valor
    
    def setNumeroMemoriaDeDados(self, posicao, numero):
        enderecoLogico = [self.mmu.getTabela(), posicao]
        try:
            self.mmu.setNumeroMemoria(enderecoLogico, numero)
        except Exception as error:
            print(f"Error:{error}")
            self.mmu.invalidaPagina(enderecoLogico)
            self.estado = "pagina indisponivel"
    
    def dorme(self):
        self.estado = "dorme"


    












    