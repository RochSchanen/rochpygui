# 'plot.py'
# content; classes for the plot interface.
# author; Roch schanen
# created; 2020 April 07
# repository; https://github.com/RochSchanen/rochpygui

# wxpython: https://www.wxpython.org/
import wx

# numpy: https://numpy.org/
import numpy as np

# LOCAL
from theme import *

###############################################################################
############################### CLIP SCREEN ###################################
###############################################################################

class _ClipScreen(wx.Control):

	def __init__(
		self,
		parent,
		Width 	= 100,
		Height	= 100):

		wx.Control.__init__(
			self,
			parent 		= parent,
			id 			= wx.ID_ANY,
			pos 		= wx.DefaultPosition,
			size 		= wx.DefaultSize,
			style 		= wx.NO_BORDER,
			validator 	= wx.DefaultValidator,
			name 		= "")

		# PARAMETERS
		self.parent = parent
		self.W 		= Width
		self.H 		= Height

		# LOCAL
		self.buffer 	= None
		self.position 	= 0, 0
		self.clipArea 	= 0, 0, 0, 0
		self.tool 		= None

		# Set Screen Size
		self.SetSize((self.W, self.H))

		# call user defined constructor		
		self.Start()

		# Bind display Refresh events
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
			x, y = self.position
			w, h = self.W, self.H
			l, r, t, b = self.clipArea
			# get clip image
			# todo: add case when negative values
			# todo: add case when too large values
			# at the moment: coertion is used in the drag tool
			r = wx.Rect(x+l, y+t, w-l-r, h-t-b)
			clip = self.buffer.GetSubBitmap(r)
			# draw clipped area
			dc.DrawBitmap(clip, l, t)

		# more drawing from user
		# add user onPaint() here ...

		# more drawing from selected tool
		if self.tool:
			self.tool.onPaint(dc)

		# done: It is not required to deselect
		# the DC object when using BufferedPaintDC()
		# in the onPaint() context [ref].
		return

	def ToolSelect(self, tool):
		if self.tool: self.tool.Deselect()
		self.tool = tool
		tool.Select()
		self.Refresh()
		return

###############################################################################
############################## CLIP SCREEN TOOL ###############################
###############################################################################

# generic class for creating tools
class _ClipScreenTool():

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
		self.scr.Bind(wx.EVT_LEFT_DOWN, 	self._LeftDown)
		self.scr.Bind(wx.EVT_MOTION, 		self._Motion)
		self.scr.Bind(wx.EVT_LEFT_UP, 		self._LeftUp)
		self.scr.Bind(wx.EVT_LEAVE_WINDOW,  self._LeaveWindow)
		return

	# self deselect method
	def Deselect(self):
		# Bind Screen events to this tool handler methods
		self.scr.Unbind(wx.EVT_LEFT_DOWN)
		self.scr.Unbind(wx.EVT_MOTION)
		self.scr.Unbind(wx.EVT_LEFT_UP)
		self.scr.Unbind(wx.EVT_LEAVE_WINDOW)
		return

	def _LeaveWindow(self, event):
		pass

###############################################################################
############################## CLIP SCREEN DRAG BUFFER ########################
###############################################################################

# tool used to drag the buffer under the clipScreen
class _ClipScreenDragBuffer(_ClipScreenTool):

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
			# coerce: todo instead of coertion
			# modify bitmap draw in _onPaint()
			w, h = self.scr.buffer.GetSize()
			W, H = self.scr.W, self.scr.H
			P, Q = max(P, 0), max(Q, 0)
			P, Q = min(P, w-W), min(Q, h-H)
			self.scr.position = P, Q
			# invoque the _onPaint method
			self.scr.Refresh()
		return

	def _LeftUp(self, event):
		if self.lock:
			# here: call to a user refresh of the buffer
			self.lock = False
		return

	# Make Leave event the same as Left event
	def _LeaveWindow(self, event):
		self._LeftUp(event)
		return

