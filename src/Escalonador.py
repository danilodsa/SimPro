#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

#------------------------------------------------------#
#         Graduação em Ciência da Computação           #
#                                                      #
#    Orientador: Diego Mello Silva                     # 
#    Aluno: Danilo da Silva Alves                      #
#    Matrícula: 0002749                                #
#                                                      #
#------------------------------------------------------#

from Fila import *

import numpy as np
import skfuzzy as fuzz
import time
from skfuzzy import control as ctrl

def defineEscalonador(arg):
    if arg == 'PRTY':
        escalonador = PRTY()
    elif arg == 'FCFS':
        escalonador = FCFS()
    elif arg == 'SJF':
        escalonador = SJF()
    elif arg == 'RR':
        escalonador = RR()
    elif arg == 'SRT':
        escalonador = SRT()
    elif arg == 'PFCS':
        escalonador = PFCS() #fuzzy
    elif arg == 'IFCS':
        escalonador = IFCS() #fuzzy
    elif arg == 'FPCS':
        escalonador = FPCS() #fuzzy
    else:
        print 'Método de escalonamento inválido.'
        quit()

    return escalonador



class Escalonador(object):

    def __init__(self):
        self.preemptivo = None
        self.quantum    = None
        self.nome       = None

    def selecionaProcesso(self):
        raise NotImplementedError("O escalonador deve ter um metodo para selecionar processos")
        #Abstrato

    def getPreemp(self):
        return self.preemptivo

    def getQuantum(self):
        return self.quantum

#Priority (Escalonamento por prioridades)
#-------------------------------------------------------------------------------------#
class PRTY(Escalonador):
    def __init__(self):
        self.preemptivo = False
        self.quantum = None
        self.nome = 'PRTY'

    def selecionaProcesso(self,filaDeProntos,tempo):
        #Ordena a fila de processos, tendo como critério a prioridade
        listaOrdenada = sorted(filaDeProntos.queue, key=lambda processo: (processo.getPrioridade(),processo.getChegada()), reverse = True)
        filaDeProntos.queue = listaOrdenada
        #filaDeProntos.remove(listaOrdenada[0].getProcessoId())

        return filaDeProntos.remove()

    def recalcula(self,filaDeProntos,colecao,tempoAtual):
        #obtem-se o mais prioritario da fila de prontos
        listaOrdenada = sorted(filaDeProntos.queue, key=lambda processo: (processo.getPrioridade(),processo.getChegada()), reverse = True)
        novoProcesso = listaOrdenada[0]
        #--#
        #Verificar qual e o menos prioritario em execucao
        cpuInterrompida = colecao.CPUs[0]
        processoInterrompido = colecao.buscaProcesso(cpuInterrompida.getProcessoAtual())
        menorPrd = processoInterrompido.getPrioridade()
        

        for cpu in colecao.CPUs:
            processo = colecao.buscaProcesso(cpu.getProcessoAtual())
            prd = processo.getPrioridade()

            if prd < menorPrd:
                cpuInterrompida = cpu
                menorPrd = prd
                processoInterrompido = processo
            elif prd == menorPrd: #Se a prioridade for a mesma, sera usado o tempo de chegada como criterio
                if processo.getChegada() > processoInterrompido.getChegada():
                    cpuInterrompida = cpu
                    menorPrd = prd
                    processoInterrompido = processo
        if novoProcesso.getPrioridade() > processoInterrompido.getPrioridade():
            filaDeProntos.remove(novoProcesso.getProcessoId())
            return novoProcesso,processoInterrompido,cpuInterrompida
        elif novoProcesso.getPrioridade() == processoInterrompido.getPrioridade():
            if novoProcesso.getChegada() < processoInterrompido.getChegada():
                filaDeProntos.remove(novoProcesso.getProcessoId())
                return novoProcesso,processoInterrompido,cpuInterrompida
        return None, None, None

    def desempate(self,processo,colecao):
        if colecao.buscaCpuLivre() == None:
            for cpu in colecao.CPUs:
                if not cpu.getDisponivel():
                    emExecucao = colecao.buscaProcesso(cpu.getProcessoAtual())
                    if emExecucao.getChegada() == processo.getChegada():
                        if processo.getPrioridade() > emExecucao.getPrioridade():
                            return emExecucao,cpu
        return None,None

