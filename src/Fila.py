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

class Fila(object):
            
    def __init__(self):
        self.queue = []      

    def insert(self,element):
        self.queue.append(element)

    def remove(self,ident=None):
        if(not self.empty()):
            if ident == None:
                head = self.queue[0]
                del self.queue[0]
                return head
            else:
                for processo in self.queue:
                    if processo.getProcessoId() == ident:
                        pos = self.queue.index(processo)
                        del self.queue[pos]
        else:
            return "Empty Queue"    

    def empty(self):
        if(len(self.queue) == 0):
            return True
        else:
            return False              

    def toString(self):
        temp = ""

        for x in self.queue:
            temp = temp + str(x) + '\n'
        
        return temp

        