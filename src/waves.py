# need numpy to be imported.
twoPi = 2.0 * np.pi
Pi2deg = 180.0 / np.pi
deg2Pi = np.pi / 180.0


class sineWave:
    def __init__(self, amp=0.0, ph=0.0, f=1.0, ofst=0.0):
        self.ampl = amp
        self.phi = ph * deg2Pi   # input in degrees
        self.freq = f * twoPi
        self.offset = ofst
    def show(self):
        print('ampl    = ', self.ampl,"\n"\
              'phi     = ', self.phi * Pi2deg, '(deg)\n'\
              'freq    = ', self.freq / twoPi, '(Hz)\n'\
             )
    def y(self, x, x0=0.0):
        return self.ampl * np.sin((x - x0) * self.freq + self.phi) + self.offset

class gwave:
    def __init__(self, amp=0.0, ph=0.0, f=1.0, ta = 1.0, tf=1.0, ofst=0.0):
        self.ampl = amp
        self.phi = ph * deg2Pi   # input in degrees
        self.freq = f * twoPi
        self.offset = ofst
        self.tauAmpl = ta
        self.tauFreq = tf
    def show(self):
        print('ampl    = ', self.ampl,"\n"\
              'phi     = ', self.phi * Pi2deg, '(deg)\n'\
              'freq    = ', self.freq / twoPi, '(Hz)\n'\
              'offset  = ', self.offset, '\n'\
              'tauAmpl = ', self.tauAmpl, '(seconds)\n'\
              'tauFreq = ', self.tauFreq, '(seconds)'\
             )
    def wave(self, x, x0=0.0):
        ax = lambda a : self.ampl * (1.0 - np.exp(-0.5*(a/self.tauAmpl)**2))
        fx = lambda a : self.freq * (1.0 + np.exp(a/self.tauFreq))
        slope = lambda a, b, c : a * b * np.cos(c)   # amp * frqi * cos(phii), the derivative of amp * sin(phii)
        xdel = x - x0
        y = np.zeros_like(xdel)
        xdi = xdel[0]
        ampi = ax(xdi)
        frqi = fx(xdi)
        phii = self.phi
        yi = ampi * np.sin(phii) + self.offset
        dydx = slope(ampi, frqi, phii)
        y[0] = yi
        for i in range(1, len(x)):
            if xdel[i] >= 0.0 : break
            dx = 0.5 * (xdel[i] - xdi)
            phii = phii + frqi * dx
            yi = yi + dx * dydx                      # calculate yi to half way with info from previous point
            xdi = xdel[i]
            ampi = ax(xdi)
            frqi = fx(xdi)
            phii = phii + frqi * dx                  # calculate yi to this point with info from this point
            dydx = slope(ampi, frqi, phii)
            yi = yi + dx * dydx
            y[i] = yi          
        return y

