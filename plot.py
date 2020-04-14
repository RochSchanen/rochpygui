# 'plot.py'
# content; classes for the plot interface.
# author; Roch schanen
# created; 2020 April 11
# repository; https://github.com/RochSchanen/rochpygui

# todo: rationalise the extra border EB
# todo: can we estimate the number of ticks and number
#       decimal digits from the span of the data set
# todo: Check refresh requirement when dynamic changes (limit, format, ...).

# wxpython: https://www.wxpython.org/
import wx

# numpy: https://numpy.org/
from numpy import exp

# LOCAL
from theme  import *
from graph  import *
from screen import *

###############################################################################
#################################### GraphicScreen ############################
###############################################################################

class GraphicScreen(Screen):

    def Start(self):
        # some defaults limits (to prevent singular expressions)
        xs, xe, ys, ye = -11.11, +11.11, -11.11, +11.11
        # create and setup graph for onPaint refresh:
        # (labels and titles)
        self.OnPaintGraph = Graph()
        self.OnPaintGraph.SetSize(self.GetSize())
        self.OnPaintGraph.SetLimit(xs, xe, ys, ye)
        self.OnPaintGraph.SetFont(Theme.GetFont())
        # again some default format to prevent singularities
        self.OnPaintGraph.SetXFormat([2, 2])
        self.OnPaintGraph.SetYFormat([2, 2])
        self.OnPaintGraph.StyleSet(DRAW_LABELS | DRAW_PLOTS)
        # setup screen
        W, H = self.GetSize()
        self.buffer   = wx.Bitmap(3*W, 3*H, wx.BITMAP_SCREEN_DEPTH)
        self.limit    = xs, xe, ys, ye
        self.origin   = W, H
        self.position = W,H
        # create and setup graph for drawing buffer:
        # (axis and grid)
        self.bufferGraph = Graph()
        self.bufferGraph.SetSize(self.buffer.GetSize())
        self.bufferGraph.SetLimit(xs, xe, ys, ye)
        self.bufferGraph.StyleSet(DRAW_AXIS | DRAW_GRID | DRAW_PLOTS)
        self.bufferGraph.StyleSet(SKIP_BORDERS)
        # set border
        self._setBorder()
        # setup drag tool:
        self.ToolSelect(_Drag(self))
        return

    def _setBorder(self):
        # get geometry
        W, H = self.GetSize()
        l, r, t, b = self._minBorder(self.OnPaintGraph)
        # set geometry
        self.bufferGraph.SetBorder(W+l, W+r, H+t, H+b)
        self.OnPaintGraph.SetBorder(l, r, t, b)
        self.clipArea = l, r, t, b
        # update
        self.RefreshBuffer()
        # done
        return

    def SetXLimit(self, Min, Max):
        xs, xe, ys, ye = self.limit
        self.limit = Min, Max, ys, ye
        # self.RefreshBuffer()
        # self.Refresh()
        return

    def SetYLimit(self, Min, Max):
        xs, xe, ys, ye = self.limit
        self.limit = xs, xe, Min, Max
        # self.RefreshBuffer()
        # self.Refresh()
        return

    def SetXLabel(self, s):
        self.OnPaintGraph.SetBottomTitle(s)
        self._setBorder()
        # self.Refresh()
        return

    def SetYLabel(self, s):
        self.OnPaintGraph.SetLeftTitle(s)
        self._setBorder()
        # self.Refresh()
        return

    def SetXFormat(self, N = None, D = None):
        n, d = self.OnPaintGraph.xFormat
        if N: n = N
        if D: d = D
        self.OnPaintGraph.SetXFormat([n, d])
        # self._setBorder()
        self.RefreshBuffer()
        # self.Refresh()
        return

    def SetYFormat(self, N = None, D = None):
        n, d = self.OnPaintGraph.yFormat
        if N: n = N
        if D: d = D
        self.OnPaintGraph.SetYFormat([n, d])
        self._setBorder()
        self.RefreshBuffer()
        # self.Refresh()
        return

    def SetXTicks(self, n):
        nx, ny = self.OnPaintGraph.ticks
        self.OnPaintGraph.ticks = n, ny
        self.bufferGraph.ticks = n, ny
        self.RefreshBuffer()
        # self.Refresh()
        return

    def SetYTicks(self, n):
        nx, ny = self.OnPaintGraph.ticks
        self.OnPaintGraph.ticks = nx, n
        self.bufferGraph.ticks = nx, n
        self.RefreshBuffer()
        # self.Refresh()
        return

    def _minBorder(self, graph):
        ln10 = 2.3025850929940459
        # a dummy dc client is required to get text extent
        dc = wx.ClientDC(self)
        dc.SetFont(graph.font)
        # get label size
        n, d = graph.yFormat                    # integers and decimals digits
        f = f'%.{d}f'                           # get format string
        v = -(exp(ln10*(n+d))-1)/exp(ln10*(d))  # get value with maximum characters
        Wy, H = dc.GetTextExtent(f % v)         # get height (format independent)
        # reserve space for labels
        l, r, t, b = Wy, Wy, H, H 
        # add extra border EB (for readablity of the left and right labels)
        l, r = l + graph.EB, r + graph.EB   
        # reserve space for labels:
        if graph.leftText:   l += H
        if graph.bottomText: b += H
        # done
        return l, r, t, b

    def _getNewLimit(self):
        xs, xe, ys, ye = self.limit
        ax, bx, ay, by = self.OnPaintGraph.scale
        X1, Y1 = self.origin
        X2, Y2 = self.position
        dx, dy = (X2-X1)/ax, (Y2-Y1)/ay
        xs, xe, ys, ye = xs+dx, xe+dx, ys+dy, ye+dy 
        return xs, xe, ys, ye

    def RefreshBuffer(self):
        self.limit = self._getNewLimit() # get new limit
        self.position = self.origin      # reset buffer position
        dc = wx.MemoryDC()               # setup device context
        dc.SelectObject(self.buffer)     # select buffer
        dc.SetBackground(wx.Brush(wx.Colour(0,0,0)))
        dc.Clear()
        xs, xe, ys, ye = self.limit
        self.bufferGraph.SetLimit(xs, xe, ys, ye)
        self.bufferGraph.Draw(dc)
        dc.SelectObject(wx.NullBitmap)   # release device context
        return

    def onPaint(self, dc):
        xs, xe, ys, ye = self._getNewLimit()
        self.OnPaintGraph.SetLimit(xs, xe, ys, ye)
        self.OnPaintGraph.Draw(dc)
        return

class _Drag(ScreenDragBuffer):

    # superseed the previous _unlock() method to provide
    # a RefreshBuffer() at the end of the drag event
    def _unlock(self, event):
        if self.lock:
            self.scr.RefreshBuffer()            
            self.lock = False
        return
