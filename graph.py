# 'graph.py'
# content; classes for the plot interface.
# author; Roch schanen
# created; 2020 April 11
# repository; https://github.com/RochSchanen/rochpygui

# todo: - rationalise extra border EB
# todo: - eventually remove DEBUG
# todo: - set right label alignment to the right
#       (sign changes are shifting the text position)
# todo: - There seems to be a difference between labels and main ticks!
#       (in some rare circumptances, there is more labels than main ticks)
#       The algorithms for computing the ticks and labels must be exactly the same

DEBUG = False

# wxpython: https://www.wxpython.org/
import wx

# numpy: https://numpy.org/
from numpy import exp, log10, floor, ceil, linspace, array

from theme import *

###############################################################################
################################# GRAPH #######################################
###############################################################################

# local options (internal to graph)
_opt = 1

# style options
DRAW_BOX       = _opt; _opt<<=1
DRAW_AXIS      = _opt; _opt<<=1
DRAW_GRID      = _opt; _opt<<=1
DRAW_PLOTS     = _opt; _opt<<=1

DRAW_LABEL_LEFT    = _opt; _opt<<=1
DRAW_LABEL_RIGHT   = _opt; _opt<<=1
DRAW_LABEL_TOP     = _opt; _opt<<=1
DRAW_LABEL_BOTTOM  = _opt; _opt<<=1

DRAW_LABELS = (DRAW_LABEL_BOTTOM
             | DRAW_LABEL_TOP
             | DRAW_LABEL_RIGHT
             | DRAW_LABEL_LEFT)

SKIP_BORDERS   = _opt; _opt<<=1

