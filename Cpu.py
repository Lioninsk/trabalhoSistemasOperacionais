


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
    
    def memoryViolation(self):
        self.estado = "memory violation"

    def getPc(self):
        return self.pc

    def getAcumulador(self):
        return self.acumulador

    def getEstado(self):
        return self.estado
    
    def setMemoriaPrograma(self, instrucoes):
        try:
            self.acessoMemoria.setMemoriaPrograma(instrucoes)
        except:
            self.memoryViolation()
    
    def setMemoriaDados(self, vet):
        try:
            self.acessoMemoria.setMemoriaDados(vet)
        except:
            self.memoryViolation()
    
    def getInstrucao(self):
        return self.acessoMemoria.getInstrucao(self.pc)
    
    def getValorMemoriaDeDados(self, i):
        try:
            return self.acessoMemoria.getValorMemoriaDeDados(i)
        except:
            self.memoryViolation()
    
    def setNumeroMemoriaDeDados(self, i, numero):
        try:
            self.acessoMemoria.setNumeroMemoriaDeDados(i, numero)
        except:
            self.memoryViolation()


    












    