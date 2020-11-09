#Nome do aluno: Pedro Leonel
#Disciplina: Sistemas Operacionais


import Cpu, CpuEstado, Memoria, Interface

memoria = Memoria.Memoria()#inicializa memoria
cpu = Cpu.Cpu(memoria)#inicializa cpu passando acesso a memoria
vet = [None]*4#inicializa vetor com 4 posicoes nulas
cpuEstado = CpuEstado.CpuEstadoT()#inicializa cpu estado
instrucoes = Interface.leituraDoArquivo()#leitura do arquivo

Interface.cpu_estado_inicializa(cpuEstado)#definição das variaveis iniciais cpuEstado
Interface.cpu_altera_estado(cpu, cpuEstado)#definição das variaveis iniciais da cpu
Interface.cpu_altera_programa(cpu, instrucoes)#passagem das instrucoes para memoria de programa
Interface.cpu_altera_dados(cpu, vet)#passagem do vetor para memoria de dados

while(Interface.cpu_interrupcao(cpu) == "normal"):#enquanto não houver interrupção executa
    Interface.executa(cpu)

print(f"Cpu parou na instrucao {Interface.cpu_instrucao(cpu)}.")
print(f"O valor de m[0] eh {cpu.getValorMemoriaDeDados(0)}")

###fim parte 1