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

class Cenario(object):

	def __init__(self):
		self.tempoSimulacao = 0.0
		self.nCPUs 			= 0
		self.nDispositivos 	= 0

		#--------------------#
		self.tempoChegadaProcesso 	= 0
		self.tempoEncProcesso		= []
		self.nIObursts 				= []
		self.duracaoCPUburst 		= []
		self.duracaoIOburst 		= []
		self.prioridade				= []

		self.listaDeProcessos 		= []


	def carregaCenario(self,fileName,modelo):
		cenario = open(fileName, 'r') 
		texto = cenario.readlines()

		if modelo == 'D': #deterministico
			#[id,chegada,CPUburst,prioridade]
			for linha in texto:
				if linha.find('#') != -1:
					pass #comentarios
				else:
					linha = linha.split(' ')
					if linha[0] == 'P': #dados de processo
						proc = [int(linha[1]),int(linha[2]),int(linha[3]),int(linha[4])]
						self.listaDeProcessos.append(proc)
		elif modelo == 'P': #probabilistico
			for linha in texto:
				if linha.find('#') != -1:
					pass #comentarios do arq
				else:
					linha = linha.split(' ')
					#DADOS SIMULACAO
					if linha[0] == 'S':
						if linha[1] == 'TS':
							self.tempoSimulacao = int(linha[2])
					#DADOS PROCESSO
					elif linha[0] == 'P':
						if linha[1] == 'CH':
							self.tempoChegadaProcesso = float(linha[2])
						elif linha[1] == 'PR':
							self.prioridade.append(float(linha[2]))
							self.prioridade.append(float(linha[3]))
							self.prioridade.append(float(linha[4]))
						elif linha[1] == 'EN':
							self.tempoEncProcesso.append(float(linha[2]))
							self.tempoEncProcesso.append(float(linha[3]))
							self.tempoEncProcesso.append(float(linha[4]))
						elif linha[1] == 'NI':
							self.nIObursts.append(float(linha[2]))
							self.nIObursts.append(float(linha[3]))
							self.nIObursts.append(float(linha[4]))
						elif linha[1] == 'DI':
							self.duracaoIOburst.append(float(linha[2]))
							self.duracaoIOburst.append(float(linha[3]))
							self.duracaoIOburst.append(float(linha[4]))
						elif linha[1] == 'DC':
							self.duracaoCPUburst.append(float(linha[2]))
							self.duracaoCPUburst.append(float(linha[3]))
							self.duracaoCPUburst.append(float(linha[4]))
					#DADOS CPUS
					elif linha[0] == 'C':
						if linha[1] == 'QT':
							self.nCPUs = int(linha[2])
					#DADOS MEMORIA
					elif linha[0] == 'M':
						if linha[1] == 'QT':
							self.tamMemoria = int(linha[2])
					#DADOS DISPOSITIVOS
					elif linha[0] == 'D':
						if linha[1] == 'QT':
							self.nDispositivos = int(linha[2])