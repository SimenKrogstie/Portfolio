#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 13:02:47 2022

__author__ = Simen Roko Krogstie
__email__ = simen.roko.krogstie@nmbu.no

"""

def innlesing():
    vareliste = []
    Q = True
    while Q == True:
        vare = input('Vare beskrivelse (blank for å avslutte innlesing): ') 
        if vare == "":
            Q = False
            break       
        while True:
            try:
                antall = int(input('Antall: '))
                break
            except:
                print('Antall må være et tall, prøv igjen')
        while True:       
            try:
                pris = float(input('Pris: '))
                break
            except:
                print('Pris må være et tall, prøv igjen')
        vareliste.append((vare, antall, pris))  
    return(vareliste)

vareliste = innlesing()


def utskrift(vareliste):
    total_sum = 0
    print(f"{'Beskrivelse' : <25} {'Linjekost' : >25}")
    print('---------------------------------------------------')
    for i in range(0, len(vareliste)):
        totalpris = vareliste[i][1] * vareliste[i][2]
        total_sum += totalpris
        totalpris_ = (f"{totalpris:.2f}")  
        print(f"{vareliste[i][0] : <23} {totalpris_ : >24} kr") 
    print('---------------------------------------------------')
    totalsum = (f"{total_sum:.2f}")  # 
    print(f"{'Sum' : <3} {totalsum : >44} kr") 
                                               
     
utskrift(vareliste)


        
        
        
        
        
        
        