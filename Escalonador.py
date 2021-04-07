class Escalonador:
    quantum = 10
    listaProcessos = []
    
    def setProcesso(self, processo):
        self.listaProcessos.append(processo)
    
    def getProcesso(self, maior):
        
        for processo in self.listaProcessos:
            job = processo.getJob()
            prioridadeJob = job.getPrioridade()
            if(prioridadeJob == maior and processo.getEstadoProcesso() != "finalizado" and processo.getEstadoProcesso() != "bloqueado"):
                return processo
        return "fim"
    
    def maiorPrioridade(self):
        maior = 1
        for i in self.listaProcessos:
            job = i.getJob()
            prioridadeJob = job.getPrioridade()
            if(prioridadeJob < maior and i.getEstadoProcesso() != "bloqueado" and i.getEstadoProcesso() != "finalizado"):
                maior = prioridadeJob
        return maior

    def ajustaPrioridade(self, processo, tempoAtual):
        prioridade = processo.getJob().getPrioridade()
        tempoExecucao = self.quantum - (processo.getQuantum() - tempoAtual) 
        novaPrioridade = (prioridade + (tempoExecucao/self.quantum))/2
        processo.getJob().setPrioridade(novaPrioridade)
        
    
    def desbloqueiaProcesso(self, id):
        for processo in self.listaProcessos:
            if(processo.getJob().getData() == id and processo.getEstadoProcesso() == "bloqueado"):
                processo.setEstadoProcesso("continuo")  
    
    def processosDisponiveis(self):
        bloqueados = 0
        for processo in self.listaProcessos:
            status = processo.getEstadoProcesso() 
            if(status in ["continuo", "iniciado"]):
                return "next"
            elif status == "bloqueado":
                bloqueados += 1
        if(bloqueados > 0):
            return "bloqueado"
        return "fim"
    
    def processoJob(self, jobAtual):
        for processo in self.listaProcessos:
            if(processo.getJob() == jobAtual):
                return processo
    
    def getProcessoId(self, id):
        for processo in self.listaProcessos:
            if processo.getJob().getData() == id:
                return processo
        return None
    
    def getQuantum(self):
        return self.quantum

    def getNumeroProcessos(self):
        num = len(self.listaProcessos)
        return num

    def getProcessoBloqueado(self):
        for processo in self.listaProcessos:
            if processo.getEstadoProcesso()=="bloqueado":
                return processo

    def getPaginaComQuadro(self, quadro):
        for processo in self.listaProcessos:
            tabela = processo.getTabela()
            print("==========Escalonador===================")
            for pagina in tabela:
                print(f"=======================\nPagina:{pagina}\nValida:{pagina.getPaginaValida()}\nQuadro:{pagina.getQuadro()}\nQuadro atual:{quadro}")
                if pagina.getQuadro() == quadro and pagina.getPaginaValida(): 
                    return pagina
        return None
            
    def getProcessoPagina(self, pagina):
        for processo in self.listaProcessos:
            for pag in processo.getTabela():
                if pag == pagina:
                    return processo 
    
    def paginasOcupadas(self):
        cont = 0
        for processo in self.listaProcessos:
            for pagina in processo.getTabela():
                if pagina.getPaginaValida() == True:
                    cont+=1
        return cont
    
    def getListaProcessos(self):
        return self.listaProcessos

    def organizaPaginas(self):
        for processo in self.listaProcessos:
            for pagina in processo.getTabela():
                for pag in processo.getTabela():
                    if pagina != pag and pagina.getQuadro() == pag.getQuadro() and pagina.getPaginaValida() == pag.getPaginaValida() and pagina.getPaginaValida():
                        pagina.setPaginaValida(False)
    
