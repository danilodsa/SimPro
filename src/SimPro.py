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

from Escalonador import *
from Eventos import *
from Fel import *

import sys


def main():
	
	if len(sys.argv) < 4:
		print 'Parametros incorretos'
		print 'python Main.py [escalonador] [arquivo.txt] [P/D] '
		quit()

	argEsc = sys.argv[1] #Escalonador: FCFS
	argCen = sys.argv[2] #Cenario: Cenario33.txt
	argDPr = sys.argv[3] #Modelo: P ou D (probabilistico ou deterministico)

	escalonador = defineEscalonador(argEsc)

	fel = Fel(escalonador,argCen,argDPr)

	if argDPr == 'D':
		while len(fel.getFel()) > 0:
			fel.consome()
			print '---------FEL---------'
			print fel.fel
			print 'Tempo Atual: ',fel.getTempo()		
	elif argDPr == 'P':
		while fel.getTempo() < fel.eventos.tempoSimulacao:
			fel.consome()
			print '---------FEL---------'
			print fel.fel
			print 'Tempo Atual: ',fel.getTempo()
		#	raw_input('')
	


	fel.fimExecucao()
	print '# -Fim de Execucao- #'


if __name__ == "__main__":
    main()