class Memoria:
    memoriaDePrograma = []
    # tamanho = 4
    # pagina = 1
    tamanho = 4
    pagina = 1
    memoriaDeDados = [None] * tamanho


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
        try:
            return self.memoriaDeDados[i]
        except:
           print("Error getting value!")
           exit(0)
    
    def getQuadro(self, inicio, fim):
        if inicio < 0 or fim >= len(self.memoriaDeDados):
            return None
        quadro = []
        for i in range(inicio, fim+1):
            quadro.append(self.memoriaDeDados[i])
        return quadro
    
    def setQuadro(self, inicio, fim, valores):
        indice = 0
        try:
            for i in range(inicio, fim+1):
                self.memoriaDeDados[i] = valores[indice]
                indice += 1
            print("Deu bom!")
            print(self.memoriaDeDados)
        except:
            print("Deu ruim!")
            print(f"Inicio:{inicio} Fim:{fim}")
            print(f"MemoriaDados:{self.memoriaDeDados} Valores:{valores}")
            exit(0)
    

    def getTamanhoQuadro(self):
        return self.pagina
    def getTamanhoMemoria(self):
        return len(self.memoriaDeDados)
    def __str__(self):
        return f"{self.memoriaDeDados}"
    

        





