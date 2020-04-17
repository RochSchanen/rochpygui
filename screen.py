# 'screen.py'
# content; classes for the plot interface.
# author; Roch schanen
# created; 2020 April 11
# repository; https://github.com/RochSchanen/rochpygui

# wxpython: https://www.wxpython.org/
import wx

# numpy: https://numpy.org/
from numpy import exp, log10, floor, ceil, linspace

# LOCAL
from theme import *

###############################################################################
################################### SCREEN ####################################
###############################################################################

class Screen(wx.Control):

    def __init__(self, Parent, Width, Height):

        wx.Control.__init__(
            self,
            parent      = Parent,
            id          = wx.ID_ANY,
            pos         = wx.DefaultPosition,
            size        = wx.DefaultSize,
            style       = wx.NO_BORDER,
            validator   = wx.DefaultValidator,
            name        = "")

        # PARAMETERS
        self.parent = Parent

        # LOCAL
        self.tool       = None
        self.buffer     = None
        self.position   = 0, 0
        self.clipArea   = 0, 0, 0, 0

        # set geometry
        self.SetSize((Width, Height))

        # call user-defined constructor     
        self.Start()

        # bind events
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._onEraseBackground) 
        self.Bind(wx.EVT_PAINT, self._onPaint)

        # done
        return

    # Called by the OS
    def _onEraseBackground(self, event):
        # this is supposed to reduce flicker
        pass

    # Called by the OS or by a user Refresh():
    def _onPaint(self, event):
        # create device context
        # for the _onPaint() method
        dc = wx.BufferedPaintDC(self)
        # clear

        dc.SetBackground(wx.Brush(BackgroundColour))
        dc.Clear() # clear everything for the moment
        # todo: might want to clear selectively. maybe.

        # draw
        if self.buffer:
            # get clip geometry
            l, r, t, b = self.clipArea
            x, y = self.position
            w, h = self.GetSize()
            W, H = self.buffer.GetSize()
            # get clip image
            X, Y, P, Q = x+l, y+t, w-l-r, h-t-b
            # bitmap partially or fully uncovered
            if X < 0: P += X; X = 0; l = -x
            if Y < 0: Q += Y; Y = 0; t = -y
            if (X+P) > W: P = W-X
            if (Y+Q) > H: Q = H-Y
            # bitmap partially covered
            if P>0 and Q>0:
                r = wx.Rect(X, Y, P, Q)
                clip = self.buffer.GetSubBitmap(r)
                dc.DrawBitmap(clip, l, t)

        # more drawings
        self.onPaint(dc)

        # additional painting features from the selected tool
        if self.tool: self.tool.onPaint(dc)

        # It is not required to release
        # the DC object when BufferedPaintDC()
        # is used in the onPaint() method:
        # done
        return

    def ToolSelect(self, newTool):
        if self.tool: self.tool.Deselect()
        self.tool = newTool
        newTool.Select()
        self.Refresh()
        return

    # user defined constructor
    def Start(self):
        pass

    # additional painting features (most likely on the border area)
    def onPaint(self, dc):
        pass

###############################################################################
#################################### TOOLS ####################################
###############################################################################

# generic class for creating tools
class ScreenTool():

    def __init__(self, Screen):
        self.scr = Screen
        self.Start()
        return

    # user constructor
    def Start(self):
        pass

    # more drawing from selected tool
    def onPaint(self, dc):
        pass

    # self select method
    def Select(self):
        # Bind Screen events to this tool handler methods
        self.scr.Bind(wx.EVT_LEFT_DOWN,     self._LeftDown)
        self.scr.Bind(wx.EVT_MOTION,        self._Motion)
        self.scr.Bind(wx.EVT_LEFT_UP,       self._LeftUp)
        self.scr.Bind(wx.EVT_LEAVE_WINDOW,  self._Leave)
        return

    # self deselect method
    def Deselect(self):
        # Unbind Screen events to this tool handler methods
        self.scr.Unbind(wx.EVT_LEFT_DOWN)
        self.scr.Unbind(wx.EVT_MOTION)
        self.scr.Unbind(wx.EVT_LEFT_UP)
        self.scr.Unbind(wx.EVT_LEAVE_WINDOW)
        return

    def _Leave(self, event):
        pass

###############################################################################
#################################### DRAG TOOL ################################
###############################################################################

# basic drag tool
class ScreenDragBuffer(ScreenTool):

    def Start(self):
        self.lock = False
        return

    # todo: no drag from the border
    def _LeftDown(self, event):
        self.lock = True        
        self.MouseStart  = event.GetPosition()
        self.scrStart = self.scr.position
        return

    # todo: no drag further than the border
    def _Motion(self, event):
        if self.lock:
            # get parameters
            x, y = event.GetPosition()
            X, Y = self.MouseStart
            p, q = self.scrStart
            # update buffer position
            P, Q = p+X-x, q+Y-y
            # set postition
            self.scr.position = P, Q
            # invoque the _onPaint method
            self.scr.Refresh()
        return

    def _LeftUp(self, event):
        self._unlock(event)
        return

    def _Leave(self, event):
        self._unlock(event)
        return

    def _unlock(self, event):
        if self.lock:
            self.lock = False
        return
