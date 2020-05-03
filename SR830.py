# "SR830.py"
# content; SR830 interface.
# author; Roch schanen
# created; 2020 April 19
# repository; https://github.com/RochSchanen/rochpygui

# todo: add ampere units
# todo: add bindings
# todo: add configuration files
# todo: change _dn to _press

# wxpython: https://www.wxpython.org/
import wx

# LOCAL
from theme    import *
from layout   import *
from controls import *
from display  import *
from buttons  import *
from numpy    import exp, log

####################################################

_TIMER_DELAY = 1000

####################################################

class _panel(Control):

    def Start(self):
        # make a dictionary of all the controls        
        CTRLS = {}
        # create Controls
        CTRLS['SENSITIVITY']  = _sensitivity(self)
        CTRLS['TIMECONSTANT'] = _timeConstant(self)
        CTRLS['INPUT']        = _input(self)
        CTRLS['SLOPE']        = _slope(self)
        CTRLS['RESERVE']      = _reserve(self)
        CTRLS['SYNC']         = _sync(self)
        CTRLS['COUPLING']     = _coupling(self)
        CTRLS['GROUNDING']    = _grounding(self)
        CTRLS['FILTERS']      = _filters(self)
        CTRLS['OVERLOAD']     = _overload(self)
        CTRLS['UNLOCK']       = _unlock(self)
        CTRLS['PHASE']        = _phase(self)
        CTRLS['VX']           = _Vx(self)
        CTRLS['VY']           = _Vy(self)
        # Place Controls
        h1 = Group(HORIZONTAL)
        h1.Place(CTRLS['TIMECONSTANT'], deco = 'Groove')
        h1.Place(CTRLS['SENSITIVITY'],  deco = 'Groove')
        v1 = Group(VERTICAL)
        v1.Place(CTRLS['OVERLOAD'],     deco = 'Groove')
        v1.Place(CTRLS['UNLOCK'],       deco = 'Groove')
        h1.Place(v1,                    deco = None)
        h2 = Group(HORIZONTAL)
        h2.Place(CTRLS['INPUT'],        deco = 'Groove')
        h2.Place(CTRLS['SLOPE'],        deco = 'Groove')
        h2.Place(CTRLS['RESERVE'],      deco = 'Groove')
        h3 = Group(HORIZONTAL)
        h3.Place(CTRLS['COUPLING'],     deco = 'Groove')
        h3.Place(CTRLS['GROUNDING'],    deco = 'Groove')
        h3.Place(CTRLS['FILTERS'],      deco = 'Groove')
        h3.Place(CTRLS['SYNC'],         deco = 'Groove')
        h4 = Group(HORIZONTAL)
        h4.Place(CTRLS['PHASE'],        deco = 'Groove')
        h4.Place(CTRLS['VX'],           deco = 'Groove')
        h4.Place(CTRLS['VY'],           deco = 'Groove')
        # record dictionary
        self.CTRLS = CTRLS
        # make panel
        Content = Group(VERTICAL)
        Content.Place(Text(self, 'SR830'), deco = None)
        Content.Place(h1, deco = None)
        Content.Place(h4, deco = None)
        Content.Place(h2, deco = None)
        Content.Place(h3, deco = None)
        # Expansions
        Content.Expand()
        h1.Expand()
        v1.Expand()
        h2.Expand()
        h3.Expand()
        h4.Expand()
        # draw decorations
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        # done
        return

    def SetVisa(self, Instrument):
        self.instr = Instrument
        for CTRL in self.CTRLS.values():
            CTRL.SetVisa(Instrument)
        # Switch on timer
        self.Timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._onTimer, self.Timer)
        self.Timer.Start(_TIMER_DELAY)
        return

    def _onTimer(self, event):
        if self.instr:
            S = self.instr.query('SNAP?1,2')
            X, Y = S.split(',')
            self.CTRLS['VX'].SetValue(float(X))
            self.CTRLS['VY'].SetValue(float(Y))
            S = self.instr.query("LIAS?")
            self.CTRLS['UNLOCK'].SetValue(int(S))
            self.CTRLS['OVERLOAD'].SetValue(int(S))
        return

####################################################

def MiniControl(Ctrl, Names):
    l = []
    V = Group(VERTICAL)
    lib, libnam = Theme.GetImages('Round LED', Ctrl.colour)
    for name in Names:
        led = Display(Ctrl, lib, libnam)
        l.append(led)
        H = Group(HORIZONTAL)
        H.Place(led)
        H.Place(Text(Ctrl, name))
        V.Place(H, LEFT)
    Ctrl.leds.append(l)
    return V

