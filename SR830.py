# "SR830.py"
# content; SR830 interface.
# author; Roch schanen
# created; 2020 April 19
# repository; https://github.com/RochSchanen/rochpygui

# todo: rationalise the extra border EB
# todo: can we estimate the number of ticks and number
#       decimal digits from the span of the data set
# todo: Check refresh requirement when dynamic changes (limit, format, ...).

# wxpython: https://www.wxpython.org/
import wx

# numpy: https://numpy.org/
# from numpy import exp, inf, where
# from numpy import exp, log, floor, sqrt

# LOCAL
from theme    import *
from layout   import *
from controls import *
from display  import *
from buttons  import *

TIMER_DELAY_OVERLOAD = 500
TIMER_DELAY_UNLOCK   = 500
TIMER_DELAY_SNAP     = 500

####################################################

class _panel(Control):

    def Start(self):
        # Create Controls
        self.SENSITIVITY  = _sensitivity(self)
        self.TIMECONSTANT = _timeConstant(self)
        self.INPUT     = _input(self)
        self.SLOPE     = _slope(self)
        self.RESERVE   = _reserve(self)
        self.SYNC      = _sync(self)
        self.COUPLING  = _coupling(self)
        self.GROUNDING = _grounding(self)
        self.FILTERS   = _filters(self)
        self.OVERLOAD  = _overload(self)
        self.UNLOCK    = _unlock(self)
        # PHASE = Phase(self, w=143, h=54)
        # self.VX   = DigitalDisplay(self, SENSITIVITY, name = "Vx", w=132)
        # self.VY   = DigitalDisplay(self, SENSITIVITY, name = "Vy", w=131)
        # Place Controls
        h1 = Group(HORIZONTAL)
        h1.Place(self.TIMECONSTANT, decoration = 'Groove')
        h1.Place(self.SENSITIVITY, decoration = 'Groove')
        v1 = Group(VERTICAL)
        v1.Place(self.OVERLOAD, decoration = 'Groove')
        v1.Place(self.UNLOCK, decoration = 'Groove')
        h1.Place(v1)
        h2 = Group(HORIZONTAL)
        h2.Place(self.INPUT, decoration = 'Groove')
        h2.Place(self.SLOPE, decoration = 'Groove')
        h2.Place(self.RESERVE, TOP, decoration = 'Groove')
        h5 = Group(HORIZONTAL)
        # h5.Place(PHASE)
        h5.Place(self.SYNC, decoration = 'Groove')
        h3 = Group(HORIZONTAL)
        h3.Place(self.COUPLING, decoration = 'Groove')
        h3.Place(self.GROUNDING, decoration = 'Groove')
        h3.Place(self.FILTERS, decoration = 'Groove')
        # h4 = Group(HORIZONTAL)
        # h4.Place(self.VX)
        # h4.Place(self.VY)
        Content = Group(VERTICAL)
        Content.Place(Text(self, 'SR830'))
        Content.Place(h1)
        # Content.Place(h4, decoration = 'Groove')
        Content.Place(h2)
        Content.Place(h5)
        Content.Place(h3)
        # Expanding
        Content.Expand()
        h1.Expand()
        v1.Expand()
        h2.Expand()
        h3.Expand()
        # h4.Expand()
        h5.Expand()
        # draw decorations
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        # Bindings
        self.SENSITIVITY.BindEvent(self._sensitivity)
        self.TIMECONSTANT.BindEvent(self._timeconstant)
        self.INPUT.BindEvent(self._input)
        self.SLOPE.BindEvent(self._slope)
        self.RESERVE.BindEvent(self._reserve)
        self.SYNC.BindEvent(self._sync)
        self.COUPLING.BindEvent(self._coupling)
        self.GROUNDING.BindEvent(self._grounding)
        self.FILTERS.BindEvent(self._filters)
        # PHASE.BindEvent(self._phase)
        # PHASE.SetValue(float(VISA.query('PHAS?')))
        return

    def SetVisa(self, Instrument):

        self.instr = Instrument

        self.SENSITIVITY.SetValue(int(self.instr.query('SENS?')))
        self.TIMECONSTANT.SetValue(int(self.instr.query('OFLT?')))
        self.INPUT.SetValue(int(self.instr.query('ISRC?')))
        self.SLOPE.SetValue(int(self.instr.query('OFSL?')))
        self.RESERVE.SetValue(int(self.instr.query('RMOD?')))
        self.SYNC.SetValue(int(self.instr.query('SYNC?')))
        self.COUPLING.SetValue(int(self.instr.query('ICPL?')))
        self.GROUNDING.SetValue(int(self.instr.query('IGND?')))
        self.FILTERS.SetValue(int(self.instr.query('ILIN?')))

        self.UNLOCK.SetVisa(Instrument)
        self.OVERLOAD.SetVisa(Instrument)

        return

    # def _onTimer(self, event):
    #     # s = self.VISA.query("SNAP?1,2")
    #     # X = float(s[:s.find(',')])
    #     # Y = float(s[s.find(',')+1:])
    #     # self.VX.SetValue(X)
    #     # self.VY.SetValue(Y)
    #     i = int(self.VISA.query("LIAS?"))
    #     self.OVERLOAD.SetValue(i)
    #     self.UNLOCK.SetValue(i)
    #     return

    # def _phase(self, event):
    #   self.instr.write("PHAS %.2f" % event.status)
    #   return

    def _sensitivity(self, event):
      self.instr.write("SENS %d" % event.status)
    def _timeconstant(self, event):
      self.instr.write("OFLT %d" % event.status)
    def _input(self, event):
      self.instr.write("ISRC %d" % event.status)
    def _slope(self, event):
      self.instr.write("OFSL %d" % event.status)
    def _reserve(self, event):
      self.instr.write("RMOD %d" % event.status)
    def _sync(self, event):
      self.instr.write("SYNC %d" % event.status)
    def _coupling(self, event):
      self.instr.write("ICPL %d" % event.status)
    def _grounding(self, event):
      self.instr.write("IGND %d" % event.status)
    def _filters(self, event):
      self.instr.write("ILIN %d" % event.status)

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
        # displays
        self.leds = []
        # style
        self.colour = 'White'
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
        Content.Place(Text(self, 'Sensitivity'))
        Content.Place(buttons, border = (0,0,10,10))
        Content.Place(display)
        # Draw decors
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        # done
        self._refresh()
        return

    # set led values according to the status value
    def _refresh(self):
        for led, num in zip(self.leds, self.encoding[self.status]):
            for l in range(len(led)): led[l].SetValue(l==num)
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
        # displays
        self.leds = []
        # style
        self.colour = 'White'
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
        Content.Place(Text(self, 'Time Constant'))
        Content.Place(buttons, border = (0,0,10,10))
        Content.Place(display)
        # Draw decors
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        # done
        self._refresh()
        return

    def _refresh(self):
        for led, num in zip(self.leds, self.encoding[self.status]):
            for l in range(len(led)): led[l].SetValue(l==num)
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
        Content.Place(Text(self, self.name))
        Content.Place(BTNDN, border = (0,0,10,10))
        Content.Place(display)
        # Draw decors
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        # done
        self._refresh()
        return

    def _refresh(self):
        for led, num in zip(self.leds, self.encoding[self.status]):
            for l in range(len(led)): led[l].SetValue(l==num)
        return

    def SetValue(self, value):
        self.status = value
        self._refresh()
        return

