# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 14:44:51 2023

@author: kueht

for atom_type full only
"""

zlo = 20.85320015736807
zhi = 39.14679984263382
box_height = zhi-zlo

import numpy as np

with open('tip4p.data','r') as file:
    lines = []
    for line in file:
        line = line.strip()
        lines.append(line)
   
head = lines.index("Atoms # full")
foot = lines.index('Velocities')

head_list = lines[:head+2]
atom_list = lines[head+2:foot-1]
foot_list = lines[foot-1:]

new_list = []
for line in atom_list:
    line2 = []
    for item in line.split(' '):
        try:
            line2.append(int(item))
        except:
            line2.append(float(item))
    new_list.append(line2)

for line in new_list:
    line[7:] = [0,0,0]

'''
distance between O-H: 0.9572
if O at top or btm 0.9572
O: type 1 list[i][2]=1 , 
molecule: list[i][1]=K
z: list[i][6]
'''

'''
get the molecule numbers of oxygen atoms close to the top and bottom boundaries
'''
mol_num_up=[]
mol_num_down=[]

for atom in new_list:
    if atom[2] == 1:
        if atom[6] <= zlo + 0.9572:
            mol_num_down.append(atom[1])
        if atom[6] >= zhi - 0.9572:
            mol_num_up.append(atom[1])

'''
if the Hydrogen atoms are bonded to the oxygen atoms (that close to the z-boundary)
and they are at the opposite sites in z-direction, move these hydrogen atoms either upward/downward
'''

number=0
for atom in new_list:
    if (mol_num_down.count(atom[1]) >0 and atom[2]==2 and atom[6]>= zlo + box_height/2):
        new_list[number][6] -= box_height
    number += 1

number=0
for atom in new_list:
    if (mol_num_up.count(atom[1]) >0 and atom[2]==2 and atom[6]<= zlo + box_height/2):
        new_list[number][6] += box_height
    number += 1

'''
put the periodic flag to zero
'''


with open('tip4p_updated.data','w') as newfile:
    for line in head_list:
        newfile.write(f"{line}\n")
    for line in new_list:
        for item in line:
            newfile.write(str(item) +'\t')
        newfile.write('\n')
    for line in foot_list:
        newfile.write(f"{line}\n")
        