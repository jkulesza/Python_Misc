import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import sys

import pylab
from pylab import arange,pi,sin,cos,sqrt

# Advanced Plot Setup
colors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00']
fig_width     = 6.5
golden_ratio  = (sqrt(5)-1.0)/2.0
fig_height    = fig_width*golden_ratio
fig_size      =  [fig_width,fig_height]
fig_font_size = 22

params        = { 'axes.labelsize' : 14,
                  'axes.titlesize' : 14,
                  'backend'        : 'ps',
                  'font.family'    : 'serif',
                  'font.size'      : fig_font_size,
                  'legend.fontsize': fig_font_size / 2,
                  'figure.dpi'     : 150,
                  'figure.figsize' : fig_size,
                  'savefig.dpi'    : 200,
                  'savefig.bbox'   : 'tight',
                  'font.size'      : fig_font_size,
#                  'text.usetex'    : True,
                  'xtick.labelsize': fig_font_size / 2,
                  'ytick.labelsize': fig_font_size / 2,
}

pylab.rcParams.update(params)

################################################################################

def read_printpts(infilename):
    printpts = ''
    with open(infilename) as infile:
        for line in infile:
            printpts += line

    # Remove header lines.
    printpts = printpts.split('\n')[5:]

    # Split into x, y, e lists.
    printpts = filter(None, [i.split() for i in printpts])

    x = np.array([float(i[0]) for i in printpts])
    y = np.array([float(i[1]) for i in printpts])
    e = np.array([float(i[2]) for i in printpts])

    return x, y, e

################################################################################

infiles = ['m108', 'm109', 'm110']

numdens = {
    'm108' : 8.55527E-02,
    'm109' : 4.98948E-05,
    'm110' : 1.07376E-01
}

for f in infiles:
  
    x, y, e = read_printpts(f)

    y = np.reciprocal(np.multiply(y, numdens[f]))
    
    fig = plt.figure()
    ax = plt.gca()
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Neutron Energy [MeV]')
    ax.set_ylabel('Mean Free Path [cm]')
    plt.axhline(y=1, color='#000000', linestyle='--', linewidth=0.5)
    plt.axvline(x=1, color='#000000', linestyle='--', linewidth=0.5)
    plt.plot(x, y, color='#000000', marker='', linestyle='-', linewidth=0.5)
    plt.savefig(f + '.png')
  