####################################################

class _slope(_single):

    def _init(self):
        self.name     = 'Slope'
        self.encoding = [[0],[1],[2],[3]]
        self.labels   = [['6dB', '12dB','18dB','24dB']]
        self.colour   = 'White'
        self.style    = 'Blank'
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
        self.colour   = 'White'
        self.style    = 'Blank'
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
        return

    def _dn(self, event):
        self.status += 1
        if self.status > 1:
            self.status = 0
        self.SendEvent()
        self._refresh()
        return

####################################################

class _sync(_single):

    def _init(self):
        self.name     = 'Sync'
        self.encoding = [[0],[1]]
        self.labels   = [['SYNC']]
        self.colour   = 'White'
        self.style    = 'Blank'
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
        self.colour   = 'White'
        self.style    = 'Blank'
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
        return

####################################################

class _unlock(Control):

    def Start(self):
        # LOCAL
        self.status = 0
        self.instr  = None
        # create led
        lib, libnam = Theme.GetImages('Round LED', 'Red')
        self.led = Display(self, lib, libnam)
        # create content
        Content = Group(VERTICAL)
        # make layout
        lbl = Text(self, 'Unlocked')
        Content.Place(lbl)
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
        # LOCAL
        self.instr = Instrument
        # TIMER
        self.Timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._onTimer, self.Timer)
        self.Timer.Start(TIMER_DELAY_UNLOCK)
        return

    def _onTimer(self, event):
        if self.instr:
            self.SetValue(int(self.instr.query("LIAS?")))
        return

####################################################

class _overload(Control):

    def Start(self):
        # LOCAL
        self.status  = 0
        self.leds    = []
        self.colour = 'Red'
        # build display
        display = Group(HORIZONTAL)
        display.Place(MiniControl(self, ['Input', 'Filter', 'Output']))
        # create content
        Content = Group(VERTICAL)
        lbl = Text(self, 'Overload')
        Content.Place(lbl)
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
        # LOCAL
        self.instr = Instrument
        # TIMER
        self.Timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._onTimer, self.Timer)
        self.Timer.Start(TIMER_DELAY_OVERLOAD)
        return

    def _onTimer(self, event):
        if self.instr:
            self.SetValue(int(self.instr.query("LIAS?")))
        return
