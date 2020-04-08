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

# tool used to drag the buffer under the clipScreen
class _ClipScreenDragBuffer(_ClipScreenTool):

	def Start(self):
		self.lock = False

		self.position = None # ...

		return

	def onPaint(self, dc):
		if self.position:
			x, y = self.position
			dc.SetPen(wx.Pen(
				wx.Colour(220,100,100), 1.0))
			dc.DrawLine(x-15, y, x+15, y)
			dc.DrawLine(x, y-15, x, y+15)
		return

	# todo: no drag from the border
	def _LeftDown(self, event):
		self.lock = True        
		self.MouseStart  = event.GetPosition()
		self.scrStart = self.scr.position
		self.position = self.MouseStart # ...
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

			self.position = x, y # ...

			# refresh() invoques the _onPaint method
			self.scr.Refresh()
		return

	def _LeftUp(self, event):
		if self.lock:
			# here: call to a user refresh of the buffer
			self.lock = False

			self.position = None # ...
			self.scr.Refresh()

		return

	def _LeaveWindow(self, event):
		self._LeftUp(event)
		return
