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

class Dispositivo(object):

    dispositivoId   = None
    filaIO          = None
    processoAtual   = None
    disponivel      = None

    def __init__(self,ident):
        self.filaIO             = Fila()
        self.processoAtual      = 0
        self.disponivel         = True

        self.setDispositivoId(ident)

    def setDispositivoId(self,ident):
        self.dispositivoId = ident

    def getDispositivoId(self):
        return self.dispositivoId

    def setProcessoAtual(self,processo):
        self.processoAtual = processo

    def getProcessoAtual(self):
        return self.processoAtual

    def setDisponivel(self,flag):
        self.disponivel = flag

    def getDisponivel(self):
        return self.disponivel

#------------------------------------------#