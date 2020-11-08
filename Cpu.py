


class Cpu:
    pc = 0
    acumulador = 0
    estado = "normal"
    
    def __init__(self, acessoMemoria):
        self.acessoMemoria = acessoMemoria

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

    def getPc(self):
        return self.pc

    def getAcumulador(self):
        return self.acumulador

    def getEstado(self):
        return self.estado
    
    def setMemoriaPrograma(self, instrucoes):
        self.acessoMemoria.setMemoriaPrograma(instrucoes)
    
    def setMemoriaDados(self, vet):
        self.acessoMemoria.setMemoriaDados(vet)
    
    def getInstrucao(self):
        return self.acessoMemoria.getInstrucao(self.pc)
    
    def getValorMemoriaDeDados(self, i):
        return self.acessoMemoria.getValorMemoriaDeDados(i)
    
    def setNumeroMemoriaDeDados(self, i, numero):
        self.acessoMemoria.setNumeroMemoriaDeDados(i, numero)


    












    