#!/usr/bin/python
from matplotlib.ticker import FuncFormatter, LogLocator
from matplotlib import cm, colors, ticker, rc
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pylab
import re
import sys
from scipy.stats import pearsonr

from cmap_parula import *

from matplotlib.mlab import bivariate_normal

# Set plot aspect ratio to 'the golden ratio.'
fig_width     = 6.5
golden_ratio  = (np.sqrt(5)-1.0)/2.0
fig_height    = fig_width*golden_ratio
fig_size      =  [fig_width,fig_height]
fig_font_size = 10

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

params        = { 'axes.labelsize' : 10,
                  'axes.titlesize' : 10,
                  'backend'        : 'ps',
                  'font.family'    : 'serif',
                  'font.size'      : fig_font_size,
                  'legend.fontsize': fig_font_size,
                  'figure.dpi'     : 150,
                  'figure.figsize' : fig_size,
                  'savefig.dpi'    : 600,
                  'savefig.bbox'   : 'tight',
                  'text.usetex'    : True,
                  'xtick.labelsize': fig_font_size,
                  'ytick.labelsize': fig_font_size,
}

pylab.rcParams.update(params)

################################################################################

def extract_tracks(infile):
    h = []
    t = []
    s = []
    for i in infile.split('\n'):
        if('Processed' in i):
            h.append(int(re.search(r'History (\d+),', i).group(1)))
            t.append(int(re.search(r'(\d+) track', i).group(1)))
            s.append(float(re.search(r'unnormalized tally value\s+(.*?)$', i).group(1)))

    return(np.array(h), np.array(t), np.array(s))

def plot_histogram(x, outfilename, nbins=100, logX=True, logY=True, xlabel=None, ylabel=None, title=None):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    if(logX):
        xbins = np.logspace(np.log10(np.min(x[np.nonzero(x)])), np.log10(max(x)), nbins)
        plt.xscale('log')
    else:
        xbins = np.linspace(np.min(x), np.log10(max(x)), nbins)

    if(logY):
        plt.yscale('log')
        plt.setp(ax.get_yticklabels()[1], visible=False)

    n, bins, patches = plt.hist(x,
                                bins = xbins,
                                facecolor = 'black',
                                edgecolor = 'none',
                                alpha = 0.25,
                                histtype = 'stepfilled',
                                log = logY)
    print(outfilename)
    print(n)

    ax.grid(which='both', linestyle='-', color='#CCCCCC')
    ax.set_axisbelow(True)

    # Add line for the mean value of the distribution.
    xmean = np.mean(x)
    plt.axvline(xmean, color='k', linestyle='--', linewidth=0.5)

    ymin, ymax = ax.get_ylim()
    plt.text(0.95*xmean, 0.95*ymax,
        'Mean = ' + '{0:.2e}'.format(xmean),
        verticalalignment = 'top',
        horizontalalignment = 'right',
        rotation='vertical')

    if(title != None):
        plt.title(title)
    if(xlabel != None):
        plt.xlabel(xlabel)
    if(ylabel != None):
        plt.ylabel(ylabel)

    plt.savefig(outfilename + '_histogram.png', dpi=300)

def plot_histogram2d(x, y, outfilename, nbins=100, logX=True, logY=True, logZ=True, xlabel=None, ylabel=None, title=None, display_2d_axes = True):
    fig = plt.figure()

#   0 1 2    X X X
#   3 4 5 ->   X
    gs = mpl.gridspec.GridSpec(2, 3, height_ratios=[10, 1], width_ratios=[1, 10, 1], wspace=0.1)
    gs = mpl.gridspec.GridSpec(2, 3, height_ratios=[1, 1], width_ratios=[1, 1, 0.1], wspace=0.1)

    ########################################
    # Score Histogram
    ########################################
    ax = plt.subplot(gs[0])
    if(logY):
        ybins = np.logspace(np.log10(np.min(s[np.nonzero(s)])), np.log10(max(s)), nbins)
        plt.yscale('log')
    else:
        ybins = np.linspace(0.0, max(s), nbins)
        def ytickformatter(x, pos):
            return '%.1e' % (x)
        ax.yaxis.set_major_formatter(FuncFormatter(ytickformatter))

    if(logZ):
        plt.xscale('log')
        plt.setp(ax.get_xticklabels()[1], visible=False)

    n, bins, patches = ax.hist(y,
                               bins = ybins,
                               facecolor = 'black',
                               edgecolor = 'none',
                               alpha = 0.25,
                               histtype = 'stepfilled',
                               orientation = 'horizontal',
                               log = logZ)

    ax.set_axisbelow(True)
#   plt.axis('off')

    # Add line for the mean value of the distribution.
    ymean = np.mean(y)
    plt.axhline(ymean, color='k', linestyle='--', linewidth=0.5)

    print(np.sum(n))

    ########################################
    # Track Histogram
    ########################################
    ax = plt.subplot(gs[4])
    if(logX):
        xbins = np.logspace(np.log10(np.min(x[np.nonzero(x)])), np.log10(max(x)), nbins)
        plt.xscale('log')
    else:
        xbins = np.linspace(0.0, max(x), nbins)
        def xtickformatter(x, pos):
            return '%.1e' % (x)
        ax.xaxis.set_major_formatter(FuncFormatter(xtickformatter))
        plt.xticks(rotation=90)
    if(logZ):
        plt.yscale('log')
        plt.setp(ax.get_yticklabels()[1], visible=False)

    n, bins, patches = ax.hist(x,
                               bins = xbins,
                               facecolor = 'black',
                               edgecolor = 'none',
                               alpha = 0.25,
                               histtype = 'stepfilled',
                               log = logZ)

    ax.set_axisbelow(True)
