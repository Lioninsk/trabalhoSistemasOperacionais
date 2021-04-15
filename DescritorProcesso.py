import Interface as it
class DescritorProcesso:

    def __init__(self, job, memoriaDados, memoriaPrograma, cpuBack, cpuEstBack, tabelaPaginas):
        self.job = job
        self.memoriaDados = memoriaDados
        self.memoriaPrograma = memoriaPrograma
        self.cpuBack = cpuBack
        self.cpuEstBack = cpuEstBack
        self.estadoProcesso = "iniciado"
        self.tabelaPaginas = tabelaPaginas
    
    def __str__(self):
        return f"processo do programa:{self.job.getPrograma()}"

    def getJob(self):
        return self.job 
    def getMemoriaDados(self):
        return self.memoriaDados 
    def getMemoriaPrograma(self):
        return self.memoriaPrograma 
    def getCpu(self):
        return self.cpuBack 
    def getCpuEst(self):
        return self.cpuEstBack 
    def getEstadoProcesso(self):
        return self.estadoProcesso
    def getQuantum(self):
        return self.quantum
    def getTabela(self):
        return self.tabelaPaginas
    def getValorMemoriaDados(self,index):
        return self.memoriaDados[index]
    
    def setMemoriaDados(self, dado, quadro):
        self.memoriaDados[quadro] = dado 

    def setmemoriaPrograma(self, memoriaPrograma):
        self.memoriaPrograma = memoriaPrograma
    def setCpu(self, cpuInfo):
        self.cpuBack = cpuInfo 
    def setCpuEst(self, cpuEstInfo):
        self.cpuEstBack = cpuEstInfo 
    def setEstadoProcesso(self, estado):
        self.estadoProcesso = estado
    def setQuantum(self, quantum):
        self.quantum = quantum
    def setTabelaPaginas(self, tabela):
        self.tabelaPaginas = tabela
    
    def getPaginaInvalida(self, memoria):
        print(f"Tabela:{self.tabelaPaginas}")
        print("===================Descritor Processo=========================\n")
        instrucao = it.cpu_instrucao(self.cpuBack).split()
        if instrucao[0] != "ARMX":
            numeroQuadro = int(instrucao[1]) + 1
        else:
            print("ENTROUUUUU")
            numeroQuadro = memoria.getValorMemoriaDeDados(int(instrucao[1])) + 1
        print(f"+_+_+_+_+_+_+ INSTRUÇÃO:{it.cpu_instrucao(self.cpuBack)}")
        print(f"Quadro:{numeroQuadro} ")
        for pagina in self.tabelaPaginas:
            print(f"\nPagina:{pagina}, Quadro:{pagina.getQuadro()} numQuadro:{numeroQuadro}")
            if pagina.getQuadro() == numeroQuadro:
                pagina.setPaginaValida(True)
                print("============================================\n")
                return pagina
        print("Pagina não encontrada! descritor processo")
        exit(-2) 
    



    
    