####################################################

class _sensitivity(Control):

    def Start(self):
        # control state
        self.status = 0
        self.instr = None
        # displays
        self.leds = []
        # style
        self.colour = 'Green'
        # "status -> display" encoding
        self.encoding = [   
            [1,2,3],[0,2,3],
            [2,1,3],[1,1,3],[0,1,3],
            [2,0,3],[1,0,3],[0,0,3],
            [2,2,2],[1,2,2],[0,2,2],
            [2,1,2],[1,1,2],[0,1,2],
            [2,0,2],[1,0,2],[0,0,2],
            [2,2,1],[1,2,1],[0,2,1],
            [2,1,1],[1,1,1],[0,1,1],
            [2,0,1],[1,0,1],[0,0,1],
            [2,2,0]]
        # make led displays
        display = Group(HORIZONTAL)
        display.Place(MiniControl(self, ['5', '2', '1']))
        display.Place(MiniControl(self, ['x100', 'x10', 'x1']))
        display.Place(MiniControl(self, ['V', 'mV', 'µV', 'nV']))
        # make buttons
        lib, libnam = Theme.GetImages('Push', 'Up')     
        BTNUP = Push(self, lib, libnam)
        BTNUP.BindEvent(self._up)       
        lib, libnam = Theme.GetImages('Push', 'Down')       
        BTNDN = Push(self, lib, libnam)
        BTNDN.BindEvent(self._dn)
        # group buttons
        buttons = Group(HORIZONTAL)
        buttons.Place(BTNUP)
        buttons.Place(BTNDN)
        # group content
        Content = Group(VERTICAL)
        Content.Place(Text(self, 'Sensitivity'), border = (0,0,0,5))
        Content.Place(display)
        Content.Place(buttons, border = (0,0,5,5))
        # Draw decors
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        # done
        self._refresh()
        return

    def SetVisa(self, Instrument):
        self.instr = Instrument
        self.SetValue(int(self.instr.query('SENS?')))
        return

    # set led values according to the status value
    def _refresh(self):
        for led, num in zip(self.leds, self.encoding[self.status]):
            for l in range(len(led)): led[l].SetValue(l==num)
        if self.instr: self.instr.write("SENS %d" % self.status)
        return

    # move status up
    def _up(self, event):
        if self.status < 26:
            self.status += 1
            self._refresh()
            self.SendEvent()
        return

    # move status down
    def _dn(self, event):
        if self.status > 0:
            self.status -= 1
            self._refresh()
            self.SendEvent()
        return

    # set status value and refresh
    def SetValue(self, value):
        self.status = value
        self._refresh()
        return

####################################################

class _timeConstant(Control):

    def Start(self):
        # control state
        self.status = 0
        self.instr = None
        # displays
        self.leds = []
        # style
        self.colour = 'Green'
        # status -> display encoding
        self.encoding =    [[1,1,3],[0,1,3],[1,0,3],[0,0,3],
            [1,2,2],[0,2,2],[1,1,2],[0,1,2],[1,0,2],[0,0,2],
            [1,2,1],[0,2,1],[1,1,1],[0,1,1],[1,0,1],[0,0,1],
            [1,2,0],[0,2,0],[1,1,0],[0,1,0]]
        # make led display
        display = Group(HORIZONTAL)
        display.Place(MiniControl(self, ['3', '1']))
        display.Place(MiniControl(self, ['x100', 'x10', 'x1']))
        display.Place(MiniControl(self, ['kS', 'S', 'mS', 'µS']))
        # make buttons
        buttons = Group(HORIZONTAL)
        lib, libnam = Theme.GetImages('Push', 'Up')     
        BTNUP = Push(self, lib, libnam)
        BTNUP.BindEvent(self._up)       
        buttons.Place(BTNUP)
        lib, libnam = Theme.GetImages('Push', 'Down')       
        BTNDN = Push(self, lib, libnam)
        BTNDN.BindEvent(self._dn)
        buttons.Place(BTNDN)
        # create content
        Content = Group(VERTICAL)
        Content.Place(Text(self, 'Time Constant'), border = (0,0,0,5))
        Content.Place(display)
        Content.Place(buttons, border = (0,0,5,5))
        # Draw decors
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        # done
        self._refresh()
        return

    def SetVisa(self, Instrument):
        self.instr = Instrument
        self.SetValue(int(self.instr.query('OFLT?')))
        return

    def _refresh(self):
        for led, num in zip(self.leds, self.encoding[self.status]):
            for l in range(len(led)): led[l].SetValue(l==num)
        if self.instr: self.instr.write("OFLT %d" % self.status)
        return

    def _up(self, event):
        if self.status < 19:
            self.status += 1
            self.SendEvent()
            self._refresh()
        return

    def _dn(self, event):
        if self.status > 0:
            self.status -= 1
            self.SendEvent()
            self._refresh()
        return

    def SetValue(self, value):
        self.status = value
        self._refresh()
        return

