class Memoria:
    memoriaDePrograma = []
    # tamanho = 4
    # pagina = 1
    tamanho = 60
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
            print(f"Retornando o valor:{self.memoriaDeDados[i]}")
            return self.memoriaDeDados[i]
        except:
           return None


    def getTamanhoQuadro(self):
        return self.pagina
    def getTamanhoMemoria(self):
        return len(self.memoriaDeDados)
    def __str__(self):
        return f"{self.memoriaDeDados}"
    

        





