# "AG33521A.py"
# content; Agilent 33521A interface.
# author; Roch schanen
# created; 2020 May 1
# repository; https://github.com/RochSchanen/rochpygui

# todo: add rms, p-p option
# todo: change amplitude limits depending on the settings
# todo: add bindings
# todo: change _dn to _press

# wxpython: https://www.wxpython.org/
import wx

# numpy: https://numpy.org/
from numpy import inf

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
        CTRLS['FREQUENCY'] = _frequency(self)
        CTRLS['AMPLITUDE'] = _amplitude(self)
        CTRLS['OUTPUT']    = _ouput(self)
        CTRLS['IMPEDANCE'] = _impedance(self)
        self.CTRLS = CTRLS
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
        # make content
        content = Group(VERTICAL)
        content.Place(Text(self, 'AG33220A'))
        content.Place(h1)
        # expansions
        content.Expand()
        h1.Expand()
        v1.Expand()
        h2.Expand()
        # bindings
        for ctrl in CTRLS.values():
            ctrl.BindEvent(self._update)
        # draw decorations
        content.DrawAllDecorations(self)
        self.SetSize(content.GetSize())
        # done
        return

    def _update(sefl, event):
        pass

    def SetVisa(self, Instrument):
        self.instr = Instrument
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

    # this control affects the amplitude value
    def _update(self, event):
        self.status += 1
        self.status %= 2
        self._write()
        # update limits and displays
        self.parent.CTRLS['AMPLITUDE']._getLimit()
        self.parent.CTRLS['AMPLITUDE']._read()
        self.parent.CTRLS['AMPLITUDE']._refresh()
        # done
        self.SendEvent()
        self._refresh()
        return

    def SetVisa(self, Instrument):
        self.instr = Instrument
        X = self.instr.query('OUTPUT:LOAD?')
        # coerce to 50 or High impedance
        self.status = 0
        if int("%.0f" % float(X)) != 50: # use round()?
            self.instr.write('OUTPUT:LOAD INF')
            self.status = 1
        self._refresh()
        return

    def _write(self):
        if self.instr:
            X = ["50", "INF"][self.status]
            self.instr.write("OUTPUT:LOAD "+X)
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

class _amplitude(Control):

    def SetFormat(self, SFormat):
        n, d, f = 0, 0, False
        for c in list(SFormat):
            if c == '.': f = True
            if c == '0':
                n += [1, 0][f]
                d += [0, 1][f]
        self.format = f'%0{n+d+1}.{d}f'
        self.n = n
        return

    def Start(self):
        # LOCAL
        SFormat = '00.000 000'
        self.SetFormat(SFormat)
        self.MinVal, self.Maxval = -inf, +inf
        self.status = 0.0, 0
        self.instr = None
        # build control
        b = 0
        self.wheels = []        
        CTRL = Group(HORIZONTAL)
        for char in list(SFormat):
            if char == '.':
                lib, Names = Theme.GetImages('Hex Dot', 'White')
                CTRL.Place(Display(self, lib, Names))
                # continue
            if char == '0':
                lib, nNames = Theme.GetImages('Hex Digit', 'Normal')
                lib, hNames = Theme.GetImages('Hex Digit', 'Hoover')
                wheel = Wheel(self, lib, nNames, hNames)
                wheel.BindEvent(self._update)
                CTRL.Place(wheel, border = (b,0,0,0)); b = 0
                self.wheels.append(wheel)
            if char == ' ': b = 3
        lib, nNames = Theme.GetImages('Hex Unit', 'Volt Normal')
        lib, hNames = Theme.GetImages('Hex Unit', 'Volt Hoover')
        self.unit = Wheel(self, lib, nNames, hNames) 
        self.unit.BindEvent(self._update)
        CTRL.Place(self.unit)
        # make layout
        Content = Group(VERTICAL)
        Content.Place(Text(self, "Amplitude"))
        Content.Place(CTRL, border = (5,15,5,5))
        # done
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        return

    # refresh buttons from status
    def _refresh(self):
        x, u = self.status
        wheeln = 0
        for char in list(self.format % x):
            if char == '.': continue
            wheel = self.wheels[wheeln]
            wheel.SetValue(int(char))
            wheeln += 1
        self.unit.SetValue(u)
        return

    # read digits
    def _read(self):
        x, u = self.status
        if self.instr:
            S = self.instr.query('VOLT?')
            x = float(S)
            x = max(x, self.MinVal)
            x = min(x, self.Maxval)
            self.status = x, u
        return

    # write digits
    def _write(self):
        x, u = self.status
        V = self.format % x
        if self.instr:
            self.instr.write('VOLT '+V)
        return

    # update digits or unit
    def _update(self, event):
        # get parameters
        x, u = self.status
        # select digit or unit
        if event.caller == self.unit:
            u = event.caller.GetValue()
            self.instr.write('VOLT:UNIT '+['VRMS','VPP'][u])
            self.status = x, u
            self._getLimit()
            self._read()
        else:
            wheeln = self.wheels.index(event.caller)
            weight = 10**(self.n-wheeln-1)
            x += event.caller.step*weight
            if x < self.MinVal: event.caller.Reset(); return
            if x > self.Maxval: event.caller.Reset(); return
            self.status = x, u
            self._write()
        # done
        self.SendEvent()
        self._refresh()
        return

    def _getLimit(self):
        if self.instr:
            MIN = self.instr.query('VOLT? MIN')
            MAX = self.instr.query('VOLT? MAX')
            self.MinVal, self.Maxval = float(MIN), float(MAX)
            # correction: when 50 Ohms, Vrms MinVal must be 0.000355V
            self.MinVal = max(self.MinVal, 0.000355)
        return

    def SetVisa(self, Instrument):
        self.instr = Instrument
        self._getLimit()
        x, u = self.status
        S = self.instr.query('VOLT:UNIT?')
        u = ['VRMS\n','VPP\n'].index(S)
        self.status = x, u
        self._read()
        self._refresh()
        return

