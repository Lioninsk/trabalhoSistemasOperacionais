import Cpu, CpuEstado, Memoria, Interface, Controlador, glob
import Descritor, os, Timer
import Descritor, os, Timer


class SistemaOperacional:

    def __init__(self):
        self.cpuEstado = CpuEstado.CpuEstadoT()
        self.memoria = Memoria.Memoria()
        self.cpu = Cpu.Cpu(self.memoria)
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.timer = Timer.Timer()
    

    def retornaId(self, comando):
        try:
            comandoId = {
                    "PARA"  : 1,
                    "LE"    : 2,
                    "GRAVA" : 3,
                }[comando]
        except:
            
            self.interrompe("instrucao ilegal")
        return comandoId

    def para(self, num):
        print(f"CpuEstado acumulador: {Interface.retorna_cpuEstado_acumulador(self.cpuEstado)}")
        print(f"programa {self.jobAtual.getPrograma()} parou code:{num}")

    def le(self, dispositivo):
        with open(f"{self.dir + self.jobAtual.getDispEntrada() + dispositivo}.txt", "r") as file:
            try:                
                valor = int(file.readlines()[-1])
                
            except:
                print("Error in E/S LE")
                exit(-1)
        Interface.cpu_estado_altera_acumulador(self.cpuEstado ,valor)
        

    def grava(self, dispositivo):
        numero = str(Interface.retorna_cpuEstado_acumulador(self.cpuEstado))
        
        try:
            file = f"{self.dir + self.jobAtual.getArqSaida() + dispositivo}.txt"
            with open(file, "a") as file:
                file.write(numero+"\n")
        except:
            print("Error in E/S GRAVA")
            exit(-1)
    

    def executa(self, idInstrucao, instrucao):
        if idInstrucao == 1:
            argumento = int(instrucao[1])
            self.para(argumento)
            return True
        else:
            
            argumento = instrucao[1]
            Interface.cpu_salva_estado(self.cpu, self.cpuEstado)
            self.cpu.dorme()
            
            if(idInstrucao == 2):
                self.timer.interrompe("Leitura", self.jobAtual.getTempoLeitura())
                self.le(argumento)
            else:
                self.timer.interrompe("Escrita", self.jobAtual.getTempoEscrita())
                self.grava(argumento)
           
            Interface.cpu_altera_estado(self.cpu, self.cpuEstado)
            return False


    def interrompe(self,interrupcao):
        print(f"Sistema interrompido por {interrupcao}")
        if(interrupcao == "memory violation"):
            exit(-1)
        else:
            exit(-2)
    
    
    def inicializa(self, filaJobs, controlador):
        for job in filaJobs:
            self.jobAtual = job
            instrucoes = Interface.leituraArquivo(job.getPrograma()) 
            vet = [None]*job.getQtdMemoria()#inicializa vetor com a memoria do job
            Interface.cpu_estado_inicializa(self.cpuEstado)#definição das variaveis iniciais cpuEstado
            Interface.cpu_altera_estado(self.cpu, self.cpuEstado)#definição das variaveis iniciais da cpu
            Interface.cpu_altera_programa(self.cpu, instrucoes)#passagem das instrucoes para memoria de programa
            Interface.cpu_altera_dados(self.cpu, vet)#passagem do vetor para memoria de dados
            controlador.mainLoop()


job1 = Descritor.DescritorJobs("instrucoes", qtdMemoria=4, dispEntrada=f"/ES/", arqSaida=f"/ES/", tempoEntrada=5, tempoSaida=5)
job2 = Descritor.DescritorJobs("instrucoes2", qtdMemoria=4, dispEntrada=f"/ES/", arqSaida=f"/ES/", tempoEntrada=3, tempoSaida=6)
filaJobs = []
filaJobs.append(job1)
filaJobs.append(job2)

so = SistemaOperacional()
controlador = Controlador.Controlador(so.cpu, so, so.cpuEstado)
so.inicializa(filaJobs, controlador)