#-------------------------------------------------------------------------------------#
# First Come, First Served (Primeiro a chegar, primeiro a ser servido)
class FCFS(Escalonador):
    def __init__(self):
        self.preemptivo = False
        self.quantum = None
        self.nome = 'FCFS'
    #Retorna o primeiro processo que chegou
    def selecionaProcesso(self,listaDeProcessos,tempo):
        processo = listaDeProcessos.remove()
        return processo

    def desempate(self,processo,colecao):
        return None,None

#-------------------------------------------------------------------------------------#
# Round Robin (Chaveamento Circular)
class RR(Escalonador):
    def __init__(self):
        self.preemptivo = False
        self.quantum = 5
        self.nome = 'RR'

    def selecionaProcesso(self,listaDeProcessos,tempo):
        #Tira da cabeça e bota no rabo. (SILVA, D. M. 2017)
        processo = listaDeProcessos.remove()
        return processo

    def desempate(self,processo,colecao):
        return None,None    

#-------------------------------------------------------------------------------------#
# Shortest Job First (Trabalho mais curto primeiro)
class SJF(Escalonador):
    def __init__(self):
        self.preemptivo = False
        self.quantum = None
        self.nome = 'SJF'

    def selecionaProcesso(self,listaDeProcessos,tempo):
        menor = listaDeProcessos.queue[0].getCpuBurstAtual()
        menorProc = listaDeProcessos.queue[0]
        for processo in listaDeProcessos.queue:
            if processo.getCpuBurstAtual() < menor:
                menor = processo.getCpuBurstAtual()
                menorProc = processo
        listaDeProcessos.remove(menorProc.getProcessoId())
        return menorProc

    def desempate(self,processo,colecao):
        if colecao.buscaCpuLivre() == None: #Se houver CPU livre, nao precisa de desempate
            for cpu in colecao.CPUs:
                if not cpu.getDisponivel():
                    print cpu.getDisponivel()
                    emExecucao = colecao.buscaProcesso(cpu.getProcessoAtual())
                    if emExecucao.getChegada() == processo.getChegada():
                        if processo.getCpuBurstAtual() < emExecucao.getCpuBurstAtual(): #Criterio de desempate
                            return emExecucao,cpu
        return None,None   

#-------------------------------------------------------------------------------------#
# Shortes Remaining Time (Menor tempo faltando)
class SRT(Escalonador):
    def __init__(self):
        self.preemptivo = True #Escalonador preemptivo
        self.quantum = None
        self.nome = 'SRT'

    def selecionaProcesso(self,listaDeProcessos,tempo):
        menor = listaDeProcessos.queue[0].getCpuBurstAtual()
        menorProc = listaDeProcessos.queue[0]
        for processo in listaDeProcessos.queue:
            if processo.getCpuBurstAtual() < menor:
                menor = processo.getCpuBurstAtual()
                menorProc = processo
        listaDeProcessos.remove(menorProc.getProcessoId())
        return menorProc

    def recalcula(self,filaDeProntos,colecao,tempoAtual):
        menorBurstPronto = filaDeProntos.queue[0].getCpuBurstAtual()
        menorProcPronto = filaDeProntos.queue[0]
        for processo in filaDeProntos.queue:
            if processo.getCpuBurstAtual() < menorBurstPronto:
                menorBurstPronto = processo.getCpuBurstAtual()
                menorProcPronto = processo
        #neste ponto, ja se obteve o processo com menor tempo restante que esta na fila de prontos
        #Deve-se agora verificar se existe algum processo em execucao que é maior que ele

        #Agora sera identificado o processo de maior tempo restante que esta em execucao
        cpuComMaior = colecao.CPUs[0]
        processoMaior = colecao.buscaProcesso(cpuComMaior.getProcessoAtual())
        burstMaior = processoMaior.getCpuBurstAtual() - (tempoAtual - processoMaior.getInicioExecucao())

        for cpu in colecao.CPUs:
            processo = colecao.buscaProcesso(cpu.getProcessoAtual())
            burstRestante = processo.getCpuBurstAtual() - (tempoAtual - processo.getInicioExecucao())
            if burstRestante > burstMaior:
                processoMaior = processo
                burstMaior = burstRestante
                cpuComMaior = cpu


        #Sera comparado o <processo com menor tempo restante que esta na fila de prontos> com
        #                        <processo com maior tempo restante em execucao>
        #       <Fila>        <Execucao>
        if menorBurstPronto < burstMaior:
            #retira o menor da fila
            filaDeProntos.remove(menorProcPronto.getProcessoId())
            #retorna novo, processoInterrompido, cpuInterrompida
            return menorProcPronto,processoMaior,cpuComMaior
        else:
            return None,None,None

    def desempate(self,processo,colecao):
        if colecao.buscaCpuLivre() == None:
            for cpu in colecao.CPUs:
                if not cpu.getDisponivel():
                    print cpu.getDisponivel()
                    emExecucao = colecao.buscaProcesso(cpu.getProcessoAtual())
                    print cpu.getProcessoAtual()
                    print emExecucao #está none
                    print processo
                    if emExecucao.getChegada() == processo.getChegada():
                        if processo.getCpuBurstAtual() < emExecucao.getCpuBurstAtual(): #Criterio de desempate
                            return emExecucao,cpu
        return None,None




