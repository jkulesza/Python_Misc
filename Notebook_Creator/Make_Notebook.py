#!/usr/bin/python
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Joel A. Kulesza
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

def Make_Notebook(twoSided = True, keepHolePunchMargin = False, showHolePunchMarks = False,
                    showDots = True, showRoundDots = False, showGrid = False,
                    showDate = True, showName = True, showMarginInfo = False,
                    showMarginFortune = False, showPageNumber = True,
                    textName = "Your Name", textMarginInfo = '',
                    pageFirst = 1, pageTotal = 1):

    from pyx import *
    import numpy as np
    import subprocess
    import re
    import datetime

    # PAGE ELEMENT SIZING VALUES ###################################################

    PageScalingFactor = 2.5315
    PSF = PageScalingFactor

    pageX = 8.5
    pageY = 11

    holePunchDiameter = 0.28125
    holePunchX = 0.546875
    holePunchY = [1.0625, 5.6875, 9.53125]

    graphZeroX  =  0.75
    graphZeroY  =  0.30
    graphWidth  =  7.4
    graphHeight = 10.2
    graphDPI = 5

    if(not keepHolePunchMargin):
        graphWidth  =  graphWidth + (graphZeroX - (pageX - graphWidth - graphZeroX))
        graphZeroX = (pageX - graphWidth) / 2.

    if(twoSided):
        graphZeroXOdd  = graphZeroX
        graphZeroXEven = pageX - graphWidth - graphZeroX
        holePunchXOdd  = holePunchX
        holePunchXEven = pageX - holePunchX

    linewidthBorder  = 0.03
    diameterDot      = 0.014
    linewidthGrid    = 0.014

    colorHolePunchRed   = 0.50
    colorHolePunchGreen = 0.50
    colorHolePunchBlue  = 0.50

    colorBorderRed   = 0.85
    colorBorderGreen = 0.85
    colorBorderBlue  = 0.85

    colorDotRed      = 0.50
    colorDotGreen    = 0.50
    colorDotBlue     = 0.50

    colorGridRed     = 0.985
    colorGridGreen   = 0.985
    colorGridBlue    = 0.985

    # --- Show Date

    textDate = "Date: "
    fontsizeDate = text.size.normalsize # or .normalsize (larger) or .footnotesize (smaller)
    offsetDateX =  0.050
    offsetDateY =  0.050

    colorDateRed   = 0.0
    colorDateGreen = 0.0
    colorDateBlue  = 0.0

    # --- Show Name

    fontsizeName = text.size.normalsize # or .normalsize (larger) or .footnotesize (smaller)
    offsetNameX = -0.050
    offsetNameY =  0.050

    colorNameRed   = 0.0
    colorNameGreen = 0.0
    colorNameBlue  = 0.0

    # --- Show Margin Info

    textMarginInfo = ""
    fontsizeMarginInfo = text.size.normalsize # or .normalsize (larger) or .footnotesize (smaller)
    offsetMarginInfoX =  0.050
    offsetMarginInfoY = -0.050

    if(twoSided):
        offsetMarginInfoXOdd  =  offsetMarginInfoX
        offsetMarginInfoXEven = -offsetMarginInfoX

    colorMarginInfoRed   = 0.0
    colorMarginInfoGreen = 0.0
    colorMarginInfoBlue  = 0.0

    # --- Show Page Number

    fontsizePageNumber= text.size.small # or .normalsize (larger) or .footnotesize (smaller)

    colorPageNumberRed   = 0.0
    colorPageNumberGreen = 0.0
    colorPageNumberBlue  = 0.0

    ################################################################################

    pages = []

    text.set(mode="latex")
    text.preamble(r"\usepackage{color}")
    text.preamble(r"\definecolor{colorPageNumber}{rgb}{%g,%g,%g}"
                  % (colorPageNumberRed, colorPageNumberGreen, colorPageNumberBlue))
    text.preamble(r"\definecolor{colorDate}{rgb}{%g,%g,%g}"
                  % (colorDateRed, colorDateGreen, colorDateBlue))
    text.preamble(r"\definecolor{colorName}{rgb}{%g,%g,%g}"
                  % (colorNameRed, colorNameGreen, colorNameBlue))
    text.preamble(r"\definecolor{colorMarginInfo}{rgb}{%g,%g,%g}"
                  % (colorMarginInfoRed, colorMarginInfoGreen, colorMarginInfoBlue))

    for i in range(pageFirst,pageFirst+pageTotal):
        if(twoSided):
            if(i % 2 != 0):
                graphZeroX = graphZeroXOdd
                holePunchX = holePunchXOdd
                offsetMarginInfoX = offsetMarginInfoXOdd
            else:
                graphZeroX = graphZeroXEven
                holePunchX = holePunchXEven
                offsetMarginInfoX = offsetMarginInfoXEven

        if(showMarginFortune):
            textMarginInfo = re.sub("\r", " ", subprocess.check_output(['fortune','-s']))
            print("OLD:" + textMarginInfo)
            textMarginInfo = re.sub("\n", " ", textMarginInfo)
            textMarginInfo = re.sub(r"\\", r"\\textbackslash ", textMarginInfo)
            textMarginInfo = re.sub(r"\"(.*?)\"", r"``\1''", textMarginInfo)
            textMarginInfo = re.sub("_", "\\_", textMarginInfo)
            textMarginInfo = re.sub("\<", r"\\textless ", textMarginInfo)
            textMarginInfo = re.sub("\>", r"\\textgreater ", textMarginInfo)
            textMarginInfo = re.sub("\%", "\\%", textMarginInfo)
            textMarginInfo = re.sub("\$", "\\$", textMarginInfo)
            textMarginInfo = re.sub("\{", "\\{", textMarginInfo)
            textMarginInfo = re.sub("\}", "\\}", textMarginInfo)
            textMarginInfo = re.sub("\|", r"\\textbar ", textMarginInfo)
            textMarginInfo = re.sub("\#", "\\#", textMarginInfo)
            textMarginInfo = re.sub("\&", "\\&", textMarginInfo)
            print("NEW: " + textMarginInfo)
            fontsizeMarginInfo = text.size.small # or .normalsize (larger) or .footnotesize (smaller)

        print("Operating on Page " + str(i))
        c = canvas.canvas()

        # Size page.
        c.stroke(path.rect(0, 0, pageX*PSF, pageY*PSF),
                 [color.rgb.white])

        # Draw hole punch markers.
        if(showHolePunchMarks):
            for y in holePunchY:
                c.stroke(path.circle(holePunchX*PSF,y*PSF,holePunchDiameter),
                         [style.linestyle.dotted, color.rgb(colorHolePunchRed,colorHolePunchGreen,colorHolePunchBlue)])

        # Draw line grid.
        if(showGrid):
            for x in np.linspace(graphZeroX,graphZeroX+graphWidth,(graphWidth*graphDPI)):
                c.stroke(path.line(x*PSF, graphZeroY*PSF, x*PSF, (graphZeroY+graphHeight)*PSF),
                         [color.rgb(colorGridRed,colorGridGreen,colorGridBlue)])
            for y in np.linspace(graphZeroY,graphZeroY+graphHeight,(graphHeight*graphDPI)):
                c.stroke(path.line(graphZeroX*PSF, y*PSF, (graphZeroX+graphWidth)*PSF, y*PSF),
                         [color.rgb(colorGridRed,colorGridGreen,colorGridBlue)])

        # Draw dot grid.
        if(showDots):
            if(showRoundDots):
                for x in np.linspace(graphZeroX,graphZeroX+graphWidth,(graphWidth*graphDPI)):
                    for y in np.linspace(graphZeroY,graphZeroY+graphHeight,(graphHeight*graphDPI)):
                        c.fill(path.circle(x*PSF,y*PSF,diameterDot),
                               [color.rgb(colorDotRed,colorDotGreen,colorDotBlue)])
            else:
                for x in np.linspace(graphZeroX,graphZeroX+graphWidth,(graphWidth*graphDPI)):
                    for y in np.linspace(graphZeroY,graphZeroY+graphHeight,(graphHeight*graphDPI)):
                        c.fill(path.rect(x*PSF-diameterDot/2,y*PSF-diameterDot/2,diameterDot,diameterDot),
                               [color.rgb(colorDotRed,colorDotGreen,colorDotBlue)])

        # Draw bounding box.
        c.stroke(path.rect(graphZeroX*PSF, graphZeroY*PSF, graphWidth*PSF, graphHeight*PSF),
                 [color.rgb(colorBorderRed,colorBorderGreen,colorBorderBlue),
                 style.linewidth(linewidthBorder)])

        # Draw date field in upper left.
        if(showDate):
            c.text((graphZeroX+offsetDateX)*PSF,(graphZeroY+graphHeight+offsetDateY)*PSF,
                   r"\textcolor{colorDate}{" + textDate + "}",
                   [fontsizeDate])

        # Draw author name in the upper right.
        if(showName):
            c.text((graphZeroX+graphWidth+offsetNameX)*PSF,(graphZeroY+graphHeight+offsetNameY)*PSF,
                   r"\textcolor{colorName}{" + textName + "}",
                   [text.halign.boxright,fontsizeName])

        # Draw supplemental text down the right margin from the upper right or alternate & reverse directio for two-sided pages.
        if(showMarginInfo):
            if(twoSided):
                if(i % 2 != 0):
                    c.text((graphZeroX+graphWidth+offsetMarginInfoX)*PSF,(graphZeroY+graphHeight+offsetMarginInfoY)*PSF,
                           r"\textcolor{colorMarginInfo}{" + textMarginInfo + "}",
                           [fontsizeMarginInfo,trafo.rotate(-90)])
                else:
                    c.text((graphZeroX+offsetMarginInfoX)*PSF,(graphZeroY+graphHeight+offsetMarginInfoY)*PSF,
                           r"\textcolor{colorMarginInfo}{" + textMarginInfo + "}",
                           [text.halign.boxright,fontsizeMarginInfo,trafo.rotate(90)])

        # Draw the page number in the lower right.
        if(showPageNumber):
            if(twoSided):
                if(i % 2 != 0):
                    c.text((graphZeroX+graphWidth)*PSF,(graphZeroY/2)*PSF,
                           r"\textcolor{colorPageNumber}{"+str(i)+"}",
                           [text.halign.boxright,fontsizePageNumber])
                else:
                    c.text((graphZeroX)*PSF,(graphZeroY/2)*PSF,
                           r"\textcolor{colorPageNumber}{"+str(i)+"}",
                           [text.halign.boxleft,fontsizePageNumber])
            else:
                c.text((graphZeroX+graphWidth)*PSF,(graphZeroY/2)*PSF,
                       r"\textcolor{colorPageNumber}{"+str(i)+"}",
                       [text.halign.boxright,fontsizePageNumber])

        # Create the page from the canvas.
        p = document.page(c)

        # Add the page to the array of pages.
        pages.append(p)

    # Compile the document together from the array of pages.
    d = document.document(pages)

    # Create a PDF of the document.
    d.writePDFfile("Notebook_Pages_" + datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d_") + str(pageFirst) + "-" + str(pageFirst + pageTotal - 1) + ".pdf")

################################################################################
# Command line options.
################################################################################
import __main__ as main
if(__name__ == '__main__' and hasattr(main, '__file__')):
    import textwrap, argparse
    description = textwrap.dedent(
    """
    This script creates a series of pages suitable for printing and using as 
    notepaper within a notebook.
    """)
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--pages', '-p',
                        type = int,
                        default = 1,
                        help = 'how many pages to generate (default 1)')
    parser.add_argument('--start', '-s',
                        type = int,
                        default = 1,
                        help = 'starting page number (default 1)')
    parser.add_argument('--two_sided',
                        action = 'store_true', 
                        default = False,
                        dest = 'two_sided',
                        help = 'generate two sided pages (default false)')
    parser.add_argument('--hole_punch',
                        action = 'store_true', 
                        default = False,
                        help = 'create a margin to allow hole punches (default false)')
    parser.add_argument('--show_hole_punch_marks',
                        action = 'store_true', 
                        default = False,
                        help = 'show representative hole punch marks (default false)')
    parser.add_argument('--show_dots',
                        action = 'store_true', 
                        default = True,
                        help = 'show dot grid (default true)')
    parser.add_argument('--show_round_dots',
                        action = 'store_true', 
                        default = False,
                        help = 'show round dots --- more memory needed (default false)')
    parser.add_argument('--show_grid',
                        action = 'store_true', 
                        default = False,
                        help = 'show square grid lines (default false)')
    parser.add_argument('--show_date',
                        action = 'store_true', 
                        default = False,
                        help = 'show date field label (default false)')
    parser.add_argument('--show_name',
                        action = 'store_true', 
                        default = False,
                        help = 'show name field (default false)')
    parser.add_argument('--name',
                        default = '',
                        help = 'name text (default "")')
    parser.add_argument('--show_margin_info',
                        action = 'store_true', 
                        default = False,
                        help = 'show margin information (default false)') 
    parser.add_argument('--margin_info',
                        default = '',
                        help = 'margin information (default "")') 
       
    args = parser.parse_args()

    if(args.name != ''): args.show_name = True

    Make_Notebook(twoSided = args.two_sided,
                    pageFirst = args.start,
                    pageTotal = args.pages,
                    keepHolePunchMargin = args.hole_punch,
                    showHolePunchMarks = args.show_hole_punch_marks,
                    showDots = args.show_dots,
                    showRoundDots = args.show_round_dots,
                    showGrid = args.show_grid,
                    showDate = args.show_date,
                    showName = args.show_name,
                    textName = args.name,
                    showMarginInfo = args.show_margin_info,
                    textMarginInfo = args.margin_info)
 
