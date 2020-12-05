class DescritorJobs:
    
    def  __init__(self, programa, qtdMemoria, dispEntrada, tempoEntrada, arqSaida, tempoSaida):
        self.programa = programa
        self.qtdMemoria = qtdMemoria
        self.dispEntrada = dispEntrada
        self.arqSaida = arqSaida
        self.tempoLeitura = tempoEntrada
        self.tempoEscrita = tempoSaida


    def getPrograma(self):
        return self.programa
    def getQtdMemoria(self):
        return self.qtdMemoria
    def getDispEntrada(self):
        return self.dispEntrada
    def getArqSaida(self):
        return self.arqSaida
    def getTempoLeitura(self):
        return self.tempoLeitura
    def getTempoEscrita(self):
        return self.tempoEscrita







