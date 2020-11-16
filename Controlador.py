import Interface

class Controlador:
    def __init__(self, cpu, so):
        self.so = so
        self.cpu = cpu
        
    def mainLoop(self):
        while(True):
            Interface.executa(self.cpu)
            if(Interface.cpu_interrupcao(self.cpu) != "normal"):
                instrucao = Interface.cpu_instrucao(self.cpu)
                instrucao = instrucao.split()
                comandoInstrucao = instrucao[0]
                idInstrucao = self.so.retornaId(comandoInstrucao)
                self.so.executa(idInstrucao, instrucao)
                Interface.incrementaPc(self.cpu)
                
            


            