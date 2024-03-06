
### start python at command line: > python -i gwplot.py
import string
import time
import sys
from threading import Thread
import numpy as np
import matplotlib

#matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import gwpy
from  gwpy.timeseries import TimeSeries as ts

gps_start   = 1187008698
gps_end     = 1187009298
gps_span    = 600
h1 = 0
l1 = 1
v1 = 2


class ligo_detector:
   def __init__(self, lName, sName, iflg = False):
      self.name = lName
      self.short_name = sName
      self.flag = iflg
      self.data = [None, None, None]

ligo = [ ligo_detector('Hanford', 'H1', True), \
         ligo_detector('Livingston', 'L1', True), \
         ligo_detector('Virgo', 'V1', False) ]

class plot_info:
    def __init__(self):
        self.axis = None
        self.lines = None
        self.start = 0
        self.stop  = 1
        self.low = -0.1
        self.high = 0.1

    def show(self):
        print('start = ', self.start, "\n"\
              'stop  = ', self.stop, '\n'\
              'low   = ', self.low, '\n'\
              'high  = ', self.high
             )

lpi = [plot_info(), plot_info(), plot_info()]    # ligo plot info

class  scan_info:
    def __init__(self, inc=0.2, cnt=20, wndw=1.0, dwl=0.01, idl=1.0):
        self.start = 1187008700
        self.stop  = 1
        self.incr  = inc
        self.count = cnt
        self.window = wndw
        self.dwell = dwl
        self.idle  = idl
        self.run = 0
    def show(self):
        print('start = ', self.start, '   stop = ', self.stop, '\n'\
              'incr   = ', self.incr, '\n'\
              'count  = ', self.count, '\n'\
              'window = ', self.window, '\n'\
              'dwell  = ', self.dwell, '\n'\
              'idle   = ', self.idle, '\n'\
              'run    = ', self.run
             )

scan = scan_info(0.2, 50, 10, 0.3, 1.0)

ligo_names = ['Hanford', 'Livingston', 'Virgo']
ligo_short_names = ['H1', 'L1', 'V1']
# ligo_flag = [True, True, False]
# ligo_data = [None, None, None]
# plot_axis = [None, None, None]
# plot_lines = [None, None, None]
plot_data_index = [None, None, None]
ligo_used = 0
raw_plot = None
# scan_count = 50
# scan_run = 0
# scan_dwell = 0.2
# scan_idle = 0.5
# scan_incr = .1
# x_window = 1.0
# x_start = 0.0
# x_stop = 1.0


def xfile(afile, globalz=None, localz=None):
    with open(afile, "r") as fh:
        exec(fh.read(), globalz, localz)

xfile("./gwbutton.py", globals())
xfile("./waves.py", globals())

def ligo_gps_time(t):
    gpst = 0

    if type(t) != str:
        print ('gps time error: Please give valid date/time string')
    elif len(t) < 11:
        print ('gps time error: Not a valid date/time string')
    else:
        gpst = gwpy.time.to_gps(t).seconds
        print (gpst)

    return gpst

def testBit(int_type, offset):
        mask = 1 << offset
        return(int_type & mask)

def fetch_data():
    global ligo_used
    global gps_span
    global plot_data_index

    ligo_used = 0
    gps_span = gps_end - gps_start
    for i in range(3):
        if ligo[i].flag:
            ligo[i].data = ts.fetch_open_data(ligo[i].short_name, gps_start, gps_end)
            plot_data_index[ligo_used] = i
            ligo_used = ligo_used + 1


def plot_data():
    global raw_plot, lpi
    raw_plot, axes = plt.subplots(ligo_used, sharex=True, figsize=(12, 7))
    for i in range(ligo_used):
        idx = plot_data_index[i]
        lpi[i].axis = axes[i]
        lpi[i].lines = axes[i].plot(ligo[idx].data)
        lpi[i].start, lpi[i].stop = axes[i].get_xlim()
        lpi[i].low, lpi[i].high = axes[i].get_ylim()
    plt.draw()
    plt.show(block=False)






def set_time_limits(tincr = 0.0):
#    global gps_start, gps_end
#    global scan # x_start, x_stop, x_window
#    global lpi  # plot_axis
#
    if scan.start > gps_start:
        x = scan.start + tincr
        if x < gps_start:
            scan.start = x
            scan.stop = scan.start + scan.window
        elif x > gps_end:
            scan.start = x - scan.window
            scan.stop = x
        else:
            scan.start = x
            scan.stop = x + scan.window
            
    lpi[0].axis.set_xlim(scan.start, scan.stop)
    plt.draw()
#    raw_plot.canvas.draw()
#    raw_plot.canvas.flush_events()

def time_scan(pltFlag = True):
    i = 0
    while i < scan.count:
        if scan.run == 2:
            loop = 0
            while loop < 20:
                time.sleep(scan.idle)
                loop = loop + 1
#
            print('Scanning on hold...')
            sys.stdout.flush()
        elif scan.run == 0:
            i = scan.count      # force early exit 
        else:
            set_time_limits(scan.incr)
            i = i + 1
            if pltFlag : plt.pause(0.0001)     # pltFlag == False, if run in a thread
#
#        print('round: ', i, '   x start= ', x_start, ', x_stop= ', x_stop)
#        sys.stdout.flush()
        time.sleep(scan.dwell)
    print ('Time scanning finished...')
    sys.stdout.flush()
#
print('End of gwplot')
