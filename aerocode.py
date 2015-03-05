#!/usr/bin/env python

import os
import sys
import argparse

def findkey(lines,line):
    codekey = lines[line].find('G')
    if codekey == -1:
        codekey = findkey(lines,line + 1)
    return codekey


def openfile(filename):
    print 'Opening ', filename
    ocode = open(filename,'r')
    lines = ocode.readlines()
    codekey = findkey(lines,0)
    coords = []
    for line in lines:
        if line[codekey:codekey+2] == 'G0':
            line = line[0:codekey-1] + line[codekey+3:]
            coords.append(line[0:len(line)-1])
        elif line[codekey:codekey+1] == 'X' or line[codekey:codekey+1] == 'Y':
            coords.append(line[0:len(line)-1])
    ocode.close()
    return(coords)

def double(coords):
    xp = '0.00000'
    yp = '0.00000'
    for i in range(0,len(coords)):
        line = coords[i]
        xi = line.find('X')
        yi = line.find('Y')
        beg = 0
        if xi != -1:
            beg = xi
            if yi != -1:
                x = line[xi+1:yi-1]
                y = line[yi+1:]
            else:
                x = line[xi+1:]
                y = yp
        else:
            beg = yi
            if yi != -1:
                y = line[yi+1:]
                x = xp
        line = line[0:beg] + 'G01' + ' X' + x + ' Y' + y + ' A' + x + ' B' + y
        xp = x
        yp = y
        coords[i] = line
    return coords
 
def writefile(coords,filename):
    output = open(filename + '.txt','w')
    output.write('%\n')
    output.write('N00000 G92 G70 X0 Y0 A0 B0\n')
    for line in coords:
        output.write(line + '\n')
    output.write('N99999 M02')
    output.close()

if __name__ == '__main__':
    for filename in sys.argv:
        coords = openfile(filename)
        coords = double(coords)
        writefile(coords,filename)