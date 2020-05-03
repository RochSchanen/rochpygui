# 'plot.py'
# content; classes for the plot interface.
# author; Roch schanen
# created; 2020 April 11
# repository; https://github.com/RochSchanen/rochpygui

# todo: rationalise the extra border EB
# todo: can we estimate the number of ticks and number
#       decimal digits from the span of the data set
# todo: Check refresh requirement when dynamic changes (limit, format, ...).
# todo: Xfit and Yfit give an error when there is no data, fix it.

# wxpython: https://www.wxpython.org/
import wx

# numpy: https://numpy.org/
from numpy import exp, inf, where

# LOCAL
from theme    import *
from display  import *
from graph    import *
from layout   import *
from screen   import *
from controls import *
from buttons  import *

###############################################################################
#################################### GRAPH SCREEN #############################
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
        self.OnPaintGraph.StyleSet(DRAW_PLOTS | DRAW_LABELS)
        # self.OnPaintGraph.StyleSet(DRAW_LABEL_LEFT | DRAW_LABEL_BOTTOM)
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
        return

    def AddPlot(self):
        p = self.OnPaintGraph.AddPlot()
        return p

    def AddBufferedPlot(self):
        p = self.bufferGraph.AddPlot()
        return p

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

###############################################################################
################################ INTERACTIVE GRAPH ############################
###############################################################################

class InteractiveGraph(Control):

    def Start(self):
        # create plot
        self.Graph = GraphicScreen(self, 600, 600)
        # build tool bar:
        ToolBar = Group(VERTICAL)
        # measure
        self.MeasureTool = _Measure(self.Graph)
        lib, names = Theme.GetImages('Graph','Measure')
        MEASURE = Switch(self, lib, names)
        MEASURE.BindEvent(self.MeasureEvent)
        ToolBar.Place(MEASURE)
        # drag
        self.DragTool = _Drag(self.Graph)
        lib, names = Theme.GetImages('Graph','Drag')
        DRAG = Switch(self, lib, names)
        DRAG.BindEvent(self.DragEvent)
        ToolBar.Place(DRAG)
        # expand
        self.ExpandTool = _Expand(self.Graph)
        lib, names = Theme.GetImages('Graph','Expand')
        EXPAND = Switch(self, lib, names)
        EXPAND.BindEvent(self.ExpandEvent)
        ToolBar.Place(EXPAND)
        # X expand
        self.XExpandTool = _XExpand(self.Graph)
        lib, names = Theme.GetImages('Graph','X Expand')
        XEXPAND = Switch(self, lib, names)
        XEXPAND.BindEvent(self.XExpandEvent)
        ToolBar.Place(XEXPAND)
        # Y expand
        self.YExpandTool = _YExpand(self.Graph)
        lib, names = Theme.GetImages('Graph','Y Expand')
        YEXPAND = Switch(self, lib, names)
        YEXPAND.BindEvent(self.YExpandEvent)
        ToolBar.Place(YEXPAND)
        # shrink
        lib, names = Theme.GetImages('Graph','Shrink')
        SHRINK = Push(self, lib, names)
        SHRINK.BindEvent(self.ShrinkEvent)
        ToolBar.Place(SHRINK)
        # Yfit tool
        lib, names = Theme.GetImages('Graph','Yfit')
        YFIT = Switch(self, lib, names)
        YFIT.BindEvent(self.YfitEvent)
        ToolBar.Place(YFIT)
        # Xfit tool
        lib, names = Theme.GetImages('Graph','Xfit')
        XFIT = Switch(self, lib, names)
        XFIT.BindEvent(self.XfitEvent)
        ToolBar.Place(XFIT)
        # group into radio collection
        RadioCollect([MEASURE, DRAG, EXPAND, XEXPAND, YEXPAND, SHRINK])
        # setup content and set size
        Content = Group(HORIZONTAL)
        Content.Place(self.Graph)
        Content.Place(ToolBar)
        Content.DrawAllDecorations(self)
        self.SetSize(Content.GetSize())
        # done
        return

    def MeasureEvent(self, event):
        if event.status == 1: self.Graph.ToolSelect(self.MeasureTool)
        if event.status == 0: self.MeasureTool.Deselect()
        return

    def DragEvent(self, event):
        if event.status == 1: self.Graph.ToolSelect(self.DragTool)
        if event.status == 0: self.DragTool.Deselect()
        return

    def ExpandEvent(self, event):
        if event.status == 1: self.Graph.ToolSelect(self.ExpandTool)
        if event.status == 0: self.ExpandTool.Deselect()
        return

    def XExpandEvent(self, event):
        if event.status == 1: self.Graph.ToolSelect(self.XExpandTool)
        if event.status == 0: self.XExpandTool.Deselect()
        return

    def YExpandEvent(self, event):
        if event.status == 1: self.Graph.ToolSelect(self.YExpandTool)
        if event.status == 0: self.YExpandTool.Deselect()
        return

    def ShrinkEvent(self, event):
        X = 1.5 # coefficient
        xs, xe, ys, ye = self.Graph.limit
        sx, sy, cx, cy = X*(xe-xs), X*(ye-ys), 0.5*(xs+xe), 0.5*(ys+ye)
        xs, xe, ys, ye = cx-sx/2, cx+sx/2, cy-sy/2, cy+sy/2
        self.Graph.SetXLimit(xs, xe)
        self.Graph.SetYLimit(ys, ye)
        self.Graph.RefreshBuffer()
        self.Graph.Refresh()
        return

    def YfitEvent(self, event):
        if event.status:
            # get geometry
            xs, xe, ys, ye = self.Graph.limit
            # set start limits
            Ys, Ye = inf, -inf
            # for each data sets:
            plots = self.Graph.bufferGraph.plots
            for plot in plots:
                # restrict data set
                I = (plot.x >= xs) & (plot.x <= xe)
                y = plot.y[where(I)]
                if len(y):
                    # get data span
                    ys, ye = min(y), max(y)
                    # get overall extrema
                    Ys, Ye = min(Ys, ys), max(Ye, ye)
            plots = self.Graph.OnPaintGraph.plots
            for plot in plots:
                # restrict data set
                I = (plot.x >= xs) & (plot.x <= xe)
                y = plot.y[where(I)]
                if len(y):
                    # get data span
                    ys, ye = min(y), max(y)
                    # get overall extrema
                    Ys, Ye = min(Ys, ys), max(Ye, ye)
            # leave thin border surounding data
            X = 1.11 # (11 percent each side)
            sy, cy = X*(Ye-Ys), 0.5*(Ys+Ye)
            ys, ye = cy-sy/2, cy+sy/2
            # update limits
            self.Graph.SetYLimit(ys, ye)
            self.Graph.RefreshBuffer()
            self.Graph.Refresh()
        return

    def XfitEvent(self, event):
        if event.status:
            xs, xe, ys, ye = self.Graph.limit
            Xs, Xe = inf, -inf
            plots = self.Graph.bufferGraph.plots
            for plot in plots:
                I = (plot.y >= ys) & (plot.y <= ye)
                x = plot.x[where(I)]
                if len(x):
                    xs, xe = min(x), max(x)
                    Xs, Xe = min(Xs, xs), max(Xe, xe)
            plots = self.Graph.OnPaintGraph.plots
            for plot in plots:
                I = (plot.y >= ys) & (plot.y <= ye)
                x = plot.x[where(I)]
                if len(x):
                    xs, xe = min(x), max(x)
                    Xs, Xe = min(Xs, xs), max(Xe, xe)
            X = 1.11
            sx, cx = X*(Xe-Xs), 0.5*(Xs+Xe)
            xs, xe = cx-sx/2, cx+sx/2
            self.Graph.SetXLimit(xs, xe)
            self.Graph.RefreshBuffer()
            self.Graph.Refresh()
        return

