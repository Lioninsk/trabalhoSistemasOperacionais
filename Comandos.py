def retornaComandoId(comando):
    try:
        comandoId = {
                "CARGI" : 1,
                "CARGM" : 2,
                "CARGX" : 3,
                "ARMM"  : 4,
                "ARMX"  : 5,
                "SOMA"  : 6,
                "DESVZ" : 7,
                "NEG"   : 8
            }[comando]
    except:
        comandoId = -1
    return comandoId


def executaComando(cpu, id, instrucao):
    try:
        argumento = int(instrucao[1])
    except:
        pass
    if (id == 1):
        cargi(cpu, argumento)
    elif(id == 2):
        cargm(cpu, argumento)
    elif(id == 3):
        cargx(cpu, argumento)
    elif(id == 4):
        armm(cpu, argumento)
    elif(id == 5):
        armx(cpu, argumento)
    elif(id == 6):
        soma(cpu, argumento)
    elif(id == 7):
        desvz(cpu, argumento)
    else:
        neg(cpu)



def cargi(cpu, n):
    cpu.setAcumulador(n)

def cargm(cpu, n):
    cpu.setAcumulador(cpu.getValorMemoriaDeDados(n))

def cargx(cpu, n):
    cpu.setAcumulador(cpu.getValorMemoriaDeDados(cpu.getValorMemoriaDeDados(n)))

def armm(cpu, n):
    cpu.setNumeroMemoriaDeDados(n, cpu.getAcumulador())

def armx(cpu, n):
    cpu.setNumeroMemoriaDeDados(cpu.getValorMemoriaDeDados(n), cpu.getAcumulador())

def soma(cpu, n):
    cpu.setAcumulador(cpu.getAcumulador() + cpu.getValorMemoriaDeDados(n))

def neg(cpu):
    cpu.setAcumulador(cpu.getAcumulador() * -1)

def desvz(cpu, n):
    if(cpu.getAcumulador() == 0):
        cpu.setPc(n)
    


    



 
    
