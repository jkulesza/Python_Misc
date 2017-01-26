#!/usr/bin/env python3

# Configure plotting.
import datetime
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import cm, colors, ticker, rc
from mpl_toolkits import axes_grid1
import numpy as np
import pylab

################################################################################
# Set plot aspect ratio to 'the golden ratio.'
fig_width     = 6.5
golden_ratio  = (np.sqrt(5)-1.0)/2.0
fig_height    = fig_width*golden_ratio
fig_size      = [fig_width,fig_height]
fig_font_size = 10

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

params        = { 'axes.labelsize' : fig_font_size,
                  'axes.titlesize' : fig_font_size,
                  'backend'        : 'ps',
                  'font.family'    : 'serif',
                  'font.size'      : fig_font_size,
                  'legend.fontsize': 0.8*fig_font_size,
                  'figure.dpi'     : 300,
                  'figure.figsize' : fig_size,
                  'savefig.dpi'    : 600,
                  'savefig.bbox'   : 'tight',
                  'text.usetex'    : True,
                  'xtick.labelsize': fig_font_size,
                  'ytick.labelsize': fig_font_size,
}

pylab.rcParams.update(params)

################################################################################
# Conversion constants.
class constants:
    meters2feet = 1 / 0.3048 # Convert meters -> feet
    EarthRad = 3959 # feet

################################################################################
# Smoothing functions.
# See: http://stackoverflow.com/questions/28536191/how-to-filter-smooth-with-scipy-numpy
from scipy.signal import butter, filtfilt

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filtfilt(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

################################################################################
# Import RunKeeper GPX raw data.
def importGPX(infilename):
    import xml.etree.ElementTree
    import dateutil.parser

    tree = xml.etree.ElementTree.parse(infilename)
    trk = []
    for trkpt in tree.findall('.//{http://www.topografix.com/GPX/1/1}trkpt'):
        lat = float(trkpt.attrib['lat'])
        lon = float(trkpt.attrib['lon'])
        ele = float(trkpt.find('.//{http://www.topografix.com/GPX/1/1}ele').text)
        tme = trkpt.find('.//{http://www.topografix.com/GPX/1/1}time').text
        tme = dateutil.parser.parse(tme)
        trk.append({'lat': lat, 'lon': lon, 'ele': ele, 'tme': tme})

    return(trk)

# Calculate distance and average speed based on two GPS coordinates.
def calcSpeedAndDistanceFromGPS(lat1, lon1, lat2, lon2, dt):
    import datetime
    import math
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.sin(dLon/2) * math.sin(dLon/2) * \
        math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    s = constants.EarthRad * c
    ds = s / dt

    return(s, ds)

# Convert raw track data into preferred format.
def processRawTrack(rawtrk):
    import datetime
    import dateutil
    trk = []

    for n,t in enumerate(rawtrk):
        t['ele'] = t['ele'] * constants.meters2feet
        if(n == 0):
            t0 = t['tme']
            t['de'] = 0
            t['dt'] = 0
            t['s']  = 0
            t['ds'] = 0
            t['elap'] = 0
        else:
            dt = t['tme'] - rawtrk[n-1]['tme']
            t['dt'] = dt
            lat1 = rawtrk[n-1]['lat']
            lon1 = rawtrk[n-1]['lon']
            lat2 = t['lat']
            lon2 = t['lon']

            dt = dt.total_seconds() / 3600
            s, ds = calcSpeedAndDistanceFromGPS(lat1, lon1, lat2, lon2, dt)

            t['de'] = t['ele'] - rawtrk[n-1]['ele']
            t['s'] = s
            t['ds'] = ds
            t['elap'] = (t['tme'] - t0).total_seconds()
        trk.append(t)

    return(trk)

# Time tick formatter function.
def timeTicks(x, pos):
    d = datetime.timedelta(seconds=x)
    return str(d)

def plotElevation(trk, smoothed=True,
                    xlabel='Time [h:mm:ss]', ylabel='Elevation [feet]'):
    plt.figure()
    ax = plt.gca()

    x = [t['elap'] for t in trk]
    y = [t['ele'] for t in trk]
    f = butter_lowpass_filtfilt(y, 5000, 50000)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if(smoothed):
        plt.plot(x, f, 'k-', linewidth=0)
    else:
        plt.plot(x, y, 'k.-')

    labels = [i for i in plt.gca().get_yticks()]
    plt.fill_between(x, f, labels[0], color='0.85')

    plt.xticks(np.arange(min(x), max(x)+1, 150.0))

    formatter = matplotlib.ticker.FuncFormatter(timeTicks)
    ax.xaxis.set_major_formatter(formatter)
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)

    return(plt)

