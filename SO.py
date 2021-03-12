import Cpu, CpuEstado, Memoria, Interface, Controlador, glob, Mmu
import Descritor, os, Timer, DescritorProcesso, Escalonador, DescritorPagina
import pandas as pd


class SistemaOperacional:

    def __init__(self):
        self.memoria = Memoria.Memoria()
        self.mmu = Mmu.Mmu(self.memoria)
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.timer = Timer.Timer()
        self.contadorExecucao = 0
        self.contadorLeitura = 0
        self.contadorEscrita = 0
        self.contadorPara = 0
        self.contadorFalhasPagina = 0
        self.contadorTrocaProcessos = 0
        
    
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

    def para(self):
        print(f"CpuEstado acumulador: {Interface.retorna_cpuEstado_acumulador(self.cpuEstado)}")
        print(f"programa {self.jobAtual.getPrograma()} parou!")

    def le(self, dispositivo):
        self.contadorLeitura += 1
        with open(f"{self.dir + self.jobAtual.getDispEntrada() + dispositivo}.txt", "r") as file:
            try:                
                valor = int(file.readlines()[-1])
            except:
                print("Error in E/S LE")
                exit(-1)
        Interface.cpu_estado_altera_acumulador(self.cpuEstado, valor)
        
        

    def grava(self, dispositivo):
        self.contadorEscrita += 1
        numero = str(Interface.retorna_cpuEstado_acumulador(self.cpuEstado))
        
        try:
            path = f"{self.dir + self.jobAtual.getArqSaida() + dispositivo}.txt"
            mode = 'a' if os.path.exists(path) else 'w'
            with open(path, mode) as file:
                file.write(numero+"\n")
        except:
            print("Error in E/S GRAVA")
            exit(-1)
    
    def executa(self, idInstrucao, instrucao):
        self.contadorExecucao += 1
        if idInstrucao == 1:
            self.para()
            self.contadorPara += 1
            return True
        else:
            argumento = instrucao[1]
            if(idInstrucao == 2):
                tempoLeitura = self.timer.timerAgora() + self.jobAtual.getTempoLeitura()
                self.timer.setInterrupcao(tempoLeitura, "leitura", self.jobAtual.getData())
                self.le(argumento)
            else:
                tempoEscrita = self.timer.timerAgora() + self.jobAtual.getTempoEscrita()
                self.timer.setInterrupcao(tempoEscrita, "escrita", self.jobAtual.getData())
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
        self.escalonador = Escalonador.Escalonador()
        contadorPaginas = 0
        tabelaPaginas = [None]
        for job in filaJobs:
            contadorPaginas ,tabelaPaginas = self.criaPaginas(contadorPaginas, job.getQtdMemoria())
            instrucoes = Interface.leituraArquivo(job.getPrograma()) 
            vet = [None]*job.getQtdMemoria()#inicializa vetor com a memoria do job
            self.escalonador.setProcesso(DescritorProcesso.DescritorProcesso(job, vet, instrucoes, [], [], tabelaPaginas))
        self.execucaoProcessos(controlador)

    def criaPaginas(self, contadorPaginas, tamanhoMemoriaDados):
        paginas = []
        if tamanhoMemoriaDados == 0:
            return contadorPaginas, paginas
        tamanhoPagina = self.memoria.getTamanhoQuadro()
        if tamanhoMemoriaDados <= tamanhoPagina:
            contadorPaginas+=1
            paginas.append(DescritorPagina.DescritorPagina(contadorPaginas))
        else:
            while tamanhoMemoriaDados > 0:
                contadorPaginas+=1
                paginas.append(DescritorPagina.DescritorPagina(contadorPaginas))
                tamanhoMemoriaDados -= tamanhoPagina
        return contadorPaginas, paginas

    def execucaoProcessos(self, controlador):
        self.timer.numeroDeProcessos(self.escalonador.getNumeroProcessos())#prepara o timer para suportar informações com base no numero de processos
        while True:
            processoAtual = self.proximoProcesso()
            self.mmu.setTabela(processoAtual.getTabela())
            self.timer.aumentaNumeroEscalonamentos(processoAtual.getJob().getData())
            processoAtual.setQuantum(self.escalonador.getQuantum() + self.timer.timerAgora()) 
            self.quantumProcesso = processoAtual.getQuantum()
            status = processoAtual.getEstadoProcesso()
            if(status == "iniciado"):
                self.iniciaProcesso(processoAtual)
            elif status in ["continuo", "bloqueado"]:
                self.carregaProcesso(processoAtual)
            retorno = controlador.mainLoop(self.timer, processoAtual)

            if retorno == "pagina indisponivel":
                self.alocaPagina(processoAtual)
            if retorno == "para":
                self.timer.setTempoInicioFim(self.timer.timerAgora(), "fim", processoAtual.getJob().getData())
                processoAtual.setEstadoProcesso("finalizado")
            else:
                if(retorno != "quantum"):
                    self.timer.aumentaBloqueiosProcesso(processoAtual.getJob().getData())
                    processoAtual.setEstadoProcesso("bloqueado")
                else:
                    processoAtual.setEstadoProcesso("continuo")
                if(self.timer.interrupcoes == []):
                    self.checaDormindo()
            self.escalonador.ajustaPrioridade(processoAtual, self.timer.timerAgora())
    

    def iniciaProcesso(self, processo):
        self.timer.setTempoInicioFim(self.timer.timerAgora(), "inicio", processo.getJob().getData())
        processo.setCpu(Cpu.Cpu(self.mmu))
        processo.setCpuEst(CpuEstado.CpuEstadoT())
        self.cpu = processo.getCpu()
        self.cpuEstado = processo.getCpuEst()
        self.jobAtual = processo.getJob()
        Interface.cpu_estado_inicializa(self.cpuEstado)#definição das variaveis iniciais cpuEstado
        Interface.cpu_altera_estado(self.cpu, self.cpuEstado)#definição das variaveis iniciais da cpu
        Interface.cpu_altera_programa(self.memoria, processo.getMemoriaPrograma())#passagem das instrucoes para memoria de programa
        
    def carregaProcesso(self, processo):
        self.checaInterrompido(processo)
        self.jobAtual = processo.getJob()
        self.cpu = processo.getCpu()
        self.cpuEstado = processo.getCpuEst()
        Interface.cpu_altera_programa(self.memoria, processo.getMemoriaPrograma())


    
    def checaInterrompido(self, processo):
        cpuProcesso = processo.getCpu()
        if(cpuProcesso.getEstado() == "Interrompido"):
            cpuProcesso.setEstado("normal")
        
    
    def proximoProcesso(self):
        self.contadorTrocaProcessos += 1
        statusProximoProcesso = self.escalonador.processosDisponiveis() 
        if(statusProximoProcesso == "next"):
            return self.escalonador.getProcesso(self.escalonador.maiorPrioridade())
        elif(statusProximoProcesso == "bloqueado"):
            processoBloqueado = self.escalonador.getProcessoBloqueado()
            cpuEst = processoBloqueado.getCpuEst()
            cpu = processoBloqueado.getCpu()
            Interface.cpu_salva_estado(cpu, cpuEst)
            cpu.dorme()
            return processoBloqueado
        else:
            self.printaTabelaProcessos()
            self.printaTabelaTotais()
            exit(0)
    
    def checaDormindo(self):
        if Interface.cpu_interrupcao(self.cpu) == "dorme":
            Interface.cpu_altera_estado(self.cpu, self.cpuEstado)

    
    def desbloqueiaProcesso(self, idProcesso, interrupcao):
        processoBloqueado = self.escalonador.getProcessoId(idProcesso)
        print(f"Processo:{idProcesso}/{self.escalonador.getProcessoId(idProcesso).getJob().getPrograma()} desbloqueado da {interrupcao} na marca dos {self.timer.timerAgora()} segundos")
        self.escalonador.desbloqueiaProcesso(idProcesso)
        cpu = processoBloqueado.getCpu()
        cpuEst = processoBloqueado.getCpuEst()
        cpuEst.setEstado("normal")
        if not self.timer.isInterrupcaoProcesso(idProcesso):
            Interface.cpu_altera_estado(cpu, cpuEst)
            

    def checaInterrupcao(self):
        processo, interrupcao = self.timer.getInterrupcao()
        if(interrupcao != "nenhum"):
            self.desbloqueiaProcesso(processo, interrupcao)

        
    

    def checaQuantum(self, tempoAtual):
        return tempoAtual >= self.quantumProcesso

    def printaTabelaProcessos(self):
        self.timer.setRetorno()
        self.timer.setPercentualCpu()
        n = self.escalonador.getNumeroProcessos()
        print("-"*(17 * n))
        coluna = []
        linha = "Tempo Cpu:Tempo Inicial:Tempo Final:Tempo Retorno:Percentual Cpu:Tempo Bloqueado:Bloqueios:Escalonamentos:Preempcoes:Falhas de pagina".split(":")
        dados = []
        for i in range(n):
            coluna.append(f"Processo {i+1}")
        dados.append(self.timer.getTempoCpuProcesso())
        dados.append(self.timer.getTempoInicio())
        dados.append(self.timer.getTempoFim())
        dados.append(self.timer.getTempoRetorno())
        dados.append(self.timer.getPercentual())
        dados.append(self.timer.getTempoBloqueado())
        dados.append(self.timer.getNumeroBloqueios())
        dados.append(self.timer.getNumeroEscalonamentos())
        dados.append(self.timer.getNumeroPreempcao())
        dados.append(self.timer.getTempoFaltaPagina())
        tabela = pd.DataFrame(data=dados, index=linha, columns=coluna)
        print(tabela)        
        print("-"*(17 * n))
    
    def printaTabelaTotais(self):
        dados = []
        coluna = ["Tempos Totais"]
        linha = "Tempo Ativo:Tempo Ocioso:Execucoes do SO:Leituras:Escritas:Paradas:Trocas de processos:Preempcoes:Falhas de pagina".split(":")
        dados.append(self.timer.timerAgora())
        dados.append(self.timer.getCountOcioso())
        dados.append(self.contadorExecucao)
        dados.append(self.contadorLeitura)
        dados.append(self.contadorEscrita)
        dados.append(self.contadorPara)
        dados.append(self.contadorTrocaProcessos)
        dados.append(self.timer.getPreemcoesTotais())
        dados.append(self.timer.getFalhas())
        tabela = pd.DataFrame(data = dados, index=linha, columns=coluna)
        print(tabela)
    
    def alocaPagina(self, processoAtual):
        fila = self.mmu.getFila()
        primeiraPagina = self.checkPaginas()
        if not primeiraPagina:
            return
        paginaFaltante = processoAtual.getPaginaInvalida()
        numeroPaginaFaltante = paginaFaltante.getNumeroPagina()
        print(f"PRIMEIRA:{primeiraPagina} FALTANTE{paginaFaltante}")
        self.desaloca(primeiraPagina, processoAtual)
        fila.remove(primeiraPagina.getNumeroPagina())
        fila.append(primeiraPagina.getNumeroPagina())
        fila.insert(0, numeroPaginaFaltante)
        print(f"FILA:{fila}")
        primeiraPaginaQuadro = primeiraPagina.getQuadro()
        paginaFaltante.setQuadro(primeiraPaginaQuadro)
        primeiraPagina.setQuadro(numeroPaginaFaltante)
        self.aloca(paginaFaltante)

    def desaloca(self, paginaAlocada, processoAtual):
        inicio, fim = self.inicioFimPagina(paginaAlocada)
        valores = self.memoria.getQuadro(inicio, fim)
        processo = self.escalonador.getProcessoPagina(paginaAlocada)
        processo.setMemoriaDados(valores)
        paginaAlocada.setPaginaValida(False)
        paginaAlocada.setPaginaAcessada(False)
        paginaAlocada.setPaginaAlterada(False)
        self.memoria.setQuadro(inicio, fim, [None] * self.memoria.getTamanhoQuadro())
        tempoLeitura = processo.getJob().getTempoLeitura() + self.timer.timerAgora()
        self.timer.setInterrupcao(tempoLeitura, "leitura de pagina", processoAtual.getJob().getData())

    def aloca(self, pagina):
        inicio, fim = self.inicioFimPagina(pagina)
        processo = self.escalonador.getProcessoPagina(pagina)
        self.timer.aumentaFalhaPagina(processo.getJob().getData())
        self.timer.aumentaTempoFaltaPagina(processo.getJob().getData())
        valores = processo.getMemoriaDados()
        self.memoria.setQuadro(inicio, fim, valores)
        tempoEscrita = processo.getJob().getTempoEscrita() + processo.getJob().getTempoLeitura() + self.timer.timerAgora()
        self.timer.setInterrupcao(tempoEscrita, "escrita de pagina", processo.getJob().getData())
        pagina.setPaginaAlterada(False)
        pagina.setPaginaAcessada(False)
        pagina.setPaginaValida(True)
    
    def inicioFimPagina(self, pagina):
        tamPagina = self.memoria.getTamanhoQuadro()
        inicio = (pagina.getQuadro() - 1) * tamPagina
        fim = inicio + (tamPagina - 1)
        return inicio, fim
    
    def checkPaginas(self):
        fila = self.mmu.getFila()
        for numeroPagina in fila:
            pagina = self.escalonador.getPaginaComNumero(numeroPagina)
            print(f"pagina:{pagina} alterada:{pagina.getPaginaAlterada()}")
            if pagina.getPaginaAlterada():
                self.contadorFalhasPagina += 1
                print(f"RETORNANDO PAGINA ALTERADA")
                return pagina
        print("RETURN")
        return False