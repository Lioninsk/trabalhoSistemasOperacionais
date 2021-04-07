import Comandos
import glob
import os

def leituraArquivo(nomeArquivo):
    pasta = "/programas/"
    dir = os.path.dirname(os.path.realpath(__file__))
    file = f"{dir + pasta + nomeArquivo}.txt"
    print(file)
    try:
        with open(file, 'r') as fp:
            fileData = fp.readlines()
    except:
        print("Erro na leitura")
        exit(-1)
    if(fileData == []):
        print("Memoria de programa vazia!")
        exit(0)
    return fileData


def cpu_estado_inicializa(cpuEstado):
    cpuEstado.save(0,0,"normal")

def cpu_salva_estado(cpu, cpuEstado):
    
    cpuEstado.save(pc = cpu.getPc(), acumulador = cpu.getAcumulador(), estado = cpu.getEstado())

def cpu_altera_estado(cpu, cpuEstado):
    cpu.save(pc = cpuEstado.getPc(), acumulador = cpuEstado.getAcumulador(), estado = cpuEstado.getEstado())

def cpu_altera_programa(memoria, instrucoes):
    memoria.setMemoriaPrograma(instrucoes)

def cpu_altera_dados(memoria, vet):
    memoria.setMemoriaDados(vet)

def cpu_interrupcao(cpu):
    return cpu.getEstado()

def cpu_instrucao (cpu):
    return cpu.getInstrucao()

def cpu_estado_altera_acumulador(cpuEstado, novo_valor):
    cpuEstado.setAcumulador(novo_valor)

def retorna_cpuEstado_acumulador(cpuEstado):
    return cpuEstado.getAcumulador()

def incrementaPc(cpu):
    cpu.setPc(cpu.getPc() + 1)

def executa(cpu, cpuEstado):
    if(cpu_interrupcao(cpu) != "normal"):
        return
    pcAnterior = cpu.getPc()
    try:
        instrucao = cpu_instrucao(cpu)
        instrucao = instrucao.split()#intrucao = ["comando", "argumento"]
    except:
        return
    comando = instrucao[0]
    
    idInstrucao = Comandos.retornaComandoId(comando)

    if(idInstrucao != -1) :
        Comandos.executaComando(cpu, idInstrucao, instrucao)
        if cpu.getEstado() == "pagina indisponivel":
            return 
    else:
        if(cpu.getEstado() != "memory violation"):
            cpu_salva_estado(cpu, cpuEstado)
            cpu.setEstado("Interrompido")
        return
    if(cpu.getPc() == pcAnterior):#incrementa pc caso não haja interrupção ou desvio
        
        incrementaPc(cpu)



