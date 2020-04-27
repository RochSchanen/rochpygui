# 'controls.py'
# content; The Control class.
# author; Roch schanen
# created; 2020 April 03
# repository; https://github.com/RochSchanen/rochpygui

# wxpython: https://www.wxpython.org/
import wx

from theme   import *
from layout  import *
from display import *

class Control(wx.Control):

    def __init__(
        self,
        parent):

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

        return

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
