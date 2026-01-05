#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 10:30:15 2022

__author__ = "Simen Roko Krogstie"
__email__ = "simen.roko.krogstie@nmbu.no"
"""

exclude_chars = [
    ' ', '\n', ',', '.', '-', '–', '—', '*', '(', ')',
    '«', '»', ':', ';', '’', '?', "'", '"', '/', '!', '…',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


with open('norec_corpus.txt', 'r', encoding='utf-8') as infile:
    tekst = infile.readlines()
    
    bokstaver = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 
                'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 
                'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 
                'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0, "æ": 0, "ø": 0, 
                "å": 0, "é": 0}

    for lines in tekst:
       for words in lines:
            for letters in words:
                if  letters not in exclude_chars:
                    bokstaver[letters.lower()] += 1
 
    
def order_by(tup):
    liste = [(k, v) for k, v in tup.items()]
    sortert = sorted(liste, key=lambda t: t[1], reverse = True)
    
    ant_bokstaver = sum(bokstaver.values())
    #print(f"Antall bokstaver: {ant_bokstaver}")
    
    freq = []
    freq.append(f"Antall bokstaver: {ant_bokstaver}")
    for i in range(0, len(sortert)):
        freq.append(f"{sortert[i][0].upper()} {(sortert[i][1]/ant_bokstaver * 100):.2f} %")
    return freq
    
liste_frekvens = order_by(bokstaver)
for idx in liste_frekvens:
    print(idx)








