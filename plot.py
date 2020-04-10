# 'plot.py'
# content; classes for the plot interface.
# author; Roch schanen
# created; 2020 April 07
# repository; https://github.com/RochSchanen/rochpygui

# wxpython: https://www.wxpython.org/
import wx

# numpy: https://numpy.org/
from numpy import exp, log10, floor, ceil, linspace

# LOCAL
from theme import *

###############################################################################
###################################  SCREEN ###################################
###############################################################################

class _screen(wx.Control):

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
        self.size   = Width, Height

        # LOCAL
        self.tool       = None
        self.buffer     = None
        self.position   = 0, 0
        self.clipArea   = 0, 0, 0, 0

        # set geometry
        self.SetSize(self.size)

        # call user-defined constructor     
        self.Start()

        # bind events
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._onEraseBackground) 
        self.Bind(wx.EVT_PAINT, self._onPaint)

        # done
        return

    # user defined constructor
    def Start(self):
        pass

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
            w, h = self.size
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

        # more drawing from selected tool
        if self.tool: self.tool.onPaint(dc)

        # It is not required to release
        # the DC object when BufferedPaintDC()
        # is used in the onPaint() method:
        # done
        return

    def onPaint(self, dc):
        pass

    def ToolSelect(self, newTool):
        if self.tool: self.tool.Deselect()
        self.tool = newTool
        newTool.Select()
        self.Refresh()
        return

###############################################################################
#################################### TOOL #####################################
###############################################################################

# generic class for creating tools
class _tool():

    def __init__(self, ClipScreen):
        self.scr = ClipScreen
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
        self.scr.Bind(wx.EVT_LEAVE_WINDOW,  self._LeaveWindow)
        return

    # self deselect method
    def Deselect(self):
        # Unbind Screen events to this tool handler methods
        self.scr.Unbind(wx.EVT_LEFT_DOWN)
        self.scr.Unbind(wx.EVT_MOTION)
        self.scr.Unbind(wx.EVT_LEFT_UP)
        self.scr.Unbind(wx.EVT_LEAVE_WINDOW)
        return

    def _LeaveWindow(self, event):
        pass

###############################################################################
#################################### DRAG BUFFER ##############################
###############################################################################

# tool used to drag the buffer under the clipScreen
class _dragBuffer(_tool):

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

    def _LeaveWindow(self, event):
        self._unlock(event)
        return

    def _unlock(self, event):
        if self.lock:
            # here: call to a user refresh of the buffer
            self.lock = False
        return

###############################################################################
################################# GRAPH #######################################
###############################################################################

# local options (internal to graph)
_opt = 1

# style options
_DRAW_BOX       = _opt; _opt<<=1
_DRAW_AXIS      = _opt; _opt<<=1
_DRAW_GRID      = _opt; _opt<<=1
_DRAW_PLOTS     = _opt; _opt<<=1

_LABELS_LEFT    = _opt; _opt<<=1
_LABELS_RIGHT   = _opt; _opt<<=1
_LABELS_TOP     = _opt; _opt<<=1
_LABELS_BOTTOM  = _opt; _opt<<=1

_SKIP_BORDERS   = _opt; _opt<<=1

_DRAW_LABELS = (_LABELS_BOTTOM
              | _LABELS_TOP
              | _LABELS_RIGHT
              | _LABELS_LEFT)

