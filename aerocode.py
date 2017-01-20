#!/usr/bin/env python

import os
import sys
import argparse
import re

# handle input arguments neatly
parser = argparse.ArgumentParser()
parser.add_argument('nc', type=str, help='Path to input GCode')
parser.add_argument('-o', type=str, default=None, help='Path to output GCode')
parser.add_argument('-x0', type=float, default=0.0, help="New x origin")
parser.add_argument('-y0', type=float, default=0.0, help="New y origin")
parser.add_argument('-x', type=float, default=0.0, help="Initial x position (after origin change)")
parser.add_argument('-y', type=float, default=0.0, help="Initial y origin (after origin change)")
args = parser.parse_args()


def getString(cmd, x, y):
    return "{0:s} X{1:-.4f} Y{2:-.4f} A{1:-.4f} B{2:-.4f}\r\n".format(cmd, x - args.x0, y - args.y0)

# start output stringlist
x = args.x
y = args.y
output = ["%\r\n", "G20\r\n"]
output.append(getString("G92", x + args.x0, y + args.y0))

# convert file into coordinates
with open(args.nc, "r") as infile:
    line = infile.readline()
    while (line):
        # find x or y coordinates
        newcoord = False
        xstr = re.findall("X[0-9\.-]+", line)
        if xstr:
            x = float(xstr[0][1:])
            newcoord = True
        ystr = re.findall("Y[0-9\.-]+", line)
        if ystr:
            y = float(ystr[0][1:])
            newcoord = True

        # add a new line to output if coordinates changed
        if newcoord and not re.findall("G0 ", line):
            output.append(getString("G01", x, y))
        line = infile.readline()

# write output
filename = args.o
if not filename:
    filename = args.nc + ".txt"
with open(filename, "w") as outfile:
    for line in output:
        outfile.write(line)
