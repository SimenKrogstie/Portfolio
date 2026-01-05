#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Created on Fri Sep 16 09:13:18 2022"""

__author__ = "Simen Roko Krogstie"
__email__ = "simen.roko.krogstie@nmbu.no"

# a) Svaret er

innsamling_hist = [[2015, 86343, 123], [2016, 93512, 125], 
                   [2017, 83935, 119], [2018, 91274, 128], 
                   [2019, 88935, 127], [2020, 95182, 132]]



for i, element in enumerate(innsamling_hist):
    res = element[1]/element[2]
    gjennomsnitt_innsamlet = (f"({element[0]}:, {res:.2F} kr/per bøssebærer \n")
    print(gjennomsnitt_innsamlet)
    

# b) Det ble samlet inn mest penger pr. bøssebærer i 2016.



    
    
    
    

    

    
    
    
    