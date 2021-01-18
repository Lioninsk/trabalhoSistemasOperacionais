class DescritorProcesso:

    def __init__(self, job, memoriaDados, memoriaPrograma, cpuBack, cpuEstBack):
        self.job = job
        self.memoriaDados = memoriaDados
        self.memoriaPrograma = memoriaPrograma
        self.cpuBack = cpuBack
        self.cpuEstBack = cpuEstBack
        self.estadoProcesso = "iniciado"

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
    
    def setMemoriaDados(self, memoriaDados):
        self.memoriaDados =  memoriaDados
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
    



    
    