#-----------------------------------FUZZY--------------------------------------------------------#


#Fuzzy Priority CPU Scheduling Algorithm - Bashir et al (2011)
class FPCS(Escalonador):
    def __init__(self):
        self.preemptivo = False #verificar isso
        self.quantum    = None
        self.nome = 'FPCS'

    def selecionaProcesso(self,filaDeProntos,tempo):
        for processo in filaDeProntos.queue:
            self.recalculaPrioridades(processo, tempo)

        filaDeProntos.queue = sorted(filaDeProntos.queue, key = lambda processo: processo.getPrioridadeDinamica(), reverse = True)

        return filaDeProntos.remove()
    
    def recalculaPrioridades(self,processo,tempo):
        # New Antecedent/Consequent objects hold universe variables and membership
        # functions
        tempoEspera = ctrl.Antecedent(np.arange(0, 11, 1), 'tempoEspera') #causa
        tempoRestante = ctrl.Antecedent(np.arange(0, 11, 1), 'tempoRestante') #causa
        prioridade = ctrl.Antecedent(np.arange(0, 11, 1), 'prioridade') #causa
        pDinamica = ctrl.Consequent(np.arange(0, 11, 1), 'pDinamica') #Consequencia

        # Auto-membership function population is possible with .automf(3, 5, or 7)
        #tempoEspera.automf(3)
        #tempoRestante.automf(3)
        #prioridade.automf(3)

        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API 
        
        tempoEspera['curto'] =  fuzz.trimf(tempoEspera.universe, [0,0,4])
        tempoEspera['medio'] = fuzz.trimf(tempoEspera.universe, [0,5,10])
        tempoEspera['longo'] =   fuzz.trimf(tempoEspera.universe, [6,10,10])

        tempoRestante['extremamente curto'] = fuzz.trimf(tempoRestante.universe, [0,0,4])
        tempoRestante['muito curto'] = fuzz.trimf(tempoRestante.universe, [0,5,10])
        tempoRestante['curto'] = fuzz.trimf(tempoRestante.universe, [6,10,10])

        prioridade['baixa'] =  fuzz.trimf(prioridade.universe, [0,0,4])
        prioridade['media'] = fuzz.trimf(prioridade.universe, [0,5,10])
        prioridade['alta'] =   fuzz.trimf(prioridade.universe, [6,10,10])

        names = ['muito baixa','baixa','media','alta','muito alta']
        pDinamica.automf(names = names)
    
        # Creating rules to expert system
        rule1 = ctrl.Rule(prioridade['baixa'] & tempoRestante['extremamente curto'] & tempoEspera['curto'], pDinamica['muito alta'])
        rule2 = ctrl.Rule(prioridade['baixa'] & tempoRestante['extremamente curto'] & tempoEspera['medio'], pDinamica['muito alta'])
        rule3 = ctrl.Rule(prioridade['baixa'] & tempoRestante['extremamente curto'] & tempoEspera['longo'], pDinamica['muito alta'])
        rule4 = ctrl.Rule(prioridade['baixa'] & tempoRestante['muito curto'] & tempoEspera['curto'], pDinamica['muito baixa'])
        rule5 = ctrl.Rule(prioridade['baixa'] & tempoRestante['muito curto'] & tempoEspera['medio'], pDinamica['baixa'])
        rule6 = ctrl.Rule(prioridade['baixa'] & tempoRestante['muito curto'] & tempoEspera['longo'], pDinamica['alta'])
        rule7 = ctrl.Rule(prioridade['baixa'] & tempoRestante['curto'] & tempoEspera['curto'], pDinamica['muito baixa'])
        rule8 = ctrl.Rule(prioridade['baixa'] & tempoRestante['curto'] & tempoEspera['medio'], pDinamica['baixa'])
        rule9 = ctrl.Rule(prioridade['baixa'] & tempoRestante['curto'] & tempoEspera['longo'], pDinamica['alta'])
        rule10 = ctrl.Rule(prioridade['media'] & tempoRestante['extremamente curto'] & tempoEspera['curto'], pDinamica['muito alta'])
        rule11 = ctrl.Rule(prioridade['media'] & tempoRestante['extremamente curto'] & tempoEspera['medio'], pDinamica['muito alta'])
        rule12 = ctrl.Rule(prioridade['media'] & tempoRestante['extremamente curto'] & tempoEspera['longo'], pDinamica['muito alta'])
        rule13 = ctrl.Rule(prioridade['media'] & tempoRestante['muito curto'] & tempoEspera['curto'], pDinamica['media'])
        rule14 = ctrl.Rule(prioridade['media'] & tempoRestante['muito curto'] & tempoEspera['medio'], pDinamica['media'])
        rule15 = ctrl.Rule(prioridade['media'] & tempoRestante['muito curto'] & tempoEspera['longo'], pDinamica['muito alta'])
        rule16 = ctrl.Rule(prioridade['media'] & tempoRestante['curto'] & tempoEspera['curto'], pDinamica['media'])
        rule17 = ctrl.Rule(prioridade['media'] & tempoRestante['curto'] & tempoEspera['medio'], pDinamica['media'])
        rule18 = ctrl.Rule(prioridade['media'] & tempoRestante['curto'] & tempoEspera['longo'], pDinamica['alta'])
        rule19 = ctrl.Rule(prioridade['alta'] & tempoRestante['extremamente curto'] & tempoEspera['curto'], pDinamica['muito alta'])
        rule20 = ctrl.Rule(prioridade['alta'] & tempoRestante['extremamente curto'] & tempoEspera['medio'], pDinamica['muito alta'])
        rule21 = ctrl.Rule(prioridade['alta'] & tempoRestante['extremamente curto'] & tempoEspera['longo'], pDinamica['muito alta'])
        rule22 = ctrl.Rule(prioridade['alta'] & tempoRestante['muito curto'] & tempoEspera['curto'], pDinamica['alta'])
        rule23 = ctrl.Rule(prioridade['alta'] & tempoRestante['muito curto'] & tempoEspera['medio'], pDinamica['alta'])
        rule24 = ctrl.Rule(prioridade['alta'] & tempoRestante['muito curto'] & tempoEspera['longo'], pDinamica['muito alta'])
        rule25 = ctrl.Rule(prioridade['alta'] & tempoRestante['curto'] & tempoEspera['curto'], pDinamica['alta'])
        rule26 = ctrl.Rule(prioridade['alta'] & tempoRestante['curto'] & tempoEspera['medio'], pDinamica['alta'])
        rule27 = ctrl.Rule(prioridade['alta'] & tempoRestante['curto'] & tempoEspera['longo'], pDinamica['muito alta'])

        dinamicP_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27,])
        dinamicP = ctrl.ControlSystemSimulation(dinamicP_ctrl)

        # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
        # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
        dinamicP.input['prioridade'] = processo.getPrioridade()

        tRestante = 0
        for burst in processo.getBursts():
            tRestante += burst

        dinamicP.input['tempoRestante'] = tRestante
        dinamicP.input['tempoEspera'] = tempo - processo.getChegada()

        # Crunch the numbers
        dinamicP.compute()

        dPrioridade = dinamicP.output['pDinamica']
        processo.setPrioridadeDinamica(dPrioridade)


    def desempate(self,processo,colecao):
        return None,None