####################################################

class _single(Control):

    def Start(self):
        self._init()
        # control state
        self.status = 0
        self.instr = None
        # displays
        self.leds = []
        # make led display
        display = Group(HORIZONTAL)
        for label in self.labels:
            display.Place(MiniControl(self, label))
        # make buttons
        lib, libnam = Theme.GetImages('Push', self.style)       
        BTNDN = Push(self, lib, libnam)
        BTNDN.BindEvent(self._dn)
        # create content
        Content = Group(VERTICAL)
        Content.Place(Text(self, self.name), border = (0,0,0,5))
        Content.Place(display)
        Content.Place(BTNDN, border = (0,0,5,5))
        # Draw decors
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        # done
        self._refresh()
        return

    def _refresh(self):
        for led, num in zip(self.leds, self.encoding[self.status]):
            for l in range(len(led)): led[l].SetValue(l==num)
        if self.instr:
            self.instr.write(self.VISA + " %d" % self.status)
        return

    def SetValue(self, value):
        self.status = value
        self._refresh()
        return

    def SetVisa(self, Instrument):
        self.instr = Instrument
        self.SetValue(int(self.instr.query(self.VISA+'?')))
        return

####################################################

class _slope(_single):

    def _init(self):
        self.name     = 'Slope'
        self.encoding = [[0],[1],[2],[3]]
        self.labels   = [['6dB', '12dB','18dB','24dB']]
        self.colour   = 'Blue'
        self.style    = 'Blank'
        self.VISA     = 'OFSL'
        return

    def _dn(self, event):
        self.status += 1
        if self.status > 3:
            self.status = 0
        self.SendEvent()
        self._refresh()
        return

####################################################

class _input(_single):

    def _init(self):
        self.name     = 'Input'
        self.encoding = [[0],[1],[2],[3]]
        self.labels   = [['A', 'A-B','I(1uA)','I(10nA)']]
        self.colour   = 'Blue'
        self.style    = 'Blank'
        self.VISA     = 'ISRC'
        return

    def _dn(self, event):
        self.status += 1
        if self.status > 3:
            self.status = 0
        self.SendEvent()
        self._refresh()
        return

####################################################

class _coupling(_single):

    def _init(self):
        self.name     = 'Coupling'
        self.encoding = [[0],[1]]
        self.labels   = [['AC', 'DC']]
        self.colour   = 'White'
        self.style    = 'Blank'
        self.VISA     = 'ICPL'
        return

    def _dn(self, event):
        self.status += 1
        if self.status > 1:
            self.status = 0
        self.SendEvent()
        self._refresh()
        return

####################################################

class _grounding(_single):

    def _init(self):
        self.name     = 'Grounding'
        self.encoding = [[0],[1]]
        self.labels   = [['FLOAT','GROUND']]
        self.colour   = 'White'
        self.style    = 'Blank'
        self.VISA     = 'IGND'
        return

    def _dn(self, event):
        self.status += 1
        if self.status > 1:
            self.status = 0
        self.SendEvent()
        self._refresh()
        return

####################################################

class _reserve(_single):

    def _init(self):
        self.name     = 'Reserve'
        self.encoding = [[0],[1],[2]]
        self.labels   = [['HIGH RESERVE', 'NORMAL', 'LOW NOISE']]
        self.colour   = 'Blue'
        self.style    = 'Blank'
        self.VISA     = 'RMOD'
        return

    def _dn(self, event):
        self.status += 1
        if self.status > 2:
            self.status = 0
        self.SendEvent()
        self._refresh()
        return

####################################################