###############################################################################
###############################################################################

class _Drag(ScreenDragBuffer):
    # superseed the previous _unlock() method to
    # provide a RefreshBuffer() at the end of
    # the drag event
    def _unlock(self, event):
        if self.lock:
            self.scr.RefreshBuffer()            
            self.lock = False
        return

###############################################################################
###############################################################################

class _Expand(ScreenTool):

    def Start(self):
        self.lock = False
        self.pen = wx.Pen(wx.Colour(150, 150, 150), style = wx.PENSTYLE_SOLID)
        self.brush = wx.Brush(wx.Colour(150,150,150, 64))
        return

    def onPaint(self, dc):
        if self.lock:
            X, Y = self.start                       # starting point
            x, y = self.stop                        # current point
            x1, x2 = min(X, x), max(X, x)           # order values
            y1, y2 = min(Y, y), max(Y, y)           # order values
            # use a graphic context on the device context
            gc = wx.GraphicsContext.Create(dc)
            gc.SetPen(self.pen)
            gc.SetBrush(self.brush)
            # create path, draw and close path
            path = gc.CreatePath()
            path.AddRectangle(x1, y1, x2-x1, y2-y1)
            path.CloseSubpath()
            gc.DrawPath(path)

        return

    def _LeftDown(self, event):
        self.lock  = True
        self.start = event.GetPosition()
        self.stop  = self.start
        return

    def _Motion(self, event):
        if self.lock:
            self.stop = event.GetPosition()
            self.scr.Refresh()
        return

    def _LeftUp(self, event):
        if self.lock:
            self.stop = event.GetPosition()
            X, Y = self.start
            x, y = self.stop
            x1, x2 = min(X, x), max(X, x)
            y1, y2 = min(Y, y), max(Y, y)
            # convert selected pixels into data coordinates
            xs, ys = self.scr.OnPaintGraph._getCoords(x1, y2)
            xe, ye = self.scr.OnPaintGraph._getCoords(x2, y1)
            # minimum 10x10 pixels
            if (x2-x1) > 10 and (y2-y1) > 10:
                # update data scale
                self.scr.SetXLimit(xs, xe)
                self.scr.SetYLimit(ys, ye)
            self.lock = False
            self.scr.RefreshBuffer()
            self.scr.Refresh()
        # done   
        return

    # cancel operation
    def _Leave(self, event):
        if self.lock:
            self.lock = False
            self.scr.Refresh()        
        return

