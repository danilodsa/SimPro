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
from Load import *
from math import * 
from Cpu import *
from Dispositivo import *
from Processo import *
import random


class Colecoes(object):
	CPUs = []
	Dispositivos = []
	Processos = []
	Finalizados = []
	nProcessos = 0

	#Retorna a Primeira CPU livre que encontrar na colecao
	def buscaCpuLivre(self):
		for cpu in self.CPUs:
			if cpu.getDisponivel():
				return cpu
		else:
			return None

	def buscaCpu(self, ident):
		for cpu in self.CPUs:
			if cpu.getCpuId() == ident:
				return cpu

		return None

	def buscaDispositivo(self, ident):
		for dispositivo in self.Dispositivos:
			if dispositivo.getDispositivoId() == ident:
				return dispositivo
				
		return None

	def buscaProcesso(self, ident):
		for processo in self.Processos:
			if processo.getProcessoId() == ident:
				return processo
				
		return None

	def finalizaProcesso(self,ident):
		for i in xrange(len(self.Processos)):
			if self.Processos[i].getProcessoId() == ident:
				self.Finalizados.append(self.Processos[i])
				del self.Processos[i]
				return

		return