class _filters(_single):

    def _init(self):
        self.name     = 'Filter'
        self.encoding = [[0],[1]]
        self.labels   = [['LINE', '2xLINE']]
        self.colour   = 'White'
        self.style    = 'Blank'
        self.VISA     = 'ILIN'
        return

    def _dn(self, event):
        self.status += 1
        if self.status > 3:
            self.status = 0
        self.SendEvent()
        self._refresh()
        return

    def _refresh(self):
        for l in range(len(self.leds[0])):
            self.leds[0][l].SetValue(((l+1)&self.status)>0) 
        if self.instr: self.instr.write(self.VISA + " %d" % self.status)
        return

####################################################

class _unlock(Control):

    def Start(self):
        # LOCAL
        self.status = 0
        self.instr = None
        # create led
        lib, libnam = Theme.GetImages('Round LED', 'Red')
        self.led = Display(self, lib, libnam)
        # create content
        Content = Group(VERTICAL)
        # make layout
        lbl = Text(self, 'Unlocked')
        Content.Place(lbl, border = (0,0,0,5))
        Content.Place(self.led)
        # Draw decors
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        # done
        self._refresh()
        return

    def _refresh(self):
        # bit 3 indicate overflow
        self.led.SetValue(self.status & 8 > 0)
        return

    def SetValue(self, value):
        self.status = value
        self._refresh()
        return

    def SetVisa(self, Instrument):
        pass

####################################################

class _overload(Control):

    def Start(self):
        # LOCAL
        self.status = 0
        self.instr  = None
        self.leds   = []
        self.colour = 'Red'
        # build display
        display = Group(HORIZONTAL)
        display.Place(MiniControl(self, ['Input', 'Filter', 'Output']))
        # create content
        Content = Group(VERTICAL)
        lbl = Text(self, 'Overload')
        Content.Place(lbl, border = (0,0,0,5))
        Content.Place(display)
        # Draw decors
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        # done
        self._refresh()
        return

    def _refresh(self):
        for i in range(len(self.leds[0])):
            flag = 1 << i
            self.leds[0][i].SetValue(self.status & flag > 0)
        return

    def SetValue(self, value):
        self.status = value
        self._refresh()
        return

    def SetVisa(self, Instrument):
        pass

####################################################

class _sync(Control):

    def Start(self):
        # control state
        self.status = 0
        self.instr = None
        # make button
        lib, libnam = Theme.GetImages('LED Switch', 'White')       
        self.BTNSW = Switch(self, lib, libnam)
        self.BTNSW.BindEvent(self._press)
        # create content
        Content = Group(VERTICAL)
        Content.Place(Text(self, 'Sync'))
        Content.Place(self.BTNSW, border=(0,0,10,10))
        # Draw decors
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        # done
        return

    def SetValue(self, value):
        self.status = value
        # reset switch status
        self.BTNSW.status = value
        self.BTNSW.Refresh()
        return

    def _press(self, event):
        self.status = event.status
        if self.instr: self.instr.write("SYNC %d" % event.status)
        self.SendEvent()
        return

    def SetVisa(self, Instrument):
        self.instr = Instrument
        self.SetValue(int(self.instr.query('SYNC?')))
        return

####################################################

