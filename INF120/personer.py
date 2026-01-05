#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 14:00:30 2022

__author__ = "Simen Roko Krogstie"
__email__ = "simen.roko.krogstie@nmbu.no"
"""

nameDB = [
    ['Tore', 'Hansen'], 
    ['Silje', 'Olavsen'], 
    ['Aase', 'Lund'], 
    ['Jens Petter', 'Oremo'],
    ['Tina', 'Kittelsen'],
    ['Dag', 'Paulsen'],
    ['Lena', 'Nilsen'],
    ['Karsten', 'Woll'],
    ['Ine', 'Ørstad'],
    ['Ravn', 'Havnås'],
    ['Jesper', 'Danberg']]


def name_check(first, family):
        if first[0] == "T":
            return True
        elif len(family) > 6:
            return True
        elif [first, family] == ['Ravn', 'Havnås']:
            return True
        else:
            return False

for i in range(0, len(nameDB)):
    if name_check(nameDB[i][0], nameDB[i][1]):
        print(f"{(i + 1)} {nameDB[i][0]} {nameDB[i][1]}")
    

 