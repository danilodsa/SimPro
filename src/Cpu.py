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
class CPU(object):

	def __init__(self,ident=None):

		self.cpuId 				= 0
		self.processoAtual 		= 0
		self.disponivel			= True

		self.tempoAuxiliar 		= 0.0

		self.inicioExecucao 	= 0.0
		self.terminoExecucao 	= 0.0


		if ident != None:
			self.setCpuId(ident)
		else:
			pass

		#Metricas de utilizacao# A ociosidade da cpu consiste no (fim - inicio)
		#self.ultimaUtilizacao = 0.0
		#self.inicioUtilizacao = 0.0
		#self.ociosidade = 0.0

		self.totalOciosidade = 0.0
		self.totalExecucao = 0.0

		self.dicionarioExecucao = []
		self.dicionarioUtilizacao = [[],[],[]] #[tempo],[utilizacao em %],[utilizacao em tempo]

	def insereUtilizacaoAtual(self,tempo):
		#x
		self.dicionarioUtilizacao[0].append(tempo)
		#y
		if tempo == 0:
			self.dicionarioUtilizacao[1].append(0)
		else:	
			self.dicionarioUtilizacao[1].append((self.getTotalExecucao()*100)/tempo)
			self.dicionarioUtilizacao[2].append(self.getTotalExecucao())

	def getUtilizacao(self):
		return self.dicionarioUtilizacao

	def setTerminoExecucao(self,tempo):
		self.terminoExecucao = tempo

	def getTerminoExecucao(self):
		return self.terminoExecucao

	def setInicioExecucao(self,tempo):
		self.inicioExecucao = tempo

	def getInicioExecucao(self):
		return self.inicioExecucao

	def getExecucoes(self):
		return self.dicionarioExecucao

	def insereExecucao(self):
		nome = "CPU" + str(self.getCpuId())

		tempoI = self.converteTempo(self.getInicioExecucao())
		tempoT = self.converteTempo(self.getTerminoExecucao())

		inicio = '2018-01-01 ' + tempoI
		termino = '2018-01-01 ' + tempoT
		self.dicionarioExecucao.append([nome, inicio, termino])

	def recalculaExecucao(self):
		self.dicionarioExecucao[(len(self.dicionarioExecucao)-1):][0][2] = '2018-01-01 ' + self.converteTempo(self.getTerminoExecucao())

	def incOciosidade(self,tempo):
		self.totalOciosidade += (tempo - self.tempoAuxiliar)
		self.tempoAuxiliar = tempo

	def getTotalOciosidade(self):
		return self.totalOciosidade

	def incExecucao(self,tempo):
		self.totalExecucao += (tempo - self.tempoAuxiliar)
		self.tempoAuxiliar = tempo

	def getTotalExecucao(self):
		return self.totalExecucao

	def getCpuId(self):
		return self.cpuId

	def setCpuId(self,ident):
		self.cpuId = ident
	
	def getProcessoAtual(self):
		return self.processoAtual

	def setProcessoAtual(self,processo):
		self.processoAtual = processo

	def getDisponivel(self):
		return self.disponivel

	def setDisponivel(self,flag):
		self.disponivel = flag

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