####################################################

class _frequency(Control):

    def SetFormat(self, SFormat):
        n, d, f = 0, 0, False
        for c in list(SFormat):
            if c == '.': f = True
            if c == '0':
                n += [1, 0][f]
                d += [0, 1][f]
        self.format = f'%0{n+d+1}.{d}f'
        self.n = n
        return

    def Start(self):
        # LOCAL
        SFormat = '00 000.000 00'
        self.MinVal = 1.0E-5
        self.Maxval = 1.0E5-1.0E-5
        self.SetFormat(SFormat)
        self.status = 0.0
        self.instr = None
        # build control
        b = 0
        self.wheels = []        
        CTRL = Group(HORIZONTAL)
        for char in list(SFormat):
            if char == '.':
                lib, Names = Theme.GetImages('Hex Dot', 'White')
                CTRL.Place(Display(self, lib, Names))
                # continue
            if char == '0':
                lib, nNames = Theme.GetImages('Hex Digit', 'Normal')
                lib, hNames = Theme.GetImages('Hex Digit', 'Hoover')
                wheel = Wheel(self, lib, nNames, hNames)
                wheel.BindEvent(self._update)
                CTRL.Place(wheel, border = (b,0,0,0)); b = 0
                self.wheels.append(wheel)
            if char == ' ': b = 3
        lib, Names = Theme.GetImages('Hex Unit', 'Hz')
        self.unit = Display(self, lib, Names) 
        CTRL.Place(self.unit)
        # make layout
        Content = Group(VERTICAL)
        Content.Place(Text(self, "Frequency"))
        Content.Place(CTRL, border = (5,15,5,5))
        # done
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        return

    # refresh buttons from status
    def _refresh(self):
        x = self.status
        wheeln = 0
        for char in list(self.format % x):
            if char == '.': continue
            wheel = self.wheels[wheeln]
            wheel.SetValue(int(char))
            wheeln += 1
        return

    # read digits
    def _read(self):
        x = self.status
        if self.instr:
            S = self.instr.query('FREQ?')
            x = float(S)
            x = max(x, self.MinVal)
            x = min(x, self.Maxval)
        self.status = x
        return

    # write digits
    def _write(self):
        x = self.status
        V = self.format % x
        if self.instr:
            self.instr.write('FREQ '+V)
        return

    # update digits or unit
    def _update(self, event):
        # get parameters
        x = self.status
        # select digit or unit
        wheeln = self.wheels.index(event.caller)
        weight = 10**(self.n-wheeln-1)
        x += event.caller.step*weight
        if x < self.MinVal: event.caller.Reset(); return
        if x > self.Maxval: event.caller.Reset(); return
        self.status = x
        self._write()
        # done
        self.SendEvent()
        self._refresh()
        return

    def SetVisa(self, Instrument):
        self.instr = Instrument
        self._read()
        self._refresh()
        return
