import Cpu, CpuEstado, Memoria, Interface, Controlador, glob



class SistemaOperacional:

    def __init__(self, cpuEstado):
        self.cpuEstado = cpuEstado

    def retornaId(self, comando):
        
        try:
            comandoId = {
                    "PARA"  : 1,
                    "LE"    : 2,
                    "GRAVA" : 3,
                }[comando]
        except:
            interrompe("instrucao ilegal")
        return comandoId

    def para(self, num):
        print(f"CpuEstado acumulador: {Interface.retorna_cpuEstado_acumulador(self.cpuEstado)}")
        print(f"exit code:{num}")
        exit(num)

    def le(self, dispositivo):
        with open(glob.glob(f'cpu/ES/{dispositivo}.txt')[0], "r") as file:
            try:                
                valor = int(file.readlines()[-1])
            except:
                print("Error in E/S")
                exit(-1)
        Interface.cpu_estado_altera_acumulador(self.cpuEstado ,valor)

    def grava(self, dispositivo):
        numero = str(Interface.retorna_cpuEstado_acumulador(self.cpuEstado))
        
        file = glob.glob(f'cpu/ES/{dispositivo}.txt')[0]
        with open(file, "a") as file:
            file.write(numero+"\n")


            

    def executa(self, idInstrucao, instrucao):
        argumento = int(instrucao[1])
        if idInstrucao == 1:
            self.para(argumento)
        elif idInstrucao == 2:
            self.le(argumento)
        else:
            self.grava(argumento)

    def interrompe(interrupcao):
        print(f"Sistema interrompido por {interrupcao}")
        if(interrupcao == "memory violation"):
            para(-1)
        else:
            para(-2)





            
    
    




cpuEstado = CpuEstado.CpuEstadoT()#inicializa cpu estado

so = SistemaOperacional(cpuEstado)
memoria = Memoria.Memoria()#inicializa memoria
cpu = Cpu.Cpu(memoria)#inicializa cpu passando acesso a memoria
vet = [None]*4#inicializa vetor com 4 posicoes nulas
instrucoes = Interface.leituraDoArquivo()#leitura do arquivo

Interface.cpu_estado_inicializa(cpuEstado)#definição das variaveis iniciais cpuEstado

Interface.cpu_altera_estado(cpu, cpuEstado)#definição das variaveis iniciais da cpu
Interface.cpu_altera_programa(cpu, instrucoes)#passagem das instrucoes para memoria de programa
Interface.cpu_altera_dados(cpu, vet)#passagem do vetor para memoria de dados

controlador = Controlador.Controlador(cpu = cpu, so = so)
controlador.mainLoop()






    

    