#------------------------------------------------------------------------------------------------#
#Improved Fuzzy-Based CPU Scheduling - Behera et al (2012)
class IFCS(Escalonador):
    def __init__(self):
        self.preemptivo = False
        self.quantum = None
        self.nome = 'IFCS'
        self.bti = []
        self.pti = []
        self.ati = []
        self.rri = []

        self.pId = []        


    def selecionaProcesso(self,filaDeProntos,tempo):
        #Caso tenha algum processo sem prioridade dinamica calculada
        #percorre os precessos calculando
        self.recalculaPrioridades(filaDeProntos,tempo)
        processo = filaDeProntos.remove()
        #processo.setRriCongelado(True)
        print processo.getProcessoId()
        return processo


    def recalculaPrioridades(self,filaDeProntos,tempo):
        responseR = 0.0

        for i in xrange(len(filaDeProntos.queue)):
            if filaDeProntos.queue[i].getProcessoId() not in self.pId:
                self.pId.append(filaDeProntos.queue[i].getProcessoId())
                self.bti.append(filaDeProntos.queue[i].getCpuBurstAtual())
                self.pti.append(filaDeProntos.queue[i].getPrioridade())
                tempoEstimado = 0
                for burst in filaDeProntos.queue[i].getBursts():
                    tempoEstimado += burst
                #ver como calcular response ratio -> (tempo de espera + tempo estimado de execucao)/tempo estimado de execucao
                esperaAtual = tempo - filaDeProntos.queue[i].getChegada()
                #if not filaDeProntos.queue[i].getRriCongelado():
                if i == 0:
                    responseR = (esperaAtual + tempoEstimado)/float(tempoEstimado)
                else:
                    responseR = (esperaAtual + (tempo - filaDeProntos.queue[i-1].getChegada()) + filaDeProntos.queue[i-1].getCpuBurstAtual())/float(tempoEstimado)
                filaDeProntos.queue[i].setRri(responseR)

                #print 'ID ',filaDeProntos.queue[i].getProcessoId()
                #print 'Tempo esp ',esperaAtual
                #print 'tempo est ',tempoEstimado
                #print 'response ', responseR
                self.rri.append(filaDeProntos.queue[i].getRri())

        for i in xrange(len(filaDeProntos.queue)):
            for j in xrange(len(self.pId)):
                if self.pId[j] == filaDeProntos.queue[i].getProcessoId():
                    #print filaDeProntos.queue[i].getProcessoId()
                    up = self.pti[j]/float((max(self.pti) + 1))
                    ub = 1 - (self.bti[j]/float((max(self.bti) + 1)))
                    uh = self.rri[j]/float((max(self.rri) + 1))
                    #print self.rri[j],max(self.rri) + 1

            #print '--------------'
            #print 'up: ', up
            #print 'ub: ', ub
            #print 'uh: ', uh
            pDinamica = max(up,ub,uh)
            filaDeProntos.queue[i].setPrioridadeDinamica(pDinamica)
            #print 'id ', filaDeProntos.queue[i].getProcessoId()
            #print 'pd ', pDinamica
        #Evaluate μp i.e membership value of task priority for
        #individual processes by using the formula
        #up = actual task priority/(maximum task priority+1)

        #Evaluate μb that is membership value of burst time for
        #individual processes
        #print 'Pid', self.pId
        #print 'pti', self.pti
        #print 'bti', self.bti
        #print 'rri', self.rri
        up = 0.0
        ub = 0.0
        uh = 0.0

        #ordena fila de prontos
        filaDeProntos.queue = sorted(filaDeProntos.queue, key = lambda processo: processo.getPrioridadeDinamica(), reverse = True)

    def desempate(self,processo,colecao):
        if colecao.buscaCpuLivre() == None:
            lista = Fila()
            for p in colecao.Processos:
                if (p.getChegada() <= processo.getChegada()) and (len(p.getBursts())>0):
                    lista.insert(p)

            for cpu in colecao.CPUs:
                if cpu.getDisponivel():
                    return None,None
                else:
                    emExecucao = colecao.buscaProcesso(cpu.getProcessoAtual())
                    if emExecucao.getChegada() == processo.getChegada():
                        self.recalculaPrioridades(lista,processo.getChegada())
                        if emExecucao.getPrioridadeDinamica() < processo.getPrioridadeDinamica():
                            return emExecucao,cpu
        return None,None