def plotSpeed(trk, smoothed=True,
                    xlabel='Time [h:mm:ss]', ylabel='Speed [mph]'):
    plt.figure()
    ax = plt.gca()

    x = [t['elap'] for t in trk]
    y = [t['ds'] for t in trk]
    f = butter_lowpass_filtfilt(y, 5000, 50000)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if(smoothed):
        plt.plot(x, f, 'k-')
    else:
        plt.plot(x, y, 'k.-')

    plt.xticks(np.arange(min(x), max(x)+1, 150.0))
    plt.ylim(ymin=0)

    formatter = matplotlib.ticker.FuncFormatter(timeTicks)
    ax.xaxis.set_major_formatter(formatter)
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)

    return(plt)

def plotSpeedElevation(trk, smoothed=True,
                    xlabel='Time [h:mm:ss]', y1label='Speed [mph]', y2label='Elevation [feet]'):

    plt.figure()
    ax1 = plt.gca()

    x = [t['elap'] for t in trk]
    y1 = [t['ds'] for t in trk]
    f1 = butter_lowpass_filtfilt(y1, 5000, 50000)
    y2 = [t['ele'] for t in trk]
    f2 = butter_lowpass_filtfilt(y2, 5000, 50000)

    plt.xlabel(xlabel)
    plt.ylabel(y1label)

    if(smoothed):
        plt.plot(x, f1, 'k-')
    else:
        plt.plot(x, y1, 'k.-')

    plt.xticks(np.arange(min(x), max(x)+1, 150.0))
    plt.ylim(ymin=0)

    formatter = matplotlib.ticker.FuncFormatter(timeTicks)
    ax1.xaxis.set_major_formatter(formatter)
    for tick in ax1.get_xticklabels():
        tick.set_rotation(45)

    ax2 = ax1.twinx()

    plt.ylabel(y2label)

    if(smoothed):
        plt.plot(x, f2, 'k-', linewidth=0)
    else:
        plt.plot(x, y2, 'k.-')

    labels = [i for i in plt.gca().get_yticks()]
    plt.fill_between(x, f2, labels[0], color='0.85')

    ax1.set_zorder(ax2.get_zorder()+1)
    ax1.patch.set_visible(False)

    return(plt)

