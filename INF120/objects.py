#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 20:54:57 2022

__author__ = "Simen Roko Krogstie"
__email__ = "simen.roko.krogstie@nmbu.no"
"""
import random

class Katt:
    def __init__(self):
        self.dyre_slag = 'katt'
        self.antall_bein = 4
    
    def __str__(self):
        return 'Dyret er en {0} med {1} bein.'.format(self.dyre_slag, self.antall_bein)
    

class Hund:
    def __init__(self):
        self.dyre_slag = 'hund'
        self.antall_bein = 4
        
    def __str__(self):
        return 'Dyret er en {0} med {1} bein.'.format(self.dyre_slag, self.antall_bein)
    
    
class Undulat:
    def __init__(self):
        self.dyre_slag = 'Undulat'
        self.antall_bein = 2
    
    def __str__(self):
        return 'Dyret er en {0} med {1} bein.'.format(self.dyre_slag, self.antall_bein)
    
def lag_familiedyr(antall=2):
    familie_dyr = []
    i = 0
    while i < antall:
        dyr = [Katt(), Hund(), Undulat()]
        x = random.choice(dyr)
        familie_dyr.append(x)
        i += 1
    return familie_dyr


liste_med_dyr = lag_familiedyr(4)
for i, dyr in enumerate(liste_med_dyr):
    print(f'{i+1}: {dyr}')