#------------------------------------------------------------------------------------------------#
#Proposed Fuzzy CPU Scheduling Algorithm - Ajmani (2013)
class PFCS(Escalonador):
    def __init__(self):
        self.preemptivo = False
        self.quantum = None
        self.nome = 'PFCS'

        self.bti = []
        self.pti = []
        self.ati = []
        self.pId = []          

    def selecionaProcesso(self,filaDeProntos,tempo):
        #Caso tenha algum processo sem prioridade dinamica calculada
        #percorre os precessos calculando
        self.recalculaPrioridades(filaDeProntos,tempo)
        processo = filaDeProntos.remove()
        #processo.setRriCongelado(True)
        return processo       

    def recalculaPrioridades(self,filaDeProntos,tempo):

        for i in xrange(len(filaDeProntos.queue)):
            if filaDeProntos.queue[i].getProcessoId() not in self.pId:
                print 'Armazenar o ',filaDeProntos.queue[i].getProcessoId()
                self.pId.append(filaDeProntos.queue[i].getProcessoId())
                self.bti.append(filaDeProntos.queue[i].getCpuBurstAtual())
                self.pti.append(filaDeProntos.queue[i].getPrioridade())

        for i in xrange(len(filaDeProntos.queue)):
            for j in xrange(len(self.pId)):
                if self.pId[j] == filaDeProntos.queue[i].getProcessoId():
                    print 'id', filaDeProntos.queue[i].getProcessoId()
                    up = self.pti[j]/(float(max(self.pti)) + 1)
                    print 'bti ',self.bti[j]
                    print 'max bti ',max(self.bti)
        
                    ub = 1 - (self.bti[j]/float(max(self.bti) + 1))
                    if filaDeProntos.queue[i].getPrioridade() == min(self.pti):
                        pDinamica = up+ub
                        filaDeProntos.queue[i].setPrioridadeDinamica(pDinamica)
                    else:
                        pDinamica = max(up,ub)
                        filaDeProntos.queue[i].setPrioridadeDinamica(pDinamica)

            print '--------------'
            print 'up: ', up
            print 'ub: ', ub
            print 'id ', filaDeProntos.queue[i].getProcessoId()
            print 'pd ', pDinamica
            filaDeProntos.queue = sorted(filaDeProntos.queue, key = lambda processo: processo.getPrioridadeDinamica(), reverse = True)               

    def desempate(self,processo,colecao):
        if colecao.buscaCpuLivre() == None:
            lista = Fila()
            for p in colecao.Processos:
                if (p.getChegada() <= processo.getChegada()) and (len(p.getBursts())>0):
                    lista.insert(p)

            for cpu in colecao.CPUs:
                if cpu.getDisponivel():
                    return None,None
                else:
                    emExecucao = colecao.buscaProcesso(cpu.getProcessoAtual())
                    if emExecucao.getChegada() == processo.getChegada():
                        self.recalculaPrioridades(lista,processo.getChegada())
                        if emExecucao.getPrioridadeDinamica() < processo.getPrioridadeDinamica():
                            print 'V processo: ', processo.getProcessoId()
                            print 'x emExecucao: ', emExecucao.getProcessoId()
                            return emExecucao,cpu
        return None,None




        '''        
        lista = []

        for p in colecao.Processos:
            if p.getChegada() == processo.getChegada(): 
                lista.append(p)

        #1) For each process Pi in ready queue fetch its parameters
        #burst time (bti), static priority (pti), and arrival time (ati)
        #and give them as input to FIS.

        #bti = Burst time
        #pti = Prioridade estatica
        #ati = Tempo de chegada

        #É necessário conhecer o Max(pti) e o Max(bti)

        bti = []
        pti = []
        ati = []

        for processo in lista:
            bti.append(processo.getCpuBurstAtual())
            pti.append(processo.getPrioridade())
            ati.append(processo.getChegada())

        for i in xrange(len(lista)):
            up = pti[i]/float(max(pti)) + 1
            ub = 1 - (bti[i]/float(max(bti)) + 1)
            if lista[i].getPrioridade() == min(pti):
                lista[i].setPrioridadeDinamica(up+ub)
            else:
                lista[i].setPrioridadeDinamica(max(up,ub))

        #ordena fila de prontos
        ordenada = sorted(lista, key = lambda processo: processo.getPrioridadeDinamica())
        print ordenada
        aux = []
        for cpu in colecao.CPUs:
            if cpu.getDisponivel():
                return None,None
            else:                
                aux.append(colecao.buscaProcesso(cpu.getProcessoAtual()).getPrioridadeDinamica())

        for cpu in colecao.CPUs:
            if colecao.buscaProcesso(cpu.getProcessoAtual()).getPrioridadeDinamica() == min(aux):
                print 'aaaaaaa'
                if colecao.buscaProcesso(cpu.getProcessoAtual()).getPrioridadeDinamica() < ordenada[0].getPrioridadeDinamica():
                    return colecao.buscaProcesso(cpu.getProcessoAtual()),cpu

        return None,None
        '''