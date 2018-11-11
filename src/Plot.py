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

import plotly as cred
from plotly.offline import plot
import plotly.figure_factory as ff
import plotly.graph_objs as go


class Plot(object):
	def __init__(self):
		self.dados = [] #dados do gráfico

	def geraGraficoUtilizacaoGlobal(self,cpus):
		x = cpus[0].getUtilizacao()[0]
		y = []
		for i in xrange(0,len(cpus[0].getUtilizacao()[2])):
			aux = 0
			for cpu in cpus:
				aux += cpu.getUtilizacao()[2][i] #soma dos valores de utilização
			if x[i] == 0:
				y.append(0)
			else:
				y.append((aux/(x[i]*len(cpus)))*100)

		trace0 = go.Scatter(
				x = x,
				y = y,
				mode = 'lines',
				name = 'CPUs')
		data = [trace0]
		plot(data,filename='cpuUtiG.html')		



	def geraGraficoUtilizacao(self, cpus): #utilizacao individual
		#for cpu in cpus:
		#	globals()['trace_cpu%s' % cpu.getCpuId()] = 			 

		if len(cpus) == 1:
			#plot({"data":[go.Scatter(x=cpus[0].getUtilizacao()[0],y=cpus[0].getUtilizacao()[1])],"layout": go.Layout(title="UtilizacaoCPU")})
			trace0 = go.Scatter(
    				x = cpus[0].getUtilizacao()[0],
    				y = cpus[0].getUtilizacao()[1],
    				mode = 'lines',
    				name = 'CPU1')
			data = [trace0]
			plot(data,filename='cpuUti.html')

		elif len(cpus) == 2:
			trace0 = go.Scatter(
    				x = cpus[0].getUtilizacao()[0],
    				y = cpus[0].getUtilizacao()[1],
    				mode = 'lines',
    				name = 'CPU1')
			trace1 = go.Scatter(
    				x = cpus[1].getUtilizacao()[0],
    				y = cpus[1].getUtilizacao()[1],
    				mode = 'lines',
    				name = 'CPU2')
			data = [trace0,trace1]
			plot(data,filename='cpuUti.html')
		elif len(cpus) == 4:
			trace0 = go.Scatter(
    				x = cpus[0].getUtilizacao()[0],
    				y = cpus[0].getUtilizacao()[1],
    				mode = 'lines',
    				name = 'CPU1')
			trace1 = go.Scatter(
    				x = cpus[1].getUtilizacao()[0],
    				y = cpus[1].getUtilizacao()[1],
    				mode = 'lines',
    				name = 'CPU2')
			trace2 = go.Scatter(
    				x = cpus[2].getUtilizacao()[0],
    				y = cpus[2].getUtilizacao()[1],
    				mode = 'lines',
    				name = 'CPU3')
			trace3 = go.Scatter(
    				x = cpus[3].getUtilizacao()[0],
    				y = cpus[3].getUtilizacao()[1],
    				mode = 'lines',
    				name = 'CPU4')
			data = [trace0,trace1,trace2,trace3]
			plot(data,filename='cpuUti.html')
		elif len(cpus) == 8:
			pass


	def geraGraficoProcessos(self, processos):
		self.dados = [] #dados do gráfico
		procOrd = sorted(processos, key = lambda processo: processo.getProcessoId())

		for processo in procOrd:
			for execucao in processo.getExecucoes():
				nome 	= execucao[0]
				inicio 	= execucao[1]
				termino = execucao[2]
				self.dados.append(dict(Task=nome, Start=inicio, Finish=termino))


		fig = ff.create_gantt(self.dados, colors=['#333F44'], group_tasks=True, showgrid_x=True, showgrid_y=True)
		plot(fig, filename='process-job.html')


	def geraGraficoCPUs(self, cpus):
		self.dados = [] #dados do gráfico
		for cpu in cpus:
			for execucao in cpu.getExecucoes():
				nome 	= execucao[0]
				inicio 	= execucao[1]
				termino = execucao[2]
				self.dados.append(dict(Task=nome, Start=inicio, Finish=termino))

		fig = ff.create_gantt(self.dados, colors=['#333F44'], group_tasks=True, showgrid_x=True, showgrid_y=True)
		plot(fig, filename='CPU-job.html')