def getOSM(xmin, xmax, ymin, ymax):
    import math
    import os
    import shutil
    import urllib.request

    zoom = 17
    def deg2num(lon, lat, zoom):
        lat_rad = math.radians(lat)
        n = 2.0 ** zoom
        xtile = int((lon + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return (xtile, ytile, zoom)
    def num2deg(xtile, ytile, zoom):
        n = 2.0 ** zoom
        lon = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat = math.degrees(lat_rad)
        return (lon, lat)

    x, y, z = deg2num(xmin, ymax, zoom)
    xmin, ymax = num2deg(x, y, z)
    xtmin = x; ytmin = y
    x, y, z = deg2num(xmax, ymin, zoom)
    xmax, ymin = num2deg(x+1, y+1, z)
    xtmax = x+1; ytmax = y+1

    mapname = 'map_{:}_{:}-{:}_{:}-{:}.png'.format(zoom, xtmin, xtmax, ytmin, ytmax)

    ar = (ymax-ymin)/(xmax-xmin)
    art = (ytmax-ytmin)/(xtmax-xtmin)
    ar = art / ar

    if(not os.path.exists(mapname)):
        # Retreive images from OpenStreetMap.org
        i = 1
        for y in range(ytmin, ytmax):
            for x in range(xtmin, xtmax):
                url = 'http://a.tile.openstreetmap.org/'+str(z)+'/'+str(x)+'/'+str(y)+'.png'
                subfilename = 'submap-{i:02d}-{x:d}-{y:d}.png'.format(i=i,x=x,y=y)
                with urllib.request.urlopen(url) as response, open(subfilename, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
                i = i + 1

        # Composite together images.
        cmd = '/sw/bin/montage submap*.png -tile ' + str(xtmax-xtmin) + 'x -geometry 256x256+0+0 ' + mapname
        os.popen(cmd).read()

        # Remove submaps.
        os.popen('rm submap*png').read()

    return(xmin, xmax, ymin, ymax, mapname, ar)

def plotSpeedMap(trk, smoothed=True):
    from cmap_parula import cmap_parula
    import datetime
    from matplotlib.collections import LineCollection
    from matplotlib.colors import ListedColormap
    import matplotlib.image as mpimg

    x = np.array([t['lon'] for t in trk])
    y = np.array([t['lat'] for t in trk])
    z = np.array([t['ds'] for t in trk])
    f = butter_lowpass_filtfilt(z, 5000, 50000)
    # Remove duplicate positions to allow spline interpolation.
    # Uncomment section and use last line to have smooth path but with
    # smoothed speed values.
#   from scipy import interpolate
#   mask = ((np.diff(x) == 0) & (np.diff(y) == 0))
#   x = x[~mask]
#   y = y[~mask]
#   f = f[~mask]
#   tck1, u = interpolate.splprep([x,y], s=0)
#   tck2, u = interpolate.splprep([x,f], s=0)
#   unew = np.linspace(0,1,500)
#   out1 = interpolate.splev(unew,tck1)
#   out2 = interpolate.splev(unew,tck2)
#   x = out1[0]
#   y = out1[1]
#   f = out2[1]
#   pts = np.array([x, y]).T.reshape(-1,2,2)
    pts = np.array([x, y]).T.reshape(-1,1,2)
    segments = np.hstack([pts[:-1], pts[1:]])

    cmap = cmap_parula().parula
    coll = LineCollection(segments, cmap=cmap, linewidth=2)
    coll.set_array(f)

    # Get extents based on the track.
    xmin = min(x); xmax = max(x)
    ymin = min(y); ymax = max(y)
    xdel = xmax - xmin
    ydel = ymax - ymin
    xmin = xmin - 0.05 * xdel; xmax = xmax + 0.05 * xdel
    ymin = ymin - 0.05 * ydel; ymax = ymax + 0.05 * ydel

    # Get new extents based on OSM's tiling, to ensure alignment.
    xmin, xmax, ymin, ymax, mapname, ar = getOSM(xmin, xmax, ymin, ymax)

    fig, ax = plt.subplots()

    ax = plt.gca()

    img = mpimg.imread(mapname)

    implt = plt.imshow(img, zorder=0, extent=[xmin, xmax, ymin, ymax], aspect=ar, alpha=0.4)
    cs = ax.add_collection(coll)

#   ax.set_aspect(1/ar, 'box-forced')

    def fmt(x, pos):
        import math
        if(x > 0):
            y = 60 / x
            m = int(math.floor(y))
            s = int((y - math.floor(y)) * 60)
            return('{:d} ({:d}:{:02d})'.format(int(x), m, s))
        else:
            return('{:d}'.format(int(x)))

    add_colorbar(cs, ax=ax, format=ticker.FuncFormatter(fmt), label='Speed [mph] (Pace [h:mm:ss/mi])')
    cs.set_clim(vmin=1, vmax=10)
#   pos = cbar.ax.get_position()
#   cbar.ax.set_aspect('auto')
#   ax2 = cbar.ax.twinx()
#   ax2.set_ylim([-2,1])
#   pos.x0 += 0.05
#   cbar.ax.set_position(pos)
#   ax2.set_position(pos)

    # Final reset of the extents to focus on the track despite OSM's tiling.
    xmin = min(x); xmax = max(x)
    ymin = min(y); ymax = max(y)
    xdel = xmax - xmin
    ydel = ymax - ymin
    xmin = xmin - 0.05 * xdel; xmax = xmax + 0.05 * xdel
    ymin = ymin - 0.05 * ydel; ymax = ymax + 0.05 * ydel

    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])

    ax.set_xticks([])
    ax.set_yticks([])
    return(plt)

def plotElevationMap(trk, smoothed=True):
    from cmap_parula import cmap_parula
    import datetime
    from matplotlib.collections import LineCollection
    from matplotlib.colors import ListedColormap
    import matplotlib.image as mpimg

    x = np.array([t['lon'] for t in trk])
    y = np.array([t['lat'] for t in trk])
    z = np.array([t['ele'] for t in trk])
    f = butter_lowpass_filtfilt(z, 5000, 50000)
    pts = np.array([x, y]).T.reshape(-1,1,2)
    segments = np.hstack([pts[:-1], pts[1:]])

    cmap = cmap_parula().parula
    coll = LineCollection(segments, cmap=cmap, linewidth=2)
    coll.set_array(f)

    # Get extents based on the track.
    xmin = min(x); xmax = max(x)
    ymin = min(y); ymax = max(y)
    xdel = xmax - xmin
    ydel = ymax - ymin
    xmin = xmin - 0.05 * xdel; xmax = xmax + 0.05 * xdel
    ymin = ymin - 0.05 * ydel; ymax = ymax + 0.05 * ydel

    # Get new extents based on OSM's tiling, to ensure alignment.
    xmin, xmax, ymin, ymax, mapname, ar = getOSM(xmin, xmax, ymin, ymax)

    fig, ax = plt.subplots()

    ax = plt.gca()
    ax.set_aspect(ar)

    img = mpimg.imread(mapname)

    implt = plt.imshow(img, zorder=0, extent=[xmin, xmax, ymin, ymax], aspect=ar, alpha=0.4)
    cs = ax.add_collection(coll)

    add_colorbar(cs, ax=ax, label='Elevation [feet]')

    # Final reset of the extents to focus on the track despite OSM's tiling.
    xmin = min(x); xmax = max(x)
    ymin = min(y); ymax = max(y)
    xdel = xmax - xmin
    ydel = ymax - ymin
    xmin = xmin - 0.05 * xdel; xmax = xmax + 0.05 * xdel
    ymin = ymin - 0.05 * ydel; ymax = ymax + 0.05 * ydel

    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])

    ax.set_xticks([])
    ax.set_yticks([])
    return(plt)