###############################################################################
###############################################################################

class _XExpand(ScreenTool):

    def Start(self):
        self.lock = False
        self.pen = wx.Pen(wx.Colour(150, 150, 150), style = wx.PENSTYLE_SOLID)
        self.brush = wx.Brush(wx.Colour(150,150,150, 64))
        return

    def onPaint(self, dc):
        if self.lock:
            l, r, t, b = self.scr.OnPaintGraph.border
            W, H = self.scr.GetSize()
            X, Y = self.start                       # starting point
            x, y = self.stop                        # current point
            x1, x2 = min(X, x), max(X, x)           # order values
            y1, y2 = min(Y, y), max(Y, y)           # order values
            # use a graphic context on the device context
            gc = wx.GraphicsContext.Create(dc)
            gc.SetPen(wx.TRANSPARENT_PEN)
            gc.SetBrush(self.brush)
            # create path, draw and close path
            path = gc.CreatePath()
            path.AddRectangle(x1, t, x2-x1, H-t-b)
            path.CloseSubpath()
            gc.DrawPath(path)
            # draw lines
            dc.SetPen(self.pen)
            dc.DrawLine(x1, t, x1, H-b)
            dc.DrawLine(x2, t, x2, H-b)
        return

    def _LeftDown(self, event):
        self.lock  = True
        self.start = event.GetPosition()
        self.stop  = self.start
        return

    def _Motion(self, event):
        if self.lock:
            self.stop = event.GetPosition()
            self.scr.Refresh()
        return

    def _LeftUp(self, event):
        if self.lock:
            self.stop = event.GetPosition()
            X, Y = self.start
            x, y = self.stop
            x1, x2 = min(X, x), max(X, x)
            y1, y2 = min(Y, y), max(Y, y)
            # convert selected pixels into data coordinates
            xs, ys = self.scr.OnPaintGraph._getCoords(x1, y2)
            xe, ye = self.scr.OnPaintGraph._getCoords(x2, y1)
            # minimum 10x10 pixels
            if (x2-x1) > 10:
                # update data scale
                self.scr.SetXLimit(xs, xe)
            self.lock = False
            self.scr.RefreshBuffer()
            self.scr.Refresh()
        # done   
        return

    # cancel operation
    def _Leave(self, event):
        if self.lock:
            self.lock = False
            self.scr.Refresh()        
        return

###############################################################################
###############################################################################

class _YExpand(ScreenTool):

    def Start(self):
        self.lock = False
        self.pen = wx.Pen(wx.Colour(150, 150, 150), style = wx.PENSTYLE_SOLID)
        self.brush = wx.Brush(wx.Colour(150,150,150, 64))
        return

    def onPaint(self, dc):
        if self.lock:
            l, r, t, b = self.scr.OnPaintGraph.border
            W, H = self.scr.GetSize()
            X, Y = self.start                       # starting point
            x, y = self.stop                        # current point
            x1, x2 = min(X, x), max(X, x)           # order values
            y1, y2 = min(Y, y), max(Y, y)           # order values
            # use a graphic context on the device context
            gc = wx.GraphicsContext.Create(dc)
            gc.SetPen(wx.TRANSPARENT_PEN)
            gc.SetBrush(self.brush)
            # create path, draw and close path
            path = gc.CreatePath()
            path.AddRectangle(l, y1, W-l-r, y2-y1)
            path.CloseSubpath()
            gc.DrawPath(path)
            # draw lines
            dc.SetPen(self.pen)
            dc.DrawLine(l, y1, W-r, y1)
            dc.DrawLine(l, y2, W-r, y2)
        return

    def _LeftDown(self, event):
        self.lock  = True
        self.start = event.GetPosition()
        self.stop  = self.start
        return

    def _Motion(self, event):
        if self.lock:
            self.stop = event.GetPosition()
            self.scr.Refresh()
        return

    def _LeftUp(self, event):
        if self.lock:
            self.stop = event.GetPosition()
            X, Y = self.start
            x, y = self.stop
            x1, x2 = min(X, x), max(X, x)
            y1, y2 = min(Y, y), max(Y, y)
            # convert selected pixels into data coordinates
            xs, ys = self.scr.OnPaintGraph._getCoords(x1, y2)
            xe, ye = self.scr.OnPaintGraph._getCoords(x2, y1)
            # minimum 10x10 pixels
            if (y2-y1) > 10:
                # update data scale
                self.scr.SetYLimit(ys, ye)
            self.lock = False
            self.scr.RefreshBuffer()
            self.scr.Refresh()
        # done   
        return

    # cancel operation
    def _Leave(self, event):
        if self.lock:
            self.lock = False
            self.scr.Refresh()        
        return

