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
		self.buffer   = None
		self.position = 0, 0
		self.clipArea = 0, 0, 0, 0

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
		# draw
		if self.buffer:
			# get clip geometry
			x, y = self.position
			w, h = self.W, self.H
			l, r, t, b = self.clipArea
			# get clip image
			r = wx.Rect(x+l, y+t, w-l-r, h-t-b)
			clip = self.buffer.GetSubBitmap(r)
			# draw clipped area
			dc.DrawBitmap(clip, l, t)
		# done: It is not required to deselect
		# the DC object when using BufferedPaintDC()
		# in the onPaint() context [ref].
		return

# tool used to drag the buffer under the clipScreen
class _dragClipScreenBuffer():

	def __init__(self, ClipScreen):
		self.scr = ClipScreen
		self.lock = False
		return

	# additional painting
	def onPaint(self, dc):
		pass

	# self select method
	def Select(self):
		# Bind Screen events to this tool handler methods
		self.scr.Bind(wx.EVT_LEFT_DOWN, 	self._LeftDown)
		self.scr.Bind(wx.EVT_MOTION, 		self._Motion)
		self.scr.Bind(wx.EVT_LEFT_UP, 		self._LeftUp)
		# Leaving window is considered as a mouse up event
		self.scr.Bind(wx.EVT_LEAVE_WINDOW,  self._LeftUp)
		return

	# self deselect method
	def Deselect(self):
		# Bind Screen events to this tool handler methods
		self.scr.Unbind(wx.EVT_LEFT_DOWN)
		self.scr.Unbind(wx.EVT_MOTION)
		self.scr.Unbind(wx.EVT_LEFT_UP)
		self.scr.Unbind(wx.EVT_LEAVE_WINDOW)
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
			# refresh() invoques the _onPaint method
			self.scr.Refresh()
		return

	def _LeftUp(self, event):
		if self.lock:
			# here: call to a user refresh of the buffer
			self.lock = False
		return