def add_colorbar(im, aspect=10, pad_fraction=0.0, **kwargs):
    """Add a vertical color bar to an image plot."""
    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1/aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)
    return im.axes.figure.colorbar(im, cax=cax, **kwargs)

def plotReport(trk):
    from cmap_parula import cmap_parula
    import datetime
    from matplotlib.collections import LineCollection
    from matplotlib.colors import ListedColormap
    import matplotlib.image as mpimg
    import numpy as np

    fig = plt.figure()
    gs = matplotlib.gridspec.GridSpec(2, 2, height_ratios=[2, 1], width_ratios=[1, 1], wspace=0.5)

    # Plot speed map.
    ax0 = plt.subplot(gs[0,0])

    x = np.array([t['lon'] for t in trk])
    y = np.array([t['lat'] for t in trk])
    z = np.array([t['ds'] for t in trk])
    f = butter_lowpass_filtfilt(z, 5000, 50000)
    pts = np.array([x, y]).T.reshape(-1,1,2)
    segments = np.hstack([pts[:-1], pts[1:]])

    cmap = cmap_parula().parula
    coll = LineCollection(segments, cmap=cmap, linewidth=2)
    coll.set_array(f)

    # Get extents based on the track.
    xmin = min(x); xmax = max(x)
    ymin = min(y); ymax = max(y)
    xdel = xmax - xmin
    ydel = ymax - ymin
    xmin = xmin - 0.05 * xdel; xmax = xmax + 0.05 * xdel
    ymin = ymin - 0.05 * ydel; ymax = ymax + 0.05 * ydel

    # Get new extents based on OSM's tiling, to ensure alignment.
    xmin, xmax, ymin, ymax, mapname, ar = getOSM(xmin, xmax, ymin, ymax)

    ax0.set_aspect(ar)

    img = mpimg.imread(mapname)

    implt = plt.imshow(img, zorder=0, extent=[xmin, xmax, ymin, ymax], aspect=ar, alpha=0.4)
    cs = ax0.add_collection(coll)

    def fmt(x, pos):
        import math
        if(x > 0):
            y = 60 / x
            m = int(math.floor(y))
            s = int((y - math.floor(y)) * 60)
            return('{:d} ({:d}:{:02d})'.format(int(x), m, s))
        else:
            return('{:d}'.format(int(x)))

    add_colorbar(cs, format=ticker.FuncFormatter(fmt), label='Speed [mph]\n(Pace [mm:ss/mi])')
    cs.set_clim(vmin=1, vmax=10)
    # Final reset of the extents to focus on the track despite OSM's tiling.
    xmin = min(x); xmax = max(x)
    ymin = min(y); ymax = max(y)
    xdel = xmax - xmin
    ydel = ymax - ymin
    xmin = xmin - 0.05 * xdel; xmax = xmax + 0.05 * xdel
    ymin = ymin - 0.05 * ydel; ymax = ymax + 0.05 * ydel

    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])

    ax0.set_xticks([])
    ax0.set_yticks([])

    # Plot elevation map.
    ax1 = plt.subplot(gs[0,1])

    x = np.array([t['lon'] for t in trk])
    y = np.array([t['lat'] for t in trk])
    z = np.array([t['ele'] for t in trk])
    f = butter_lowpass_filtfilt(z, 5000, 50000)
    pts = np.array([x, y]).T.reshape(-1,1,2)
    segments = np.hstack([pts[:-1], pts[1:]])

    cmap = cmap_parula().parula
    coll = LineCollection(segments, cmap=cmap, linewidth=2)
    coll.set_array(f)

    # Get extents based on the track.
    xmin = min(x); xmax = max(x)
    ymin = min(y); ymax = max(y)
    xdel = xmax - xmin
    ydel = ymax - ymin
    xmin = xmin - 0.05 * xdel; xmax = xmax + 0.05 * xdel
    ymin = ymin - 0.05 * ydel; ymax = ymax + 0.05 * ydel

    # Get new extents based on OSM's tiling, to ensure alignment.
    xmin, xmax, ymin, ymax, mapname, ar = getOSM(xmin, xmax, ymin, ymax)

    ax1.set_aspect(ar)

    img = mpimg.imread(mapname)

    implt = plt.imshow(img, zorder=0, extent=[xmin, xmax, ymin, ymax], aspect=ar, alpha=0.4)
    cs = ax1.add_collection(coll)

    add_colorbar(cs, ax=ax1, label='Elevation [feet]')

    # Final reset of the extents to focus on the track despite OSM's tiling.
    xmin = min(x); xmax = max(x)
    ymin = min(y); ymax = max(y)
    xdel = xmax - xmin
    ydel = ymax - ymin
    xmin = xmin - 0.05 * xdel; xmax = xmax + 0.05 * xdel
    ymin = ymin - 0.05 * ydel; ymax = ymax + 0.05 * ydel

    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])

    ax1.set_xticks([])
    ax1.set_yticks([])

    # Plot bottom speed / elevation line plot.
    ax2 = plt.subplot(gs[1,:])

    x = [t['elap'] for t in trk]
    y = [t['ds'] for t in trk]
    f = butter_lowpass_filtfilt(y, 5000, 50000)

    plt.xlabel('Elapsed Time [mm:ss]')
    plt.ylabel('Speed [mph]')

    ax2.plot(x, f, 'k-')

    plt.xticks(np.arange(min(x), max(x)+1, 150.0))
    plt.ylim(ymin=0)

    def timeTicks(x, pos):
        d = datetime.timedelta(seconds=x)
        return str(d)
    formatter = matplotlib.ticker.FuncFormatter(timeTicks)
    ax2.xaxis.set_major_formatter(formatter)
    for tick in ax2.get_xticklabels():
        tick.set_rotation(45)

    ax3 = ax2.twinx()

    x = [t['elap'] for t in trk]
    y = [t['ele'] for t in trk]
    f = butter_lowpass_filtfilt(y, 5000, 50000)

    plt.ylabel('Elevation [feet]')

    plt.plot(x, f, 'k-', linewidth=0)

    labels = [i for i in plt.gca().get_yticks()]
    plt.fill_between(x, f, labels[0], color='0.85', zorder=0)

    ax2.set_zorder(ax3.get_zorder()+1)
    ax2.patch.set_visible(False)

    return(plt)

