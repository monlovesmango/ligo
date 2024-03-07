
### start python at command line: > python -i gwplot.py
# import string
import time
import sys
import os.path
from tkinter import *
from threading import Thread
import numpy as np
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import gwpy
from  gwpy.timeseries import TimeSeries as ts

gps_start   = 1187008698
gps_end     = 1187009298
gps_span    = 600
h1 = 0
l1 = 1
v1 = 2

button_txt = ""
global root, root_after_id

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
        self.run = 1
    def show(self):
        print('start = ', self.start, '   stop = ', self.stop, '\n'\
              'incr   = ', self.incr, '\n'\
              'count  = ', self.count, '\n'\
              'window = ', self.window, '\n'\
              'dwell  = ', self.dwell, '\n'\
              'idle   = ', self.idle, '\n'\
              'run    = ', self.run
             )

scan = scan_info(0.2, 200, 10, 0.3, 1.0)

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


# def xfile(afile, globalz=None, localz=None):
#     with open(afile, "r") as fh:
#         exec(fh.read(), globalz, localz)

# xfile("./src/gwbutton.py", globals())
# xfile("./src/waves.py", globals())

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
    for i in range(len(ligo)):
        if ligo[i].flag:
            datafile = "./data/" + ligo[i].name + ".txt"
            if os.path.isfile(datafile):
                print('Loading', ligo[i].name, 'from cached data...')
                ligo[i].data = ts.read(datafile)
            else:
                print('Fetching and saving', ligo[i].name, 'data...')
                ligo[i].data = ts.fetch_open_data(ligo[i].short_name, gps_start, gps_end)
                ligo[i].data.write(datafile)
            plot_data_index[ligo_used] = i
            ligo_used = ligo_used + 1


def plot_data(tincr = 0.0):
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
    set_time_limits()

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

def next_frame():
    global root, root_after_id
    if scan.run == 1:
        set_time_limits(scan.incr)
        root_after_id = root.after(int(scan.dwell * 1000), next_frame)

def start():
    global root, root_after_id
    root = Tk()  # create parent window
    root.geometry('300x160')
    root.title('Scan control')

    dwell_scale = IntVar()

    def dwellTime(newScale):
#        global scan
        scan.dwell = 0.05 * float(newScale)
        dwell_value['text'] = f'{scan.dwell:.2f}'

    def incrUp():
        global scan

        m = -2
        xm = abs(scan.incr)
        while xm >= 0.1:
            m = m + 1
            xm = xm / 10

        if xm < .02:
            n = 2
        elif xm < .05:
            n = 5
        else:
            n = 1
            m = m + 1

        xm = n * 10**m

        if scan.incr > 0:
            scan.incr = xm
        elif scan.incr < 0:
            scan.incr = -xm

        incr_value['text'] = str(scan.incr)
#    print("New scan incr: ", scan.incr)

    def incrDown():
        global scan

        m = -1
        xm = abs(scan.incr)
        while xm > 0.1:
            m = m + 1
            xm = xm / 10

#        print("m = ", m, ": xm = ", xm)
        if xm <= 0.02:
            n = 1
        elif xm <= 0.05:
            n = 2
        else:
            n = 5

        xm = n * 10**(m - 1)

        if scan.incr > 0:
            scan.incr = xm
        elif scan.incr < 0:
            scan.incr = -xm

        incr_value['text'] = str(scan.incr)
#        print("New scan.incr: ", scan.incr)

    def switchDir():
        global scan
        scan.incr = -scan.incr
        if scan.incr > 0:
            switch_dir['text'] = "BACKWARD"
#        print('Moving forward')
        else:
            switch_dir['text'] = "FORWARD"
#            print('Moving backward')

        incr_value['text'] = str(scan.incr)

    def runMode():
        global scan, root_after_id
        
        if scan.run == 1:
            scan.run = 2
            run_mode['text'] = 'RUN'
#            print('Paused')
        else:
            scan.run = 1
            run_mode['text'] = 'PAUSE'
            end_run.config(fg='black')
            root_after_id = root.after(int(scan.dwell * 1000), next_frame)
#            print('Running')

    def quitScan():
        global scan, root_after_id
        end_run.config(fg='red')
        root.after_cancel(root_after_id)
        root.quit()
        root.destroy()

    if scan.run == 1:
        button_txt = "PAUSE"
    else:
#        scan.run = 2
        button_txt = "RUN"

    run_mode = Button(root, text=button_txt, justify="center", command=runMode)
    run_mode.place(x=20, y=10)

    if scan.incr > 0:
        button_txt = "BACKWARD"
    else:
        button_txt = "FORWARD"

    switch_dir = Button(root, text=button_txt, justify="center", command=switchDir)
    switch_dir.place(x=100, y=10)

    dwell_label = Label(root, text="DWELL TIME", justify="center")
    dwell_label.place(x=25, y=50)
    dwell_value = Label(root, text=f'{scan.dwell:.2f}', justify="center")
    dwell_value.place(x=120, y=50)
    dwell_scale.set(int(scan.dwell * 20.0))
    dwell_time = Scale(root, from_=1, to=500, orient=HORIZONTAL, length=250, showvalue=0, \
                   variable=dwell_scale, command=dwellTime)
    dwell_time.place(x=25, y=70)

    incr_label = Label(root, text="SCAN STEP SIZE", justify="center")
    incr_label.place(x=100, y=100)

    incr_down = Button(root, text="DOWN", justify="center", command=incrDown)
    incr_down.place(x=20, y=115)

    button_txt = str(scan.incr)
    incr_value = Label(root, text=button_txt, justify="center")
    incr_value.place(x=120, y=120)

    incr_up = Button(root, text="UP", justify="center", command=incrUp)
    incr_up.place(x=220, y=115)

    if scan.run == 0:
        button_txt = 'red'
    else:
        button_txt = 'black'
    end_run = Button(root, text="STOP", justify="center", fg = button_txt, command=quitScan)
    end_run.place(x=220, y=10)

    root_after_id = root.after(int(scan.dwell * 1000), next_frame)
    root.mainloop()

fetch_data()
plot_data()
print('End of gwplot')