###############################################################################
################################# GRAPH #######################################
###############################################################################

# options
_opt = 1

# drawing location
LEFT			= _opt; _opt<<=1
RIGHT			= _opt; _opt<<=1
TOP				= _opt; _opt<<=1
BOTTOM			= _opt; _opt<<=1

# drawing options
DRAW_BOX		= _opt; _opt<<=1
DRAW_LABELS		= _opt; _opt<<=1
DRAW_GRID		= _opt; _opt<<=1
DRAW_AXIS		= _opt; _opt<<=1
DRAW_PLOTS		= _opt; _opt<<=1

SKIP_BORDERS 	= _opt; _opt<<=1

class _Graph():

	def __init__(self, Width, Height):

		# PARAMETERS
		self.size = Width, Height
		
		# LOCAL
		self.bitmap = wx.EmptyBitmap(Width, Height, wx.BITMAP_SCREEN_DEPTH)
		self.limit  = -1.0, 1.0, -1.0, 1.0 # default to avoid division by zero
		self.border = 0, 0, 0, 0
		self.scale  = None
		self.style  = DRAW_BOX | DRAW_AXIS | DRAW_GRID

		# here the buffer is only cleared
		self._resetScale()
		self._refreshBuffer()

		# done
		return

	# prepare to refresh the buffer:
	# create device context and clear
	def _refreshBuffer(self):
		# Create Device Context
		dc = wx.MemoryDC()
		# Select DisplayBitmap
		dc.SelectObject(self.bitmap)
		# set background
		dc.SetBackground(wx.Brush(wx.Colour(0,0,0)))
		# clear everything
		dc.Clear()
		# user drawings
		self.RefreshBuffer(dc)        
		# Release bitmap from the device context
		dc.SelectObject(wx.NullBitmap)
		return

	def ResetBorder(self, l, r, t, b):
		self.border = l, r, t, b
		self._resetScale()
		self._refreshBuffer()
		return

	def ResetLimit(self, xs, xe, ys, ye):
		self.limit = float(xs), float(xe), float(ys), float(ye)
		self._resetScale()
		self._refreshBuffer()
		return

	# Compute scale such that:

	# xs -> l
	# xe -> W-r-1
	# ys -> H-b-1 
	# ye -> t

	def _resetScale(self):
		# get geometry
		W, H = self.size
		l, r, t, b = self.border
		xs, xe, ys, ye = self.limit
		# make computation explicit
		Xs, Xe, Ys, Ye = l, W-r-1, H-b-1, t
		# compute scale
		ax = (Xe-Xs)/float(xe-xs)
		ay = (Ye-Ys)/float(ye-ys)
		bx, by = Xs-ax*xs, Ys-ay*ys
		# record result
		self.scale = ax, bx, ay, by
		return

	# get pixels from coordinates
	# (x and y can be arrays of the same size)
	def GetPixels(self, x, y):
		ax, bx, ay, by = self.scale
		X, Y = ax*x+bx, ay*y+by
		return X, Y

	# get coordinates from pixels
	# (X and Y can be arrays of the same size)
	def GetCoords(self, X, Y):
		ax, bx, ay, by = self.scale
		# compute coordinates
		x, y = (X-bx)/ax, (Y-by)/ay
		return x, y

	# the drawings happen here
	def RefreshBuffer(self, dc):
		if self.style & DRAW_GRID: 	self._drawGrid(dc)
		if self.style & DRAW_AXIS: 	self._drawAxis(dc)
		if self.style & DRAW_BOX: 	self._drawBox(dc)
		return

	def _drawBox(self, dc):
		# get geometry
		W, H = self.size
		l, r, t, b = self.border
		# setup style
		dc.SetBrush(wx.TRANSPARENT_BRUSH)
		dc.SetPen(wx.Pen(wx.Colour(200,200,100), 1.0))
		# draw box
		dc.DrawRectangle(l, t, W-l-r, H-t-b)
		# done
		return

	def _drawAxis(self, dc):
		# get geometry
		W, H = self.size
		X, Y = self.GetPixels(0.0, 0.0)
		l, r, t, b = self.border
		if self.style & SKIP_BORDERS:
			l, r, t, b = (0, 0, 0, 0)
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
		X, Y = self.GetPixels(0.0, 0.0)
		l, r, t, b = self.border
		xs, xe, ys, ye = self.limit
		# get ticks intervals
		mix, six = self._GetTKI(xs, xe, 7)
		miy, siy = self._GetTKI(ys, ye, 7)
		# find edge coordinates
		if self.style & SKIP_BORDERS: l, r, t, b = 0, 0, 0, 0
		xs, ys = self.GetCoords(l, H-b-1)
		xe, ye = self.GetCoords(W-r-1, t)
		# get buffer ticks positions (coordinates)
		mpx, spx = self._GetTKP(xs, xe, mix, six)
		mpy, spy = self._GetTKP(ys, ye, miy, siy)
		# set sub grid style
		dc.SetPen(wx.Pen(wx.Colour(70,70,70), 1.0))
		# Get tik positions in pixels
		X, Y = self.GetPixels(spx, spy)
		# draw grid lines
		for x in X: dc.DrawLine(x, t, x, H-b-1)
		for y in Y: dc.DrawLine(l, y, W-r-1, y)
		# set main grid style
		dc.SetPen(wx.Pen(wx.Colour(150,150,150), 1.0))
		# Get tik positions in pixels
		X, Y = self.GetPixels(mpx, mpy)
		# draw grid lines
		for x in X: dc.DrawLine(x, t, x, H-b-1)
		for y in Y: dc.DrawLine(l, y, W-r-1, y)
		# done
		return

	# get tick interval
	# vs: value_start
	# ve: value_end
	# n : expected number of ticks
	# returns the main tik interval "mn" and the  sub ticks interval "sb"
	def _GetTKI(self, vs, ve, n):

		#         0     1     2     3     4     5     6     7     8     9    10    11
		tt = [0.010,0.020,0.025,0.050,0.100,0.200,0.250,0.500,1.000,2.000,2.500,5.000]
		ss = [    5,    4,    5,    5,    5,    4,    5,    5,    5,    4,    5,    5]

		ln10 = 2.3025850929940459

		# main parameters
		rg = ve-vs 									# scale range
		du = np.exp(np.floor(np.log10(rg))*ln10) 	# decade multiplier
		dg = np.floor(rg/du) 						# digits number
		if dg<1.0: dg=1.0 							# fail safe

		# find optimum number of tiks
		i=0
		for t in tt:
			m = np.floor(rg/du/t) 	# number of intervals
			if m < n: 				# first match
				break
			i=i+1

		mn = du*t 					# main ticks intervals
		sb = mn/ss[i] 				# sub ticks intervals

		return mn, sb

	# get ticks positions
	# vs: value_start
	# ve: value_end
	# mn: main_interval (see _GetTKI)
	# sb:  sub_interval (see _GetTKI)
	# returns the main tick positions "mp" and the sub tick positions "sp"
	def _GetTKP(self, vs, ve, mn, sb):
		# main ticks
		ns =  np.ceil(vs/mn-0.001)*mn 		# start value
		ne = np.floor(ve/mn+0.001)*mn 		# end value
		p = round((ne-ns)/mn)+1 			# fail safe
		mp = np.linspace(ns,ne,p) 			# list of main positions
		# sub ticks
		ns =  np.ceil(vs/sb+0.001)*sb 		# start value
		ne = np.floor(ve/sb-0.001)*sb 		# end value
		p = round((ne-ns)/sb)+1 			# fail safe
		sp = np.linspace(ns,ne,p) 			# list of sub positions
		# done
		return mp, sp
