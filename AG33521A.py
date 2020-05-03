# "AG33521A.py"
# content; Agilent 33521A interface.
# author; Roch schanen
# created; 2020 May 1
# repository; https://github.com/RochSchanen/rochpygui

# todo: add rms, p-p option
# todo: change amplitde limits depending on the settings
# todo: add bindings
# todo: change _dn to _press

# wxpython: https://www.wxpython.org/
import wx

# LOCAL
from theme    import *
from layout   import *
from controls import *
from buttons  import *

####################################################

class _panel(Control):

    def Start(self):
        # make a dictionary of all the controls
        CTRLS = {}
        # create controls
        CTRLS['FREQUENCY'] = _frequency(self)
        CTRLS['AMPLITUDE'] = _amplitude(self)
        CTRLS['OUTPUT']    = _ouput(self)
        CTRLS['IMPEDANCE'] = _impedance(self)
        # make layout
        h1 = Group(HORIZONTAL)
        v1 = Group(VERTICAL)
        v1.Place(CTRLS['FREQUENCY'], deco = 'Groove')
        v1.Place(CTRLS['AMPLITUDE'], deco = 'Groove')
        
        h2 = Group(HORIZONTAL)
        h2.Place(CTRLS['OUTPUT'],    deco = 'Groove')
        h2.Place(CTRLS['IMPEDANCE'], deco = 'Groove')
        h1.Place(v1)
        h1.Place(h2)
        # records objects        
        self.CTRLS = CTRLS
        # make content
        content = Group(VERTICAL)
        content.Place(Text(self, 'AG33220A'))
        content.Place(h1)
        # expantions
        content.Expand()
        h1.Expand()
        v1.Expand()
        h2.Expand()
        # draw decorations
        content.DrawAllDecorations(self)
        self.SetSize(content.GetSize())
        # done
        return

    def SetVisa(self, Instrument):
        self.CTRLS['FREQUENCY'].SetVisa(Instrument)
        self.CTRLS['AMPLITUDE'].SetVisa(Instrument)
        self.CTRLS['OUTPUT'].SetVisa(Instrument)
        self.CTRLS['IMPEDANCE'].SetVisa(Instrument)
        return

####################################################

class _impedance(Control):

    def Start(self):
        self.instr = None
        # make leds
        self.leds = []
        LEDS = Group(VERTICAL)
        lib, libnam = Theme.GetImages('Round LED', 'White')
        for name in ['50 Ohms', 'High Z']:
            led = Display(self, lib, libnam)
            NAME = Group(HORIZONTAL)
            NAME.Place(led)
            NAME.Place(Text(self, name))
            LEDS.Place(NAME, LEFT)
            self.leds.append(led)
        # make button
        lib, libnam = Theme.GetImages('Push', 'Blank')
        BUTTON = Push(self, lib, libnam)
        BUTTON.BindEvent(self._update)
        # make content
        Content = Group(VERTICAL)
        Content.Place(Text(self, "Impedance"), border = (0,0,0,5))
        Content.Place(LEDS)
        Content.Place(BUTTON, border = (0,0,5,5))
        # draw decoration
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        # done
        self._refresh()
        return

    def _refresh(self):
        for l in range(len(self.leds)):
            self.leds[l].SetValue(l == self.status)
        return

    def _update(self, event):
        self.status += 1
        self.status %= 2
        self.SendEvent()
        self._refresh()
        self._write()
        return

    def SetVisa(self, Instrument):
        self.instr = Instrument
        X = self.instr.query('OUTPUT:LOAD?')
        # coerce to 50 or High impedance
        self.status = 0
        if int("%.0f" % float(X)) != 50:
            self.instr.write('OUTPUT:LOAD INF')
            self.status = 1
        self._refresh()
        return

    def _write(self):
        if self.instr:
            X = ["50", "INF"][self.status]
            self.instr.write("OUTPUT:LOAD %s" % X)
            x = float(self.instr.query('VOLT?'))
            self.parent.CTRLS['AMPLITUDE'].SetValue(x)
        return

####################################################