class Graph():

    def __init__(self):
        
        # LOCAL
        self.limit  = None        # this is the box coordinates
        self.size   = None        # this is the bitmap size
        self.border = 0, 0, 0, 0  # these are the border around the box

        # style defines which elements are drawn onto the bitmap and how:
        self.style      = 0     # default style
        self.ticks      = 7, 7  # expected number of ticks on the grid (x and y)
        self.font       = None
        self.leftText   = None
        self.bottomText = None
        self.xFormat    = [2, 1] # integer digits, decimal digits
        self.yFormat    = [2, 1] # integer digits, decimal digits
        self.plots      = {}     # list of plot to draw

        # scale is computed from size, limit and border:
        self.scale     = None        

        # extra border        
        self.EB = 5 

        # done
        return

    def Draw(self, dc):
        if self.scale:
            if self.style & DRAW_GRID:   self._drawGrid(dc)
            if self.style & DRAW_AXIS:   self._drawAxis(dc)
            if self.style & DRAW_BOX:    self._drawBox(dc)
            if self.style & DRAW_LABELS: self._drawLabels(dc)
            if self.style & DRAW_PLOTS:  self._drawPlots(dc)
            self._drawTitles(dc)
        # else: print("_graph.Draw(): undefined scale.")
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

    # def StyleClear(self, StyleFlag):
    #     self.style &= ~StyleFlag
    #     return

    def SetFont(self, Font):
        self.font = Font
        return

    def SetXFormat(self, f):
        self.xFormat = f
        return

    def SetYFormat(self, f):
        self.yFormat = f
        return

    def SetLeftTitle(self, s):
        self.leftText = s
        return

    def SetBottomTitle(self, s):
        self.bottomText = s
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
        dc.SetPen(wx.Pen(wx.Colour(150,150,150), 1.0))
        # draw box
        dc.DrawRectangle(l, t, W-l-r, H-t-b)
        # done
        return

    def _drawAxis(self, dc):
        # get geometry
        W, H = self.size
        X, Y = self._getPixels(0.0, 0.0)
        l, r, t, b = self.border
        if self.style & SKIP_BORDERS: l, r, t, b = 0, 0, 0, 0
        # setup style
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.Pen(wx.Colour(200,200,230), 2))
        # draw Axis
        dc.DrawLine(X, t, X, H-b-1)
        dc.DrawLine(l, Y, W-r-1, Y)
        # done
        return

    def _drawGrid(self, dc):
        # get geometry
        W, H = self.size
        # X, Y = self._getPixels(0.0, 0.0)
        l, r, t, b = self.border
        if self.style & SKIP_BORDERS: l, r, t, b = 0, 0, 0, 0
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
        # X, Y = self._getPixels(0.0, 0.0)
        l, r, t, b = self.border
        xs, xe, ys, ye = self.limit
        # get style
        nx, ny = self.ticks
        # get ticks intervals
        mix, six = self._getTKI(xs, xe, nx)
        miy, siy = self._getTKI(ys, ye, ny)
        # find edge coordinates
        # xs, ys = self._getCoords(l, H-b-1) # ?
        # xe, ye = self._getCoords(W-r-1, t) # ?
        # get tick positions (coordinates)
        mpx, spx = self._getTKP(xs, xe, mix, six)
        mpy, spy = self._getTKP(ys, ye, miy, siy)
        # get mains tick positions (pixels)
        X, Y = self._getPixels(mpx, mpy)
        # set style
        dc.SetFont(self.font)
        dc.SetTextForeground(wx.Colour(180,180,180))

        if self.style & (DRAW_LABEL_BOTTOM | DRAW_LABEL_TOP):
            # get formatting
            n, d = self.xFormat # length, decimals
            f = f'%.{d}f'       # string format
            # draw horizontal labels
            for x, v in zip(X, mpx):
                # get label string
                lT = f % v                                   
                lW, lH = dc.GetTextExtent(lT) # get size
                p = x-lW/2                    # get position
                p = max(p, l)                 # coerce to min
                p = min(p, W-r-lW)            # coerce to max
                if self.style & DRAW_LABEL_TOP:
                    dc.DrawText(lT, p, t-lH)
                if self.style & DRAW_LABEL_BOTTOM:
                    dc.DrawText(lT, p, H-b)

                if DEBUG:
                    dc.SetBrush(wx.TRANSPARENT_BRUSH)
                    if self.style & DRAW_LABEL_TOP:
                        dc.DrawRectangle(p, t-lH, lW, lH)
                    if self.style & DRAW_LABEL_BOTTOM:
                        dc.DrawRectangle(p, H-b, lW, lH)

        if self.style & (DRAW_LABEL_LEFT | DRAW_LABEL_RIGHT):
            # get formatting
            n, d = self.yFormat # length, decimals
            f = f'%.{d}f'       # string format
            # draw horizontal labels
            for y, v in zip(Y, mpy):
                # get label string
                lT = f % v                                   
                lW, lH = dc.GetTextExtent(lT) # get size
                q = y-lH/2                    # get position
                if self.style & DRAW_LABEL_LEFT:
                    dc.DrawText(lT, l-lW-self.EB, q)
                if self.style & DRAW_LABEL_RIGHT:
                    dc.DrawText(lT, W-r+self.EB, q)

                if DEBUG:
                    dc.SetBrush(wx.TRANSPARENT_BRUSH)
                    if self.style & DRAW_LABEL_LEFT:
                        dc.DrawRectangle(l-lW-self.EB, q, lW, lH)
                    if self.style & DRAW_LABEL_RIGHT:
                        dc.DrawRectangle(W-r+self.EB, q, lW, lH)

        return

    def _drawTitles(self, dc):
        if self.font:
            # get geometry
            W, H = self.size
            # set style
            dc.SetFont(self.font)
            dc.SetTextForeground(wx.Colour(180,180,180))
            # draw left
            if len(self.leftText):
                lT = self.leftText
                lW, lH = dc.GetTextExtent(lT)
                dc.DrawRotatedText(lT, 0, H/2+lW/2, 90)
            # draw botttom
            if len(self.bottomText):
                lT = self.bottomText
                lW, lH = dc.GetTextExtent(lT)
                dc.DrawRotatedText(lT, W/2-lW/2, H-lH, 0)
        return

    def _drawPlots(self, dc):
        # get geometry
        W, H = self.size
        l, r, t, b = self.border
        if self.style & SKIP_BORDERS: l, r, t, b = 0, 0, 0, 0
        dc.SetClippingRegion(l, t, W-l-r, H-t-b)
        # draw
        for plot in self.plots.values():
            if len(plot.x) and len(plot.y):
                # get data
                X, Y   = self._getPixels(plot.x, plot.y)
                points = list(zip(X, Y))
                bitmap = plot.point
                pw, ph = bitmap.GetSize()
                pw, ph = round(pw/2), round(ph/2)
                # draw lines
                dc.SetPen(plot.pen)
                dc.DrawLines(points)
                # draw points
                for x, y in points:
                    dc.DrawBitmap(bitmap, x-pw, y-ph)

                # DEBUG
                # dc.SetPen(wx.Pen(wx.Colour(255,255,255)))
                # for x, y in points:
                #     dc.DrawPoint(x, y)
                #     dc.DrawPoint(x-pw, y-ph)
                #     dc.DrawPoint(x+pw, y+pw)

        dc.DestroyClippingRegion()
        return

    def AddPlot(self, Name, X, Y):
        # create object
        p = _plot(X, Y)
        # store
        self.plots[Name] = p
        # return reference
        return p