class _phase(Control):

    def Start(self):
        self.instr = None
        # make digital display
        CTRL = Group(HORIZONTAL)
        # make format
        n = 3 # integer digits (Number of)
        d = 2 # decimal digits (Number of)
        self.format = f'%+0{n+d+2}.{d}f'
        # displays
        self.wheels = []        
        for char in list(self.format % 0):
            if char == '+':
                lib, Names = Theme.GetImages('Hex Sign', 'White')
                self.sign = Display(self, lib, Names) 
                CTRL.Place(self.sign)
            if char == '0':
                lib, nNames = Theme.GetImages('Hex Digit', 'Normal')
                lib, hNames = Theme.GetImages('Hex Digit', 'Hoover')
                wheel = Wheel(self, lib, nNames, hNames)
                wheel.BindEvent(self._update)
                CTRL.Place(wheel)
                self.wheels.append(wheel)
            if char == '.':
                lib, Names = Theme.GetImages('Hex Dot', 'White')
                CTRL.Place(Display(self, lib, Names))
        # make layout
        Content = Group(VERTICAL)
        Content.Place(Text(self, 'Phase'))
        Content.Place(CTRL, border = (5,15,5,5))
        # done
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        return

    def GetValue(self):
        # the number of integer digits is 3, thus
        # the most significant digit is 100 (start value of p)
        p, x = 1E2, 0 # Most Significant Digit, Accumulator
        for wheel in self.wheels:
            value = wheel.GetValue()
            x += wheel.GetValue()*p
            p /= 10 # shift to next decimal digit
        # Set sign
        if self.sign.GetValue() == 1: x = -x
        # re-format to round properly the return value
        return float(self.format % x)

    def SetValue(self, Value):
        wheeln = 0 # index pointer to current digit
        for char in list(self.format % Value):
            if char == '+': self.sign.SetValue(0); continue
            if char == '-': self.sign.SetValue(1); continue
            if char == '.': continue
            # get reference to current wheel
            wheel = self.wheels[wheeln]
            # set current wheel status
            wheel.SetValue(int(char))
            # set current wheel dynamics
            wheel.SetRotation([+1, -1][self.sign.GetValue()])
            # next index
            wheeln += 1
        # done
        self.status = Value
        return

    def SetVisa(self, Instrument):
        self.instr = Instrument
        X = self.instr.query('PHAS?')
        self.SetValue(float(X))
        return

    def _update(self, event):
        # get current value
        x = self.GetValue()
        # get reference to caller
        wheeln = self.wheels.index(event.caller)
        # get significant value
        # (for 3 integer digits and 2 decimal digits)
        sv = [100, 10, 1.0, 0.1, 0.01][wheeln]
        # get overflow
        overflow = event.caller.overflow
        # get sign
        sign = [+1, -1][self.sign.GetValue()]
        # correct overflow
        if overflow: x += overflow*sv*10*sign
        # coerce to 360 degrees
        if x < -179.99: x += 360.00
        if x > +180.00: x -= 360.00
        # update
        self.SetValue(x)
        if self.instr: self.instr.write("PHAS %.2f" % x)
        # done
        self.SendEvent()
        return

####################################################

class _signal(Control):

    def Start(self):
        self._init()
        self.instr = None
        # make digital display
        DISP = Group(HORIZONTAL)
        # make format
        n = 3 # integer digits (Number of)
        d = 4 # decimal digits (Number of)
        self.format = f'%+{n+d+2}.{d}f'
        # displays
        self.wheels = []        
        for char in list(f'%+0{n+d+2}.{d}fU'%0):
            if char == '+':
                lib, Names = Theme.GetImages('SR830 Sign',  'Red')
                self.sign = Display(self, lib, Names) 
                DISP.Place(self.sign)
            if char == '0':
                lib, Names = Theme.GetImages('SR830 Digit', 'Red')
                wheel = Display(self, lib, Names)
                DISP.Place(wheel)
                self.wheels.append(wheel)
            if char == '.':
                lib, Names = Theme.GetImages('SR830 Dot',   'Red')
                DISP.Place(Display(self, lib, Names))
            if char == 'U':
                lib, Names = Theme.GetImages('SR830 Unit',  'Red')
                self.unit = Display(self, lib, Names) 
                DISP.Place(self.unit)
        BAR = Group(HORIZONTAL)
        lib, Names = Theme.GetImages('SR830 Bar', 'Left')
        self.left = Display(self, lib, Names)
        BAR.Place(self.left)
        lib, Names = Theme.GetImages('SR830 Bar', 'Right')
        self.right = Display(self, lib, Names)
        BAR.Place(self.right)
        self.left.SetValue(4)
        self.right.SetValue(0)
        # make layout
        Content = Group(VERTICAL)
        Content.Place(Text(self, self.label))
        Content.Place(DISP, border = (5,15,5,5))
        Content.Place(BAR)
        # done
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        return

    def SetValue(self, Value):
        SENS = self.parent.CTRLS['SENSITIVITY']
        i, j, k = SENS.encoding[SENS.status]
        V = Value*1000**(k)  # scale Value to units
        I = float([5, 2, 1][i]*[100, 10, 1][j])/8.0 # Interval
        N = min(8, abs(round(V/I)))
        self.left.SetValue( N if V < 0 else 0)
        self.right.SetValue(N if V > 0 else 0)
        self.unit.SetValue(k)
        wheeln = 0 # index pointer to current digit
        for char in list(self.format % V):
            if char == '+': self.sign.SetValue(0); continue
            if char == '-': self.sign.SetValue(1); continue
            if char == '.': continue
            n = 10 if char == ' ' else int(char)
            wheel = self.wheels[wheeln]
            wheel.SetValue(n)
            wheeln += 1
        # done
        return

    def SetVisa(self, Instrument):
        pass

class _Vx(_signal):

    def _init(self):
        self.label = 'Vx'
        return

class _Vy(_signal):

    def _init(self):
        self.label = 'Vy'
        return
