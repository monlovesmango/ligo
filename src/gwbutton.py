from tkinter import *

global scan
button_txt = ""

def scanButton():
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
        global scan
        
        if scan.run == 1:
            scan.run = 2
            run_mode['text'] = 'RUN'
#            print('Paused')
        else:
            scan.run = 1
            run_mode['text'] = 'PAUSE'
            end_run.config(fg='black')
#            print('Running')

    def quitScan():
        global scan
        scan.run = 0
        end_run.config(fg='red')
        root.quit()

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
    dwell_time = Scale(root, from_=0, to=500, orient=HORIZONTAL, length=250, showvalue=0, \
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
    root.mainloop()