class _graph():

    def __init__(self):
        
        # LOCAL
        self.limit  = None        # this is the box coordinates
        self.size   = None        # this is the bitmap size
        self.border = 0, 0, 0, 0  # these are the border around the box

        # style defines which elements are drawn onto the bitmap and how:
        self.style  = 0    # default style
        self.ticks  = 7, 7 # expected number of ticks on the grid (x and y)
        
        # scale is computed from size, limit and border:
        self.scale  = None        
        
        # done
        return

    def Draw(self, dc):
        if self.scale:
            if self.style & _DRAW_GRID:   self._drawGrid(dc)
            if self.style & _DRAW_AXIS:   self._drawAxis(dc)
            if self.style & _DRAW_BOX:    self._drawBox(dc)
            if self.style & _DRAW_LABELS: self._drawLabels(dc)
        else: print("_graph.Draw(): undefined scale.")
        return

    def SetSize(self, Size):
        self.size = Size
        self._setScale()
        return

    def SetBorder(self, l, r, t, b):
        self.border = l, r, t, b
        self._setScale()
        return

    def SetLimit(self, xs, xe, ys, ye):
        self.limit = float(xs), float(xe), float(ys), float(ye)
        self._setScale()
        return

    def StyleSet(self, StyleFlag):
        self.style |= StyleFlag
        return

    def StyleClear(self, StyleFlag):
        self.style &= ~StyleFlag
        return

    def SetFont(self, Font):
        self.font = Font
        return

    def SetFormat(self, Format):
        self.format = Format
        return

    # Compute scale such that:

    # xs -> l
    # xe -> W-r-1
    # ys -> H-b-1 
    # ye -> t

    def _setScale(self):
        self.scale = None
        if not self.limit: return
        if not self.size: return
        # get geometry
        W, H = self.size
        l, r, t, b = self.border
        xs, xe, ys, ye = self.limit
        # make computation explicit
        Xs, Xe, Ys, Ye = l, W-r-1, H-b-1, t
        # check for singulatiries
        if xe == xs: return
        if ye == ys: return
        # compute scale
        ax = (Xe-Xs)/float(xe-xs)
        ay = (Ye-Ys)/float(ye-ys)
        bx, by = Xs-ax*xs, Ys-ay*ys
        # record result
        self.scale = ax, bx, ay, by
        return

    # get pixels from coordinates
    # (x and y can be arrays of the same size)
    def _getPixels(self, x, y):
        ax, bx, ay, by = self.scale
        X, Y = ax*x+bx, ay*y+by
        return X, Y

    # get coordinates from pixels
    # (X and Y can be arrays of the same size)
    def _getCoords(self, X, Y):
        ax, bx, ay, by = self.scale
        # compute coordinates
        x, y = (X-bx)/ax, (Y-by)/ay
        return x, y

    def _drawBox(self, dc):
        # get geometry
        W, H = self.size
        l, r, t, b = self.border
        # setup style
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.Pen(wx.Colour(150,150,0), 1.0))
        # draw box
        dc.DrawRectangle(l, t, W-l-r, H-t-b)
        # done
        return

    def _drawAxis(self, dc):
        # get geometry
        W, H = self.size
        X, Y = self._getPixels(0.0, 0.0)
        l, r, t, b = self.border
        if self.style & _SKIP_BORDERS: l, r, t, b = 0, 0, 0, 0
        # setup style
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.Pen(wx.Colour(220,100,100), 1.0))
        # draw Axis
        dc.DrawLine(X, t, X, H-b-1)
        dc.DrawLine(l, Y, W-r-1, Y)
        # done
        return

    def _drawGrid(self, dc):
        # get geometry
        W, H = self.size
        X, Y = self._getPixels(0.0, 0.0)
        l, r, t, b = self.border
        if self.style & _SKIP_BORDERS: l, r, t, b = 0, 0, 0, 0
        xs, xe, ys, ye = self.limit
        # get style
        nx, ny = self.ticks
        # get ticks intervals
        mix, six = self._getTKI(xs, xe, nx)
        miy, siy = self._getTKI(ys, ye, ny)
        # find edge coordinates
        xs, ys = self._getCoords(l, H-b-1)
        xe, ye = self._getCoords(W-r-1, t)
        # get buffer ticks positions (coordinates)
        mpx, spx = self._getTKP(xs, xe, mix, six)
        mpy, spy = self._getTKP(ys, ye, miy, siy)
        # set sub grid style
        dc.SetPen(wx.Pen(wx.Colour(70,70,70), 1.0))
        # Get tik positions in pixels
        X, Y = self._getPixels(spx, spy)
        # draw grid lines
        for x in X: dc.DrawLine(x, t, x, H-b-1)
        for y in Y: dc.DrawLine(l, y, W-r-1, y)
        # set main grid style
        dc.SetPen(wx.Pen(wx.Colour(150,150,150), 1.0))
        # Get tik positions in pixels
        X, Y = self._getPixels(mpx, mpy)
        # draw grid lines
        for x in X: dc.DrawLine(x, t, x, H-b-1)
        for y in Y: dc.DrawLine(l, y, W-r-1, y)
        # done
        return

    # get Interval for an optimum number of ticks
    def _getTKI(self, valStart, valStop, nTicks):
        # trial table
        T = [0.010,0.020,0.025,0.050,0.100,0.200,0.250,0.500,1.000,2.000,2.500,5.000]
        # the ticks sub division interval is fixed to be human readable
        S = [    5,    4,    5,    5,    5,    4,    5,    5,    5,    4,    5,    5]
        ln10 = 2.3025850929940459
        span = valStop - valStart           # get data span
        dec = exp(ln10*floor(log10(span)))  # get decade
        span /= dec                         # re-scale span
        # find number of tiks closest to n
        i=0; m=floor(span/T[i])             # first trial
        while m > nTicks:                   # next ?
            i+=1; m=floor(span/T[i])        # try again 
        # get results
        mti = dec*T[i]                      # main ticks interval
        sti = mti/S[i]                      # sub ticks interval
        return mti, sti

    # get ticks positions
    # vs: value_start
    # ve: value_end
    # mn: main_interval (see _GetTKI)
    # sb:  sub_interval (see _GetTKI)
    # returns the main tick positions "mp" and the sub tick positions "sp"
    def _getTKP(self, valStart, valStop, mti, sti):
        # main ticks
        ns = ceil(valStart/mti-0.001)*mti  # start
        ne = floor(valStop/mti+0.001)*mti  # end
        p  = round((ne-ns)/mti)+1          # fail safe
        mp = linspace(ns,ne,p)             # main positions
        # sub ticks
        ns = ceil(valStart/sti+0.001)*sti  # start
        ne = floor(valStop/sti-0.001)*sti  # end
        p  = round((ne-ns)/sti)+1          # fail safe
        sp = linspace(ns,ne,p)             # sub positions
        # done
        return mp, sp

    def _drawLabels(self, dc):
        # get geometry
        W, H = self.size
        X, Y = self._getPixels(0.0, 0.0)
        l, r, t, b = self.border
        xs, xe, ys, ye = self.limit
        # get style
        nx, ny = self.ticks

        # get ticks intervals
        mix, six = self._getTKI(xs, xe, nx)
        miy, siy = self._getTKI(ys, ye, ny)
        # find edge coordinates
        xs, ys = self._getCoords(l, H-b-1) # ?
        xe, ye = self._getCoords(W-r-1, t) # ?
        # get tick positions (coordinates)
        mpx, spx = self._getTKP(xs, xe, mix, six)
        mpy, spy = self._getTKP(ys, ye, miy, siy)
        # get mains tick positions (pixels)
        X, Y = self._getPixels(mpx, mpy)
        # get style
        dc.SetFont(self.font)
        dc.SetTextForeground(wx.Colour(250,250,250))

        if self.style & (_LABELS_BOTTOM | _LABELS_TOP):
            # get formatting
            n, d = self.format['x']                # length, decimals
            f = f'%.{d}f'                          # string format
            # draw horizontal labels
            for x, v in zip(X, mpx):
                # get label string
                lT = f % v                                   
                lW, lH = dc.GetTextExtent(lT)      # get size
                p = x-lW/2                         # get position
                p = max(p, l)                      # coerce to min
                p = min(p, W-r-lW)                 # coerce to max
                if self.style & _LABELS_TOP:    dc.DrawText(lT, p, t-lH)
                if self.style & _LABELS_BOTTOM: dc.DrawText(lT, p, H-b)

        if self.style & (_LABELS_LEFT | _LABELS_RIGHT):
            # get formatting
            n, d = self.format['y']                # length, decimals
            f = f'%.{d}f'                          # string format
            # draw horizontal labels
            for y, v in zip(Y, mpy):
                # get label string
                lT = f % v                                   
                lW, lH = dc.GetTextExtent(lT)      # get size
                q = y-lH/2                         # get position
                q = max(q, t)                      # coerce to min
                q = min(q, H-b-lH)                 # coerce to max
                if self.style & _LABELS_LEFT:  dc.DrawText(lT, l-lW, q)
                if self.style & _LABELS_RIGHT: dc.DrawText(lT, W-r, q)

        return

