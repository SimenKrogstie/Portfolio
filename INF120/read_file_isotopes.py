#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 16:24:20 2022

__author__ = "Simen Roko Krogstie"
__email__ = "simen.roko.krogstie@nmbu.no"

"""

with open('Oxygen.txt', 'r') as infile:
    lines = infile.readlines()
    lines_with_data = lines[1:]
    
    molarmasse = 0
    for element in lines_with_data:
        numbers = element.split()
        molarmasse_ = float(numbers[1]) * float(numbers[2])
        molarmasse  += molarmasse_

print(f"Oksygens molare masse er {molarmasse:.4f} g/mol")
        
# a) Oksygen sin molare masse er 15.9994 g/mol
    
        

    