class _plot():

    def __init__(self, X = [], Y = []):
        # LOCAL
        self.pen        = None
        self.point      = None
        self.colour     = None
        # DEFAULTS
        self.pointStyle = 'DOT','WHITE','MEDIUM'
        self.lineStyle  = 'SOLID','THIN'
        # PARAMETERS
        self.x, self.y = array(X), array(Y)
        # setup
        self.SetPointStyle()
        # done
        return

    def SetPointStyle(self, Styles = None):

        SHAPES = {
            'DOT'        : "DOT"}

        COLOURS = {
            'WHITE'      : "White",
            'BLUE'       : "Blue",
            'RED'        : "Red",
            'GREEN'      : "Green"}

        SIZES = {
            'SMALL'      : "_0",
            'MEDIUM'     : "_1",
            'LARGE'      : "_2",
            'EXTRALARGE' : "_3"}

        # fit parameter type (Style must be a list)
        if not isinstance(Styles, list): Styles = [Styles]
        # get current values
        shape, colour, size = self.pointStyle
        # run through new values
        for style in Styles:
            if style in SHAPES.keys():  shape  = style
            if style in COLOURS.keys(): colour = style
            if style in SIZES.keys():   size   = style
        # record new values
        self.pointStyle = shape, colour, size
        # store point
        lib, images = Theme.GetImages(SHAPES[shape], COLOURS[colour])
        self.point = lib.Get(COLOURS[colour] + SIZES[size])
        # get colour from point bitmap
        dc = wx.MemoryDC()               # setup device context
        dc.SelectObject(self.point)      # select point as bitmap
        w, h = self.point.GetSize()      # find center of bitmap
        self.colour = dc.GetPixel(w/2, h/2)   # pick colour
        dc.SelectObject(wx.NullBitmap)   # release device context
        # update line color
        self.SetLineStyle()
        # done
        return

    def SetLineStyle(self, Styles = None):

        DASHINGS = {
            'DOT'        : wx.PENSTYLE_DOT,
            'DOT DASH'   : wx.PENSTYLE_DOT_DASH,
            'LONG DASH'  : wx.PENSTYLE_LONG_DASH,
            'SHORT DASH' : wx.PENSTYLE_SHORT_DASH,
            'SOLID'      : wx.PENSTYLE_SOLID,
            'TRANSPARENT': wx.PENSTYLE_TRANSPARENT}

        WIDTHS = {
            'THIN'       : 1,
            'MEDIUM'     : 2,
            'THICK'      : 3}

        # fit parameter type (Style must be a list)
        if not isinstance(Styles, list): Styles = [Styles]
        # get current values
        dashing, width = self.lineStyle
        # run through values
        for style in Styles:
            if style in DASHINGS.keys(): dashing = style
            if style in WIDTHS.keys():   width   = style
        # record new values
        self.lineStyle = dashing, width
        # store pen
        self.pen = wx.Pen(self.colour, WIDTHS[width], DASHINGS[dashing])
        # done
        return
