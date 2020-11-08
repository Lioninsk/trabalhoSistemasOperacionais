class Memoria:
    memoriaDePrograma = []
    memoriaDeDados = []

    def getLinhaMemoriaPrograma(self, i):
        return self.memoriaDePrograma[i]

    def setMemoriaPrograma(self, memoriaPrograma):
        for linha in memoriaPrograma:
            self.memoriaDePrograma.append(linha)
    
    def setMemoriaDados(self, memoriaDeDados):
        for item in memoriaDeDados:
            self.memoriaDeDados.append(item)
    
    def setNumeroMemoriaDeDados(self, i, numero):
        self.memoriaDeDados[i] = numero
    
    def getInstrucao(self, pc):
        return self.memoriaDePrograma[pc]
    
    def getValorMemoriaDeDados(self, i):
        return self.memoriaDeDados[i]
