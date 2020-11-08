#Nome do aluno: Pedro Leonel
#Disciplina: Sistemas Operacionais


import Cpu, CpuEstado, Memoria, Interface

memoria = Memoria.Memoria()
cpu = Cpu.Cpu(memoria)
vet = [None]*4
cpuEstado = CpuEstado.CpuEstadoT()
instrucoes = Interface.leituraDoArquivo()

Interface.cpu_estado_inicializa(cpuEstado)
Interface.cpu_altera_estado(cpu, cpuEstado)
Interface.cpu_altera_programa(cpu, instrucoes)
Interface.cpu_altera_dados(cpu, vet)

while(Interface.cpu_interrupcao(cpu) == "normal"):
    Interface.executa(cpu)

print(f"Cpu parou na instrucao {Interface.cpu_instrucao(cpu)}.")
print(f"O valor de m[0] eh {cpu.getValorMemoriaDeDados(0)}")