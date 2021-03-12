class Memoria:
    memoriaDePrograma = []
    tamanho = 4
    memoriaDeDados = [None] * tamanho
    pagina = 4


    def getLinhaMemoriaPrograma(self, i):
        return self.memoriaDePrograma[i]

    def setMemoriaPrograma(self, memoriaPrograma):
        self.memoriaDePrograma.clear()
        for linha in memoriaPrograma:
            self.memoriaDePrograma.append(linha)

    def getInstrucao(self, pc):
        return self.memoriaDePrograma[pc]
    
    def setMemoriaDados(self, memoriaDeDados):
        self.memoriaDeDados = memoriaDeDados
    
    def setNumeroMemoriaDeDados(self, i, numero):
        self.memoriaDeDados[i] = numero
    
    def getValorMemoriaDeDados(self, i):
        return self.memoriaDeDados[i]
    
    def getQuadro(self, inicio, fim):
        if inicio < 0 or fim >= len(self.memoriaDeDados):
            return None
        quadro = []
        for i in range(inicio, fim+1):
            quadro.append(self.memoriaDeDados[i])
        return quadro
    
    def setQuadro(self, inicio, fim, valores):
        indice = 0
        for i in range(inicio, fim+1):
            self.memoriaDeDados[i] = valores[indice]
            indice += 1
    

    def getTamanhoQuadro(self):
        return self.pagina
    def getTamanhoMemoria(self):
        return len(self.memoriaDeDados)
    def __str__(self):
        return f"{self.memoriaDeDados}"
    

        