#   plt.axis('off')

    # Add line for the mean value of the distribution.
    xmean = np.mean(x)
    plt.axvline(xmean, color='k', linestyle='--', linewidth=0.5)

    print(np.sum(n))

    ########################################
    # 2D Histogram
    ########################################
    ax = plt.subplot(gs[1])
    if(logX):
        xbins = np.logspace(np.log10(np.min(x[np.nonzero(x)])), np.log10(max(x)), nbins)
        plt.xscale('log')
    else:
        xbins = np.linspace(0.0, max(x), nbins)
    if(logY):
        ybins = np.logspace(np.log10(np.min(y[np.nonzero(y)])), np.log10(max(y)), nbins)
        plt.yscale('log')
    else:
        ybins = np.linspace(0.0, max(y), nbins)

    H, x, y = np.histogram2d(x, y, bins=[xbins, ybins])
    H = np.ma.masked_where(H==0, H)

    X, Y = np.meshgrid(x, y)

    parula = def_parula()
    parula = mpl.colors.ListedColormap(name='parula', colors=np.divide(parula, 255.), N=len(parula))
    cm.register_cmap(cmap=parula)
    if(logZ):
        plt.pcolormesh(X, Y, H.T, cmap='parula', norm=colors.LogNorm())
    else:
        plt.pcolormesh(X, Y, H.T, cmap='parula')

    if(not display_2d_axes):
        plt.axis('off')

    plt.axhline(ymean, color='k', linestyle='--', linewidth=0.5)
    plt.axvline(xmean, color='k', linestyle='--', linewidth=0.5)

    ax.xaxis.set_major_formatter(plt.NullFormatter())
    ax.yaxis.set_major_formatter(plt.NullFormatter())

    cbax = plt.subplot(gs[2])
    cb = plt.colorbar(ticks=LogLocator(subs=range(10)), cax=cbax)

    if(title != None):
        fig.suptitle(title)
    if(xlabel != None):
        if(logX):
            fig.text(0.67, 0.02, xlabel, ha='center')
        else:
            fig.text(0.67,-0.08, xlabel, ha='center')
    if(ylabel != None):
        fig.text(0.02, 0.72, ylabel, va='center', rotation='vertical')

    plt.savefig(outfilename + '_histogram2d.png', dpi=300)

    print(np.sum(H))


# EXECUTE PROGRAM ##############################################################

if __name__ == "__main__":

    try:
        infilename = sys.argv[1]
    except:
        print("Error: No MCNP outp file defined in ARGV")
        exit()

    with open (infilename, "r") as myfile:
        outp = myfile.read()

    h, t, s = extract_tracks(outp)

    nonzero_score_tracks = t[np.nonzero(s)]
    nonzero_scores = s[np.nonzero(s)]

    zero_score_tracks = t[np.where(s == 0)[0]]

    plot_histogram(t, infilename + '_tracks',
                    title = 'Track Distribution (All Scores, ' + str(len(t)) + ' Total)',
                    xlabel = 'Number of Tracks For A Given History',
                    ylabel = 'Absolute Frequency')

    plot_histogram(nonzero_score_tracks, infilename + '_nonzero_score_tracks',
                    title = 'Track Distribution (Non-Zero Scores, ' + str(len(nonzero_score_tracks)) + ' Total)',
                    xlabel = 'Number of Tracks For A Given History',
                    ylabel = 'Absolute Frequency')

    plot_histogram(zero_score_tracks, infilename + '_zero_score_tracks',
                    title = 'Track Distribution (Zero Scores, ' + str(len(zero_score_tracks)) + ' Total)',
                    xlabel = 'Number of Tracks For A Given History',
                    ylabel = 'Absolute Frequency')

    plot_histogram(s, infilename + '_scores',
                    title = 'Score Distribution (' + str(len(nonzero_score_tracks)) + ' Non-Zero)',
                    xlabel = 'Score for a Given History',
                    ylabel = 'Absolute Frequency')

    pcc, ttpv = pearsonr(nonzero_scores,nonzero_score_tracks)

    print(pcc)

    plot_histogram2d(nonzero_score_tracks, nonzero_scores, infilename + '_non-zero_histories',
                    title = 'Score-Track Bivariate Distribution (' + str(len(nonzero_score_tracks)) + ' Non-Zero Histories)\nPearson Correlation Coefficient: ' + '{0:.3e}'.format(pcc) + '',
                    xlabel = 'Number of Tracks For a Given History',
                    ylabel = 'Score for a Given History'
                    )

    pcc, ttpv = pearsonr(s, t)

    print(pcc)

    plot_histogram2d(t, s, infilename + '_all_histories_log',
                    title = 'Score-Track Bivariate Distribution (' + str(len(t)) + ' Histories)\nPearson Correlation Coefficient: ' + '{0:.3e}'.format(pcc) + '',
                    xlabel = 'Number of Tracks For a Given History',
                    ylabel = 'Score for a Given History',
                    )

    plot_histogram2d(t, s, infilename + '_all_histories_lin',
                    title = 'Score-Track Bivariate Distribution (' + str(len(t)) + ' Histories)\nPearson Correlation Coefficient: ' + '{0:.3e}'.format(pcc) + '',
                    xlabel = 'Number of Tracks For a Given History',
                    ylabel = 'Score for a Given History',
                    logX = False, logY = False, display_2d_axes = False
                    )

    plot_histogram2d(t, s, infilename + '_all_histories_linlog',
                    title = 'Score-Track Bivariate Distribution (' + str(len(t)) + ' Histories)\nPearson Correlation Coefficient: ' + '{0:.3e}'.format(pcc) + '',
                    xlabel = 'Number of Tracks For a Given History',
                    ylabel = 'Score for a Given History',
                    logX = True, logY = False, display_2d_axes = False
                    )
  
