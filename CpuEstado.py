class CpuEstadoT:
    pc = 0
    acumulador = 0
    estado = ""


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