################################################################################
# Command line options.
################################################################################
import __main__ as main
if(__name__ == '__main__' and hasattr(main, '__file__')):
    import textwrap, argparse
    description = textwrap.dedent(
    """
    Script to parse and plot RunKeeper GPX files.
    """)
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--infilename', '-f',
                        nargs = '+',
                        default = '',
                        help = 'which GPS file to parse (default none)')
    parser.add_argument('--elevation', '-e',
                        default = False,
                        action='store_true',
                        help = 'plot elevation data (default False)')
    parser.add_argument('--speed', '-s',
                        default = False,
                        action='store_true',
                        help = 'plot speed data (default False)')
    parser.add_argument('--speedmap', '-sm',
                        default = False,
                        action='store_true',
                        help = 'plot speed map data (default False)')
    parser.add_argument('--elevationmap', '-em',
                        default = False,
                        action='store_true',
                        help = 'plot elevation map data (default False)')
    parser.add_argument('--speedelevation', '--elevationspeed', '-se', '-es',
                        default = False,
                        action='store_true',
                        help = 'plot speed and elevation (default False)')
    parser.add_argument('--report', '-r',
                        default = False,
                        action='store_true',
                        help = 'plot report (default False)')
    args = parser.parse_args()

    opts = [a for a in vars(args) if getattr(args,a)]
    assert(opts != ['infilename']), 'No options selected.'

    for infilename in args.infilename:
        assert(infilename != ''), 'No filename given.'

        rawtrk = importGPX(infilename)
        trk = processRawTrack(rawtrk)

        if(args.elevation):
            plt = plotElevation(trk)
            plt.savefig(infilename + '_elevation.png', dpi=300)
        if(args.speed):
            plt = plotSpeed(trk)
            plt.savefig(infilename + '_speed.png', dpi=300)
        if(args.speedelevation):
            plt = plotSpeedElevation(trk)
            plt.savefig(infilename + '_speedelevation.png', dpi=300)
        if(args.speedmap):
            plt = plotSpeedMap(trk)
            plt.savefig(infilename + '_speedmap.png', dpi=500)
        if(args.elevationmap):
            plt = plotElevationMap(trk)
            plt.savefig(infilename + '_elevationmap.png', dpi=500)
        if(args.report):
            plt = plotReport(trk)
            plt.savefig(infilename + '_report.png', dpi=500)
