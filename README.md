# aerocody.py
aerocode.py is a post-processor for GCode.  It takes a gcode file listing X and Y coordinates and writes an output file listing X, Y, A, and B coordinates.  This script is useful for getting generic GCode from HSMWorks into a format compatible with the CNC hot wire foam cutter in the Brown Design Workshop.  For the wire cutter, X/Y are one tower's axis and A/B are the other tower, so you have to dubplicate all the X/Y coordinates into the A/B coordinates for it to know what to do.

Basically, open a terminal window with python installed and run "python aerocode.py [original GCode]".  It will output a file with the same name as the original, but with ".txt" appended.  This file is in theory good to go.

However, since often times what you design in Solidworks is not set up for the foam cutter (e.g.: the origin is in the wrong place) aerocode has a couple built-in features:

-o [output filename] allows you to specify a different output filename

-x0 and -y0 allow you to move the origin to a new point

-x and -y change the initial x and y position (i.e., the position the machine should think the wire is at at the beginning of the cut)

Contact philip.eng.mathieu@gmail.com with questions.