###############################################################################
#################################### PLOT #####################################
###############################################################################

class _plot(_screen):

    def Start(self):

        ln10 = 2.3025850929940459

        font = Theme.GetFont()

        LabelFormat = {
            "x": [3, 2],
            "y": [3, 2]}

        # FIND TEXT SIZE FOR LABELS

        dc = wx.ClientDC(self)
        dc.SetFont(font)

        n, d = LabelFormat['x']                # length, decimals
        f = f'%.{d}f'                          # get format string
        v = -(exp(ln10*(n+d))-1)/exp(ln10*(d)) # full size value
        Width, tmp = dc.GetTextExtent(f % v)   # get width
        print(f % v)

        n, d = LabelFormat['y']                # length, decimals
        f = f'%.{d}f'                          # get format string
        v = -(exp(ln10*(n+d))-1)/exp(ln10*(d)) # full size value
        tmp, Height = dc.GetTextExtent(f % v)  # get width
        print(f % v)

        labelSize = Width, Height        

        # SET BORDER SIZE
        W, H = labelSize
        l, r, t, b = W, W, H, H
        l, r, t, b = l+20, r+20, t+20, b+20
        self.clipArea  = l, r, t, b

        # get screen geometry
        W, H = self.Size
        w, h = W-l-r, H-t-b
        
        # create buffer
        self.buffer = wx.Bitmap(3*w, 3*h, wx.BITMAP_SCREEN_DEPTH)
        self.position = w-l, h-t

        # create and setup graph for drawing buffer:
        g = _graph()
        g.SetSize(self.buffer.GetSize())
        g.SetBorder(w, w, h, h)
        g.SetLimit(-10.32, +10.17, -10.13, +10.38)
        g.StyleSet(_DRAW_AXIS | _DRAW_GRID)
        g.StyleSet(_SKIP_BORDERS)

        self.bufferGraph = g

        # create and setup graph for onPaint refresh:
        g = _graph()
        g.SetSize(self.GetSize())
        g.SetBorder(l, r, t, b)
        g.SetLimit(-10.32, +10.17, -10.13, +10.38)
        g.StyleSet(_DRAW_BOX | _DRAW_LABELS)
        g.SetFont(font)
        g.SetFormat(LabelFormat)

        self.OnPaintGraph = g

        # CLEAR AND DRAW BUFFER

        # create context
        dc = wx.MemoryDC()      
        dc.SelectObject(self.buffer)
        # clear buffer
        dc.SetBackground(wx.Brush(wx.Colour(0,0,0)))
        dc.Clear()
        # now draw  graph on buffer
        self.bufferGraph.Draw(dc)
        # and release device context
        dc.SelectObject(wx.NullBitmap)

        # SETUP DRAG TOOL

        # d = _dragBuffer(self)
        # self.ToolSelect(d)

        return

    def onPaint(self, dc):
        self.OnPaintGraph.Draw(dc)
        return
