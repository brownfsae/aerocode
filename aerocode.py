#!/usr/bin/env python

import os
import sys
import argparse


def findkey(lines, line):
    codekey = lines[line].find('G')
    if codekey == -1:
        codekey = findkey(lines, line + 1)
    return codekey


def openfile(filename):
    print 'Opening ', filename
    ocode = open(filename, 'r')
    lines = ocode.readlines()
    codekey = findkey(lines, 0)
    coords = []
    for line in lines:
        if line[codekey:codekey + 2] == 'G0':
            line = line[0:codekey - 1] + line[codekey + 3:]
            coords.append(line[0:len(line) - 1])
        elif line[codekey:codekey + 1] == 'X' or line[codekey:codekey + 1] == 'Y':
            coords.append(line[0:-1])
    ocode.close()
    return(coords)


def double(coords, neworigin):
    xp = '0.00000'
    yp = '0.00000'
    for i in range(len(coords)):
        line = coords[i]
        xi = line.find('X')
        yi = line.find('Y')
        ii = line.find('I')
        ji = line.find('J')
        if ii > -1 or ji > -1:
            print "Warning: Invalid arc found on line {0}. Converted to line".format(i)
            line_trunc = 0
            if ii == -1:
                line_trunc = -(len(line) - ji)
            elif ji == -1:
                line_trunc = -(len(line) - ii)
            elif ii < ji:
                line_trunc = -(len(line) - ii)
            else:
                line_trunc = -(len(line) - ji)
            line = line[:line_trunc]
        beg = 0
        if xi != -1:
            beg = xi
            if yi != -1:
                x = line[xi + 1:yi - 1]
                y = line[yi + 1:]
            else:
                x = line[xi + 1:]
                y = yp
        else:
            beg = yi
            if yi != -1:
                y = line[yi + 1:]
                x = xp
        line = line[0:beg] + 'G01' + ' X' + str(float(x) - neworigin[0]) + \
            ' Y' + str(float(y) - neworigin[1]) + ' A' + str(
                float(x) - neworigin[0]) + ' B' + str(float(y) - neworigin[1])
        xp = x
        yp = y
        coords[i] = line
    return coords


def writefile(coords, filename):
    output = open(filename + '.txt', 'w')
    output.write('%\n')
    output.write('N00000 G92 G70 X0 Y0 A0 B0\n')
    for line in coords:
        output.write(line + '\n')
    output.write('N99999 M02')
    output.close()

if __name__ == '__main__':
    print len(sys.argv)
    if len(sys.argv) <= 1:
        print "Not enough arguments given!"
        sys.exit(1)
    if len(sys.argv) == 4:
        x = float(sys.argv[2])
        y = float(sys.argv[3])
    else:
        x = 0
        y = 0
    filename = sys.argv[1]
    coords = openfile(filename)
    coords = double(coords, [x, y])
    writefile(coords, filename)
