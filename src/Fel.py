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

from Eventos import *
import sys

class Fel(object):

    fel = None
    tempo = None
    eventos = None
    eventoId = None

    def __init__(self,escalonador,cenario,modelo):
        self.fel = []
        self.tempo = 0.0
        self.eventoId = 0
    
        self.eventos = Evento(escalonador,cenario,modelo)
        agendar = self.eventos.start() 

        self.agendaEvento(agendar)

    def getTempo(self):
        return self.tempo

    def setTempo(self,tempo):
        self.tempo = tempo

    def getFel(self):
        return self.fel


    #Agenda o evento
    def agendaEvento(self,listaEventos):
        print '----LISTA PARA AGENDAR------'
        print listaEventos
        if len(listaEventos) > 0:
            for evento in listaEventos:
                pos = 0
                self.eventoId += 1 
                if(len(self.fel) == 0): #Caso a fel esteja vazia
                    self.fel.append(evento)
                elif evento[0] == 0:
                    self.fel.insert(0,evento)
                else:
                    for eventoAgendado in self.fel: #Enquanto o tempo do evento for maior, percorre FEL
                        if(evento[1] < eventoAgendado[1]):
                            break;
                        else:
                            pos = pos + 1
                    self.fel.insert(pos, evento)
        else:
            pass
        print 'Agendado'
        

    #Desagenda Evento
    def desagendaEvento(self,processoId,cpuId): #desagenda evento

        for i in xrange(len(self.fel)):
            evento = self.fel[i]
            #Buscando execucao agendada
            if evento[0] == 2: 
                if evento[2] == processoId:
                    if evento[3] == cpuId:
                        self.fel.pop(i)
                        break
        print self.fel
        #quit()


    def consome(self): #Consome o próximo evento da fel
        evento = self.getProximo()
        self.remove()
        print evento

        agendar = []
        if (evento[0] == 1): #fimChegadaProcessoCPU(self,tempo)#
            self.setTempo(evento[1])
            agendar = self.eventos.fimChegadaProcessoCPU(self.getTempo(),evento[2])
            print 'Fim Chegada de processo'
            self.agendaEvento(agendar)

        elif (evento[0] == 2): #fimExecutaCPU(self,tempo,processo,cpu)#
            self.setTempo(evento[1])
            print self.getTempo()
            agendar = self.eventos.fimExecutaCPU(self.getTempo(),evento[2],evento[3])
            print 'Fim execucao na cpu'
            self.agendaEvento(agendar)

        elif (evento[0] == 3): #fimExecutaIO(self,tempo,processo)#
            self.setTempo(evento[1])
            agendar = self.eventos.fimExecutaIO(self.getTempo(),evento[2])
            print 'Fim execucao IO'
            self.agendaEvento(agendar)

        elif (evento[0] == 4):#fimEncerraProcesso(self,tempo,processo)#
            self.setTempo(evento[1])
            agendar = self.eventos.fimEncerraProcesso(self.getTempo(),evento[2])
            print 'Fim Encerra Processo'      
            self.agendaEvento(agendar)
        elif (evento[0] == 0):#Desagendar algum evento na fel
            self.desagendaEvento(evento[1],evento[2])


    def remove(self):
        del self.fel[0]

    def getProximo(self):
        if len(self.fel) > 0:
            return self.fel[0]
        else:
            print '# -Fim de Execucao- #'
            sys.exit()


    def fimExecucao(self):
        print 'Chamar Fim EVENTO'
        self.eventos.fimExecucao(self.getTempo())

    def toString(self):
        pass
        #1 - Chegada de processo
        #2 - Execução na CPU
        #3 - Execução IO
        #4 - Fim de execucao