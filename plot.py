# 'plot.py'
# content; classes for the plot interface.
# author; Roch schanen
# created; 2020 April 11
# repository; https://github.com/RochSchanen/rochpygui

# wxpython: https://www.wxpython.org/
import wx

# LOCAL
from theme  import *
from graph  import *
from screen import *

###############################################################################
#################################### PLOT #####################################
###############################################################################

class Plot(Screen):

    def Start(self):

        # SET DEFAULTS:

        # get font style
        font = Theme.GetFont()
        # set label format
        LabelFormat = {"x": [3, 2], "y": [3, 2]}
        # set default limits
        xs, xe, ys, ye = -11.32, +10.17, -10.13, +10.38

        # get label maximum label size
        dc = wx.ClientDC(self)
        dc.SetFont(font)
        ln10 = 2.3025850929940459
        n, d = LabelFormat['x']                # length, decimals
        f = f'%.{d}f'                          # get format string
        v = -(exp(ln10*(n+d))-1)/exp(ln10*(d)) # get maximum value
        Width, tmp = dc.GetTextExtent(f % v)   # get width
        n, d = LabelFormat['y']                # length, decimals
        f = f'%.{d}f'                          # get format string
        v = -(exp(ln10*(n+d))-1)/exp(ln10*(d)) # get maximum value
        tmp, Height = dc.GetTextExtent(f % v)  # get height

        # SETUP SCREEN:

        # border area
        l, r, t, b = Width, Width, Height, Height   # label
        l, r, t, b = l+20, r+20, t+20, b+20         # extra
        self.clipArea  = l, r, t, b
        # buffer
        W, H = self.Size
        w, h = W-l-r, H-t-b
        self.buffer = wx.Bitmap(3*w, 3*h, wx.BITMAP_SCREEN_DEPTH)
        # origin
        self.origin = w-l, h-t
        self.position = self.origin
        # limits
        self.limit = xs, xe, ys, ye

        # SETUP GRAPH:

        # create and setup graph for drawing buffer:
        g = Graph()
        g.SetSize(self.buffer.GetSize())
        g.SetBorder(w, w, h, h)
        g.SetLimit(xs, xe, ys, ye)
        g.StyleSet(DRAW_AXIS | DRAW_GRID)
        g.StyleSet(SKIP_BORDERS)

        self.bufferGraph = g

        # create and setup graph for onPaint refresh:
        g = Graph()
        g.SetSize(self.GetSize())
        g.SetBorder(l, r, t, b)
        g.SetLimit(xs, xe, ys, ye)
        g.StyleSet(DRAW_BOX | DRAW_LABELS)
        g.SetFont(font)
        g.SetFormat(LabelFormat)

        self.OnPaintGraph = g

        # DRAW BUFFER
        self.RefreshBuffer()

        # SETUP DRAG TOOL:

        self.ToolSelect(Drag(self))

        return

    def _getNewLimit(self):
        xs, xe, ys, ye = self.limit
        ax, bx, ay, by = self.OnPaintGraph.scale
        X1, Y1 = self.origin
        X2, Y2 = self.position
        dx, dy = (X2-X1)/ax, (Y2-Y1)/ay
        xs, xe, ys, ye = xs+dx, xe+dx, ys+dy, ye+dy 
        return xs, xe, ys, ye

    def RefreshBuffer(self):
        # get new limit
        self.limit = self._getNewLimit()
        # reset buffer position
        self.position = self.origin
        # draw new buffer
        dc = wx.MemoryDC()      
        dc.SelectObject(self.buffer)
        # clear buffer
        dc.SetBackground(wx.Brush(wx.Colour(0,0,0)))
        dc.Clear()
        # draw graph
        xs, xe, ys, ye = self.limit
        self.bufferGraph.SetLimit(xs, xe, ys, ye)
        self.bufferGraph.Draw(dc)
        # and release device context
        dc.SelectObject(wx.NullBitmap)
        return

    def onPaint(self, dc):
        xs, xe, ys, ye = self._getNewLimit()
        self.OnPaintGraph.SetLimit(xs, xe, ys, ye)
        self.OnPaintGraph.Draw(dc)
        return

class Drag(ScreenDragBuffer):

    # overload _umlock method to add RefreshBuffer()
    def _unlock(self, event):
        if self.lock:
            self.scr.RefreshBuffer()            
            self.lock = False
        return
