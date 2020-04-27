# 'buttons.py'
# content; Simple button classes.
# author; Roch schanen
# created; 2020 April 03
# repository; https://github.com/RochSchanen/rochpygui

# wxpython: https://www.wxpython.org/
import wx
import wx.lib.newevent

# LOCAL IMPORTS
from display  import Display
from controls import Control
from layout   import *

####################################################

# root class for buttons
class _btn(Display):

    def __init__(
        self,
        parent,
        pnglib,
        names):

        Display.__init__(
            self,
            parent = parent,
            pnglib = pnglib,
            names  = names)

        # LOCALS
        self.radio = None
        self.ctr   = None
        self.evt   = None

        # BINDINGS
        self.Bind(wx.EVT_LEFT_DOWN,   self._onMouseDown)
        self.Bind(wx.EVT_LEFT_DCLICK, self._onMouseDown)
        # capture double clicks events as secondary single clicks

        self._start()

        return

    def _start(self):
        pass

    # radio feature
    def _clear(self):
        pass

    # on EVT_LEFT_DOWN, the event.skip()
    # method must be called to preserve
    # the focus event to be processed
    def _onMouseDown(self, event):
        event.Skip() # allow focus events
        return

    # Bind the event to the parent handler
    def BindEvent(self, handler):
        # "handler" is a reference to a function defined by the parent
        self.ctr, self.evt = wx.lib.newevent.NewEvent()
        self.GetParent().Bind(self.evt, handler)
        return

    # Sends a event to parent using "status" as parameter
    def SendEvent(self):
        if self.ctr:
            event = self.ctr(caller=self, status=self.status)
            wx.PostEvent(self.GetParent(), event)
        return

####################################################

# send event on mouse_down()
class Push(_btn):

    def _start(self):
        self.lock = False
        self.Bind(wx.EVT_LEFT_UP,      self._onMouseUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._onMouseLeave)
        return

    def _onMouseDown(self, event):
        event.Skip() # allow focus events
        self.lock = True
        if self.radio:
            self.radio.Select(self)
        self.status = 1
        self.Refresh()
        self.SendEvent()
        return

    def _onMouseUp(self, event):
        if self.lock:
            self.lock = False
            self.status = 0
            self.Refresh()
        return

    def _onMouseLeave(self, event):
        if self.lock:
            self.lock = False
            self.status = 0
            self.Refresh()
        return

####################################################

# send event on release
class Switch(_btn):

    def _start(self):
        self.lock = False
        self.Bind(wx.EVT_LEFT_UP, self._onMouseUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._onMouseLeave)
        return

    def _onMouseDown(self, event):
        event.Skip() # allow focus events
        self.lock = True
        if self.radio:
            self.radio.Select(self)
        self.status |= 2
        self.Refresh()
        return

    def _onMouseUp(self, event):
        if self.lock:
            self.lock = False
            self.status &= 1
            self.status ^= 1
            self.Refresh()
            self.SendEvent()
        return

    def _onMouseLeave(self, event):
        if self.lock:
            self.lock = False
            self.status &= 1
            self.Refresh()
        return

    # called by radio group
    def _clear(self):
        if self.status:
            self.status = 0
            self.Refresh()
            self.SendEvent()
        return

####################################################

# send event on mouse_down()
class Radio(_btn):

    def _onMouseDown(self, event):
        event.Skip() # allow focus events
        if self.radio:
            self.radio.Select(self)
        if not self.status:
            self.status = 1     
            self.Refresh()
            self.SendEvent()
        return

    # called by a radio group to deselect self
    def _clear(self):
        if self.status:
            self.status = 0
            self.Refresh()
            self.SendEvent()
        return

class RadioCollect():

    def __init__(self, btns):
        self.btns = btns
        for b in self.btns:
            b.radio = self
        return

    def Select(self, btn):
        for b in self.btns:
            if b is not btn:
                b._clear()
        return

####################################################

class Wheel(Display):

    def __init__(
        self,
        parent,
        pnglib,
        Normal,
        Hoover = []):
        # call parent class __init__()
        Display.__init__(
            self,
            parent = parent,
            pnglib = pnglib,
            names  = Normal + Hoover)
        # LOCALS
        self.rotation = +1   # inverse rotation
        self.reset = None # cancel operation
        # "hoover length" should be zero or
        # the same as "Normal length"
        self.l = len(Normal), len(Hoover)
        self.radio = None # radio group handle
        self.ctr   = None # 
        self.evt   = None
        self.overflow = 0
        # BINDINGS
        self.Bind(wx.EVT_ENTER_WINDOW, self._onMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._onMouseLeave)
        self.Bind(wx.EVT_MOUSEWHEEL,   self._onMouseWheel)
        return

    def _onMouseEnter(self, event):
        # event.Skip()
        ln, lh = self.l
        # coerce to normal
        m = self.status % ln
        # upgrade to hoover
        m += ln if lh else 0
        # update state
        self.status = m
        # done
        self.Refresh()
        return

    def _onMouseLeave(self, event):
        ln, lh = self.l
        # coerce to normal
        m = self.status % ln
        # update state
        self.status = m
        # done
        self.Refresh()
        return

    def _onMouseWheel(self, event):
        # save state if cancellation
        self.reset = self.status
        self.overflow = 0
        # get parameters
        ln, lh = self.l
        m = self.status % ln
        # apply wheel action
        r = event.GetWheelRotation()        
        if r > 0: m += self.rotation
        if r < 0: m -= self.rotation
        # set overflow flag
        if m < 0   : self.overflow = -1
        if m > ln-1: self.overflow = +1
        # coerce (when overflow)
        m %= ln
        # upgrade to hoover
        m += ln if lh else 0
        # update state
        self.status = m
        # done
        self.Refresh()
        self.SendEvent()
        return

    # sign value is +1 or -1
    def SetRotation(self, Value):
        self.rotation = Value
        return

    def SetValue(self, Value):
        # get parameters
        ln, lh = self.l
        # get value
        m = int(Value)
        if self.status > ln-1: m += ln 
        # update
        self.status = m
        self.reset  = m
        self.Refresh()
        return

    def GetValue(self):
        # get parameters
        ln, lh = self.l
        return self.status % ln

    def Reset(self):
        self.status = self.reset
        self.Refresh()
        return

    # Bind the event to the parent handler
    def BindEvent(self, handler):
        # "handler" is a reference to a function defined by the parent
        self.ctr, self.evt = wx.lib.newevent.NewEvent()
        self.GetParent().Bind(self.evt, handler)
        return

    # Sends a event to parent using "status" as parameter
    def SendEvent(self):
        if self.ctr:
            event = self.ctr(caller=self, status=self.status)
            wx.PostEvent(self.GetParent(), event)
        return
