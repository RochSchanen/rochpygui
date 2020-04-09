# 'display.py'
# content; Simple display classes.
# author; Roch schanen
# created; 2020 April 02
# repository; https://github.com/RochSchanen/rochpygui

# wxpython: https://www.wxpython.org/
import wx

from theme import *

class Display(wx.Control):

    def __init__(
        self,
        parent,
        pnglib,
        names):

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
        # the set of images is defined by a name list
        self.names  = names
        # load the whole set of images:
        self.pngs   = pnglib.Get(names)

        # LOCAL
        # status is an index or a name
        self.status = 0

        # get png size from first image
        w, h = self.pngs[self.status].GetSize()
        self.SetSize((w, h))

        # set background color
        self.SetBackgroundColour(BackgroundColour)

        # BINDINGS
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._onEraseBackground)
        self.Bind(wx.EVT_PAINT, self._onPaint)

        return

    def _onEraseBackground(self, event):
        # no operation (reduced flicker)
        pass 

    def _onPaint(self, event):
        v = self.status
        if isinstance(v, int): n = v
        if isinstance(v, str): n = self.names.index(v)
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.pngs[n], 0, 0)
        return

    def SetValue(self, Value):
        self.status = Value
        self.Refresh()
        return

    def GetValue(self):
        return self.status

class Text(wx.StaticText):

    def __init__(self, parent, text):

        wx.StaticText.__init__(self,
            parent = parent,
            label  = text,
            id     = wx.ID_ANY,
            pos    = wx.DefaultPosition,
            size   = wx.DefaultSize,
            style  = wx.NO_BORDER,
            name   = wx.TextCtrlNameStr)

        self.SetForegroundColour(TextColour)
        self.SetBackgroundColour(BackgroundColour)

        return
