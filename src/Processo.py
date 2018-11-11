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

from math import *

#https://docs.python.org/3.0/library/random.html
import random

class Processo(object):

	#Construtor de processos#
	def __init__(self,ident,quantum,nIOdist,ioBurstDist,cpuBurstDist,dispositivoId,chegada,prioridade,lista=None):

	
		self.inicioExecucao = 0.0
		self.terminoExecucao = 0.0

		#variavel para controlar o tempo de execução total
		self.tempoExecucao = 0.0

		#variavel para controlar o tempo de espera total
		self.tempoEspera = 0.0

		self.cpuBursts = []
		self.ioBursts = []
		self.nIoBursts = 0
		self.nCpuBursts = 0	

		self.dPrioridade = 0.0
		self.rri = 0.0
		self.processoId = 0

		if lista != None: #Deterministico
			# [identificador][chegada][burst][prioridade]
			self.setProcessoId(lista[0])
			self.nCpuBursts = 1
			self.chegada = lista[1]
			self.cpuBursts.append(lista[2])
			self.prioridade = lista[3]
			self.setQuantum(quantum)
			self.tempoAuxiliar = self.chegada
		else: #Probabilistico
			self.tempoAuxiliar = chegada
			self.chegada = chegada						

			self.setProcessoId(ident)

			self.prioridade = int(random.triangular(prioridade[0],prioridade[2],prioridade[1])) #Prioridade Estatica

			self.setQuantum(quantum)
			
			if (nIOdist[0] == 0) and (nIOdist[1] == 0) and (nIOdist[2] == 0):
				self.nIoBursts = 0
			else:	
				self.nIoBursts = int(random.triangular(nIOdist[0],nIOdist[2],nIOdist[1]))
			
			self.nCpuBursts = self.nIoBursts + 1

			self.setDispositivo(dispositivoId)

			for i in range(0,self.nCpuBursts):
				self.cpuBursts.append(int(random.triangular(cpuBurstDist[0],cpuBurstDist[2],cpuBurstDist[1])))
		
			for i in range(0,self.nIoBursts):
				self.ioBursts.append(int(random.triangular(ioBurstDist[0],ioBurstDist[2],ioBurstDist[1])))

		self.dicionarioExecucao = []
		
	def setRri(self,valor):
		self.rri = valor

	def getRri(self):
		return self.rri

	def getBursts(self):
		return self.cpuBursts

	def getExecucoes(self):
		return self.dicionarioExecucao

	def insereExecucao(self):
		nome = "p" + str(self.getProcessoId())

		tempoI = self.converteTempo(self.getInicioExecucao())
		tempoT = self.converteTempo(self.getTerminoExecucao())

		inicio = '2018-01-01 ' + tempoI
		termino = '2018-01-01 ' + tempoT
		self.dicionarioExecucao.append([nome, inicio, termino])

	def recalculaExecucao(self):
		self.dicionarioExecucao[(len(self.dicionarioExecucao)-1):][0][2] = '2018-01-01 ' + self.converteTempo(self.getTerminoExecucao())

	def getTempoExecucao(self):
		return self.tempoExecucao

	def incExecucao(self,tempo):
		self.tempoExecucao += (tempo - self.tempoAuxiliar)
		self.tempoAuxiliar = tempo

	def getTempoEspera(self):
		return self.tempoEspera

	def setAuxiliar(self,tempo):
		self.tempoAuxiliar = tempo

	def incEspera(self,tempo):
		self.tempoEspera += (tempo - self.tempoAuxiliar)
		self.tempoAuxiliar = tempo

	def getPrioridade(self):
		return self.prioridade

	def setPrioridadeDinamica(self,dpi):
		self.dPrioridade = dpi

	def getPrioridadeDinamica(self):
		return self.dPrioridade

	def setTerminoExecucao(self,tempo):
		self.terminoExecucao = tempo

	def getTerminoExecucao(self):
		return self.terminoExecucao

	def getChegada(self):
		return self.chegada

	def setInicioExecucao(self,tempo):
		self.inicioExecucao = tempo

	def getInicioExecucao(self):
		return self.inicioExecucao

	def setProcessoId(self,ident):
		self.processoId = ident

	def getProcessoId(self):
		return self.processoId

	def getnCpuBursts(self):
		return self.nCpuBursts

	def getnIoBursts(self):
		return self.nIoBursts

	def setQuantum(self,quantum):
		self.quantum = quantum

	def getQuantum(self):
		return self.quantum

	def decrementaIoBursts(self):
		del self.ioBursts[0]
		self.nIoBursts -= 1

	def decrementaCpuBursts(self):
		del self.cpuBursts[0]
		self.nCpuBursts -= 1

	def getIoBurstAtual(self):
		return self.ioBursts[0]

	def getCpuBurstAtual(self):
		return self.cpuBursts[0]

	def setDispositivo(self,disp):
		self.dispositivoId = disp

	def getDispositivo(self):
		return self.dispositivoId

	def reduzCpuBurst(self,valor):
		tempo = valor - self.getInicioExecucao()
		print 'REDUCAO DE CPU BURST'
		print 'tempo ', tempo
		print 'BURST ', self.cpuBursts[0]

		self.cpuBursts[0] -= tempo

	def subQuantum(self):
		print 'REDUCAO DE CPU BURST (quantum)'
		print 'tempo ', self.quantum
		print 'BURST ', self.cpuBursts[0]

		if self.quantum > self.cpuBursts[0]:
			self.decrementaCpuBursts()
			return False
		else:
			self.cpuBursts[0] -= self.quantum
			print 'Reduziu: ', self.cpuBursts[0]
			return True

	def converteTempo(self,tempo):
		t1 = int(tempo%60) #00:00:[00]
		aux = int(tempo/60)
		if  aux < 60:
			t2 = aux #00:[00]:00
			t3 = 00
		else:
			t2 = aux/60
			t3 = aux%60

		if t1<10:
			st1 = '0'+str(t1)
		else:
			st1 = str(t1)

		if t2<10:
			st2 = '0'+str(t2)
		else:
			st2 = str(t2)

		if t3<10:
			st3 = '0'+str(t3)	
		else:
			st3 = str(t3)


		t = st3+':'+st2+':'+st1
		return t

#------------------------------------------#