###############################################################################
###############################################################################

class _Measure(ScreenTool):

    def Start(self):
        # LOCAL
        self.lock = False
        self.P0 = None
        self.P1 = None
        # style
        self.colour = wx.Colour(155,155,100) # adjust color
        self.pen = wx.Pen(self.colour, 1, wx.PENSTYLE_DOT_DASH)
        self.brush = wx.Brush(wx.Colour(0,0,0), wx.BRUSHSTYLE_SOLID)
        return

    def onPaint(self, dc):
        # get refernce to graph
        Graph = self.scr.OnPaintGraph
        # get geometry
        l, r, t, b = Graph.border
        W, H = Graph.size
        # draw P0
        if self.P0:
            x0, y0 = self.P0
            dc.SetPen(self.pen)
            dc.DrawLine(x0, t, x0, H-b)            
            dc.DrawLine(l, y0, W-r, y0)
        # draw P1
        if self.P1:
            x1, y1 = self.P1
            dc.SetPen(self.pen)
            dc.DrawLine(x1, t, x1, H-b)            
            dc.DrawLine(l, y1, W-r, y1)                
        # get style
        n, d = Graph.xFormat; fx = f'%.{d+1}f'
        n, d = Graph.yFormat; fy = f'%.{d+1}f'
        # set style
        dc.SetBrush(self.brush)
        dc.SetFont(Graph.font)
        dc.SetTextForeground(self.colour)
        dc.SetPen(wx.TRANSPARENT_PEN)
        wX, wY = 0, 0
        # write P0
        if self.P0:
            x0, y0 = self.P0
            X0, Y0 = self.scr.OnPaintGraph._getCoords(x0, y0)
            X, Y = l, t
            T = "X0 = " + fx % X0
            wX, h = dc.GetTextExtent(T)
            dc.DrawRectangle(X, Y, wX, h)
            dc.DrawText(T, X, Y)
            X, Y = X, Y+h
            T = "Y0 = " + fx % Y0
            wY, h = dc.GetTextExtent(T)
            dc.DrawRectangle(X, Y, wY, h)
            dc.DrawText(T, X, Y)
        # draw P1
        if self.P1:
            x1, y1 = self.P1
            X1, Y1 = self.scr.OnPaintGraph._getCoords(x1, y1)
            X, Y = X + max(wX, wY)+5, t
            T = "X1 = " + fx % X1
            wX, h = dc.GetTextExtent(T)
            dc.DrawRectangle(X, Y, wX, h)
            dc.DrawText(T, X, Y)
            X, Y = X, Y+h
            T = "Y1 = " + fx % Y1
            wY, h = dc.GetTextExtent(T)
            dc.DrawRectangle(X, Y, wY, h)
            dc.DrawText(T, X, Y)
        # write delta
        if self.lock:
            X, Y = X + max(wX, wY)+5, t
            T = "dX = " + fx % (X1-X0)
            wX, h = dc.GetTextExtent(T)
            dc.DrawRectangle(X, Y, wX, h)
            dc.DrawText(T, X, Y)
            X, Y = X, Y+h
            T = "dY = " + fx % (Y1-Y0)
            wY, h = dc.GetTextExtent(T)
            dc.DrawRectangle(X, Y, wY, h)
            dc.DrawText(T, X, Y)
        # done
        return

    def _getPosition(self, event):
        # get geometry
        l, r, t, b = self.scr.OnPaintGraph.border
        W, H = self.scr.GetSize()
        # get event parameters
        position = event.GetPosition()
        # filter values
        X, Y = position
        if X<l or X>W-r-1: position = None
        if Y<t or Y>H-b-1: position = None
        # done
        return position

    def _LeftDown(self, event):
        self.lock  = True
        self.P0 = self._getPosition(event) 
        self.P1 = self.P0
        return

    def _Motion(self, event):
        # get position
        P = self._getPosition(event)
        # update measured value
        if self.lock: self.P0, self.P1 = self.P0, P
        else:         self.P0, self.P1 = P, None
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
            self.lock  = False
            self.P0 = self._getPosition(event)
            self.P1 = None
            self.scr.Refresh()
        return