class _ouput(Control):

    def Start(self):
        self.status = 0
        self.instr = None
        lib, libnam = Theme.GetImages('LED Switch', 'Green')       
        self.BTNSW = Switch(self, lib, libnam)
        self.BTNSW.BindEvent(self._pressed)
        Content = Group(VERTICAL)
        Content.Place(Text(self, 'Output'))
        Content.Place(self.BTNSW, border=(0,0,10,10))
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        return

    def SetVisa(self, Instrument):
        self.instr = Instrument
        x = int(self.instr.query("OUTPUT?"))
        self.BTNSW.SetValue(x)
        self.SetValue(x)
        return

    def SetValue(self, Value):
        self.status = Value
        if self.instr: self.instr.write("OUTPUT %d" % self.status)
        return
    
    def _pressed(self, event):
        self.SetValue(event.status)
        self.SendEvent()
        return

####################################################

class _wheelctrl(Control):

    def Start(self):
        self._init()
        self.instr = None
        self.wheels = []        
        n, d, b = self.n, self.d, 0
        CTRL = Group(HORIZONTAL)
        for char in list(self.ctrlformat):
            if char == '.':
                lib, Names = Theme.GetImages('Hex Dot', 'White')
                CTRL.Place(Display(self, lib, Names))
                continue
            if char == '0':
                lib, nNames = Theme.GetImages('Hex Digit', 'Normal')
                lib, hNames = Theme.GetImages('Hex Digit', 'Hoover')
                wheel = Wheel(self, lib, nNames, hNames)
                wheel.BindEvent(self._update)
                CTRL.Place(wheel, border = (b,0,0,0))
                self.wheels.append(wheel)
                b = 0
            if char == ' ': b = 3
        lib, Names = Theme.GetImages('Hex Unit', self.Unit)
        CTRL.Place(Display(self, lib, Names))
        # make layout
        Content = Group(VERTICAL)
        Content.Place(Text(self, self.label))
        Content.Place(CTRL, border = (5,15,5,5))
        # done
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        return

    def GetValue(self):
        p, x = 10**(self.n-1), 0 
        for wheel in self.wheels:
            value = wheel.GetValue()
            x += wheel.GetValue()*p
            p /= 10
        return float(self.format % x)

    def SetValue(self, Value):
        wheeln = 0
        for char in list(self.format % Value):
            if char == '.': continue
            wheel = self.wheels[wheeln]
            wheel.SetValue(int(char))
            wheeln += 1
        self.status = Value
        V = self.format % Value
        if self.instr: self.instr.write(self.VISA+' '+V)
        return

    def _update(self, event):
        x = self.GetValue()
        wheeln = self.wheels.index(event.caller)
        weight = 10**(self.n-wheeln)
        overflow = event.caller.overflow
        if overflow: x += overflow*weight
        if x < self.MinVal: event.caller.Reset(); return
        if x > self.Maxval: event.caller.Reset(); return
        self.SetValue(x)
        self.SendEvent()
        return

    def SetVisa(self, Instrument):
        self.instr = Instrument
        S = self.instr.query('%s?' % self.VISA)
        x = float(S)
        x = max(x, self.MinVal)
        x = min(x, self.Maxval)
        self.SetValue(x)
        return

class _amplitude(_wheelctrl):

    def _init(self):
        self.label = 'Amplitude'
        self.n = 1 # integer digits (Number of)
        self.d = 6 # decimal digits (Number of)
        self.format = f'%0{self.n+self.d+1}.{self.d}f'
        self.ctrlformat = '0.000 000'
        self.MinVal = 0.000707
        self.Maxval = 7.071
        self.Unit = 'V'
        self.VISA = 'VOLT'
        return

class _frequency(_wheelctrl):

    def _init(self):
        self.label = 'Frequency'
        self.n = 6 # integer digits (Number of)
        self.d = 6 # decimal digits (Number of)
        self.format = f'%0{self.n+self.d+1}.{self.d}f'
        self.ctrlformat = '000 000.000 000'
        self.MinVal = 1E-6
        self.Maxval = 1E6-1E-6
        self.Unit = 'Hz'
        self.VISA = 'FREQ'
        return
