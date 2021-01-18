class DescritorJobs:
    
    def  __init__(self, programa, qtdMemoria, dispEntrada, tempoEntrada, arqSaida, tempoSaida, data, prioridade):
        self.programa = programa
        self.qtdMemoria = qtdMemoria
        self.dispEntrada = dispEntrada
        self.arqSaida = arqSaida
        self.tempoLeitura = tempoEntrada
        self.tempoEscrita = tempoSaida
        self.data = data
        self.prioridade = prioridade


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
    def getData(self):
        return self.data
    def getPrioridade(self):
        return self.prioridade
    def setPrioridade(self, prioridade):
        self.prioridade = prioridade







