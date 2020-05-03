# 'controls.py'
# content; The Control class.
# author; Roch schanen
# created; 2020 April 03
# repository; https://github.com/RochSchanen/rochpygui

# todo: check whether the wx.Control class should be raplaced by panels
# todo: change self.evt to local evt. it is only used once to bind event object

# wxpython: https://www.wxpython.org/
import wx

from theme   import *
from layout  import *
from display import *

class Control(wx.Control):
    # superseed __init__()
    def __init__(
        self,
        parent):
        # call parent __init__()
        wx.Control.__init__(
            self,
            parent      = parent,
            id          = wx.ID_ANY,
            pos         = wx.DefaultPosition,
            size        = wx.DefaultSize,
            style       = wx.NO_BORDER,
            validator   = wx.DefaultValidator,
            name        = "")
        # PARAMETERS
        self.parent = parent
        # LOCAL DEFAULTS
        self.status = 0
        self.BackgroundBitmap = None
        self.ctr, self.evt = None, None
        # DEFAULT BACKGROUND
        self.SetBackgroundColour(BackgroundColour)
        # BINDINGS
        self.Bind(wx.EVT_ERASE_BACKGROUND,self._onEraseBackground)
        self.Bind(wx.EVT_PAINT,self._onPaint)
        # user constructor
        self.Start()
        # done
        return

    # to be superseeded
    def Start(self):
        return

    def _onEraseBackground(self, event):
        # no operation (reduced flicker)
        pass 

    def _onPaint(self, event):
        if self.BackgroundBitmap:
            dc = wx.BufferedPaintDC(self)
            dc.DrawBitmap(self.BackgroundBitmap, 0, 0)
        return

    def BindEvent(self, handler):
        self.ctr, self.evt = wx.lib.newevent.NewEvent()
        self.GetParent().Bind(self.evt, handler)
        return

    def SendEvent(self):
        if self.ctr:
            event = self.ctr(caller=self, status = self.status)
            wx.PostEvent(self.GetParent(), event)
        return
