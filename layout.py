# 'layout.py'
# Roch schanen
# created 2017 sept 23

# wxpython: https://www.wxpython.org/
import wx

from colors import BackgroundColor

# dcgraphics: (this needs some clarification)
from dcgraphics import dcClear, dcMark

# define options
opt = 1

HORIZONTAL  = opt; opt<<=1    
VERTICAL    = opt; opt<<=1   

CENTER      = opt; opt<<=1
LEFT        = opt; opt<<=1
RIGHT       = opt; opt<<=1
TOP         = opt; opt<<=1
BOTTOM      = opt; opt<<=1

# The group class allows to group and align graphic objects.
# All graphic objects must have:
# - A positioning method: SetPostion((x, y))
# - A size method: GetSize() returning a tuple (w, h)

class Group:

	def __init__(
			self,
			direction = HORIZONTAL,   # default orientation of the group
			w         = 0,            # minimum width of this group
			h         = 0):           # minimum height of this group

		# This group parameters
		self.direction = direction
		self.x, self.y = 0, 0   # this group position
		self.w, self.h = w, h   # this group minimum width and height
		self.parent    = None   # this group parent

		# This group contents
		self.items       = []   # list of items in this group
		self.alignments  = []   # items' alignment
		self.decorations = []   # items' decoration
		self.borders     = []   # items' border

		return

	# Add an item to this group
	# Items order follows the order in which they have added.
	# Options are:
	# - alignment
	# - decoration
	# - border
	# Example: some_group.Place(some_item, CENTER, 'Groove', (10,10,5,5))
	# Decorations such as "groove" are found in ".\resources\decorations\"

	def Place(
			self,
			item,                       # item object
			alignment  = CENTER,        # alignment
			decoration = None,          # decoration
			border     = (0, 0, 0, 0)   # borders (left, right, top, bottom)
			):

		# add the new item to the group
		self.items.append(item)
		self.alignments.append(alignment)
		self.decorations.append(decoration)
		self.borders.append(border)

		# If item is a group, register its parenthood
		# (Used for ending recursion).
		if isinstance(item, Group):
			item.parent = self

		# Update geometry of the group tree
		self._UpdateGeometry()

		return

	def Expand(self, direction = HORIZONTAL|VERTICAL):

		W, H = self.w, self.h
		w, h = self._GetMinSize()

		# this group direction is HORIZONTAL
		if self.direction == HORIZONTAL:

			# expand horizontally
			if direction & HORIZONTAL:
				if W > w:
					# compute parameters
					n = len(self.items)
					q = (W-w)/(2*n)		# ratio (integer)
					p = (W-w)-(2*n)*q	# remainder
					# modify borders
					for i in range(n):
						# get geometry
						l, r, t, b = self.borders[i]
						m=0 # distribute the remainder
						# among the first items: 
						if p>1: m=1; p -= 2
						# set new borders
						self.borders[i] = l+q+m, r+q+m, t, b

			# expand vertically
			if direction & VERTICAL:
				# compute parameters
				m = max(H, h)
				# modify borders
				for i in range(len(self.items)):
					# get current geometry
					iw, ih = self.items[i].GetSize()
					l, r, t, b = self.borders[i]
					# compute current height
					s = ih + t + b
					if self.decorations[i]:
						# todo: add decoration
						s += 2*5
					# modify accordingly
					a = self.alignments[i]
					if a == TOP: 	t, b = t, b+m-s
					if a == BOTTOM: t, b = t+m-s, b
					if a == CENTER:
						# split at the center
						q = (m-s)/2
						# correct for the remainder
						p = (m-s)-2*q
						# new borders
						t, b = t+q, b+q+p
					# set new borders
					self.borders[i] = l, r, t, b 

		# this group direction is HORIZONTAL
		if self.direction == VERTICAL:

			# expand vertically
			if direction & VERTICAL:
				if H > h:
					# compute parameters
					n = len(self.items)
					q = (H-h)/(2*n)		# ratio (integer)
					p = (H-h)-(2*n)*q	# remainder
					# modify borders
					for i in range(n):
						# get geometry
						l, r, t, b = self.borders[i]
						m=0 # distribute the remainder
						# among the first items:
						if p>1: m=1; p -= 2
						# set new borders
						self.borders[i] = l, r, t+q+m, b+q+m

			# expand horizontally
			if direction & HORIZONTAL:
				# compute parameters
				m = max(W, w)
				# modify borders
				for i in range(len(self.items)):
					# get current geometry
					iw, ih = self.items[i].GetSize()
					l, r, t, b = self.borders[i]
					# compute current height
					s = iw + l + r
					if self.decorations[i]:
						# todo: add decoration
						s += 2*5
					# modify accordingly
					a = self.alignments[i]
					if a == LEFT: 	l, r = l, r+m-s
					if a == RIGHT: 	l, r = l+m-s, r
					if a == CENTER:
						# split at the center
						q = (m-s)/2
						# correct for the remainder
						p = (m-s)-2*q
						# new borders
						l, r = l+q, r+q+p
					# set new borders
					self.borders[i] = l, r, t, b 

		self._UpdateGeometry()
		return

	# finds the top parent and reset positions
	def _UpdateGeometry(self):

		# find top parent
		if self.parent:
			self.parent._UpdateGeometry()
		
		else:
			# set position of child objects.
			# top parent has position (0, 0) by default.
			self.SetPosition((self.x, self.y))
		
		return

	def SetPosition(self, position):

		# record the new position
		self.x, self.y = position

		# get this group size (recursive)
		W, H = self.GetSize()                   

		# reset children positions

		x, y = 0, 0

		for item, alignment, decoration, border in zip(
			self.items, self.alignments, self.decorations, self.borders):

			# get geometry (width, height)
			w, h = item.GetSize()

			# get border (left, right, top, bottom)
			l, r, t, b = border 

			# get decors geometry
			s = 0
			if decoration:
				# s = Decors.Side(decoration)
				s = 5

			if self.direction == VERTICAL:

				# get horizontal offset
				if alignment == LEFT:   x = l+s
				if alignment == CENTER: x = W/2-w/2
				if alignment == RIGHT:  x = W-w-r-s

				# set position
				item.SetPosition((self.x+x, self.y+y+t+s))
				
				# shift vertical position for next item
				y += h+t+b+2*s

			if self.direction == HORIZONTAL:

				# get vertical offset
				if alignment == TOP:    y = t+s
				if alignment == CENTER: y = H/2-h/2
				if alignment == BOTTOM: y = H-h-b-s
				
				# set position
				item.SetPosition((self.x+x+l+s, self.y+y))
				
				# shift horizontal position for next item
				x += w+l+r+2*s

		return

	def GetPosition(self):
		return (self.x, self.y)

	def _GetMinSize(self):

		W, H = 0, 0

		for item, decoration, border in zip(
			self.items, self.decorations, self.borders):

			# get geometry (width, height)
			w, h = item.GetSize()

			# get border (left, right, top, bottom)
			l, r, t, b = border 

			# get decoration geometry
			s = 0
			if decoration:
				# s = Decors.Side(decoration)
				s = 5

			if self.direction == VERTICAL:
				W = max(W, w+2*s+l+r)
				H += h+2*s+t+b

			if self.direction == HORIZONTAL:
				W += w+2*s+l+r
				H = max(H, h+2*s+t+b)

			# c = 0
			# if decoration:
			# 	c = Decors.Corner(decoration)
			# 	# minimum 5x5 pixels inside a decoration
			# 	if W < (2*c+5): W = 2*c+5
			# 	if H < (2*c+5): H = 2*c+5

		return (W, H)

	def GetSize(self):

		W, H = self._GetMinSize()

		# coerce to requested size
		if W < self.w: W = self.w
		if H < self.h: H = self.h

		return (W, H)

	# Called once from top group
	# (no decoration around the top group)
	def DrawAllDecorations(self, Ctrl):

		# get the group geometry
		w, h = self.GetSize()

		# create bitmap of the same size
		Ctrl.BackgroundBitmap = wx.EmptyBitmap(w, h)

		# create device context for drawing
		dc = wx.MemoryDC()
		dc.SelectObject(Ctrl.BackgroundBitmap)

		# draw decorations recursively
		self._DrawDecorations(dc)

		# release device context
		dc.SelectObject(wx.NullBitmap)

		# done        
		return

	def _DrawDecorations(self, dc):

		if self.items: # check for empty contents

			for item, decoration, border in zip(
				self.items, self.decorations, self.borders):
		
				# Get geometry
				w, h = item.GetSize()
				x, y = item.GetPosition()
				l, r, t, b = border

				if decoration:

					# get decoration geometry
					# s = Decors.Side(decoration)
					# dc.DrawBitmap(Decors.Get(decoration, w+2*s, h+2*s), x-s, y-s)
					
					s = 5
					dcMark(dc, x-l-s, y-t-s, w+l+r+2*s, h+t+b+2*s)
					dc.SetPen(wx.Pen(
						wx.Colour(0, 150, 150), 
						width = 1,
						style = wx.PENSTYLE_SOLID))
					dc.DrawRectangle(x, y, w, h)

				else:

					dcClear(dc, x-l, y-t, w+l+r, h+t+b)
					dc.SetPen(wx.Pen(
						wx.Colour(0, 150, 150), 
						width = 1,
						style = wx.PENSTYLE_SOLID))
					dc.DrawRectangle(x, y, w, h)

				if isinstance(item, Group):

					# draw children decoration
					item._DrawDecorations(dc)
		return

class _decorationsLibrary():

	registeredDecorations = {
		"Groove":  (1, 1, 40, 40, 5, 5, 5, 5),
		"Ridge" :  (0, 0, 40, 40, 5, 5, 5, 5),
		"Inset" :  (0, 0, 41, 41, 5, 5, 5, 5),
		"Outset":  (0, 0, 40, 40, 5, 5, 5, 5)}
		# todo: use info files to define geometry
		# elements are x, y, w, h, l, r, t, b

	def __init__(self, Path):
		self.path = Path
		self.decorations = {} 
		# elements are "name":(Sample, l, r, t, b)
		return

	def GetBitmap(self, name, width, height):

		# check if name is in library
		if name in self.decorations:
			Sample, l, r, t, b = self.decorations[name]

		# check if name is in defintions
		elif name in self.registeredDecorations:
			x,y,w,h,l,r,t,b = self.registeredDecorations[name]
			path = self.path + name + ".png"
			Raw = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
			W, H = Raw.GetSize()
			Clip = wx.Rect(W/2-w/2+x, H/2-h/2+y, w, h)
			Sample = Raw.GetSubBitmap(Clip)
			self.decorations[name] = (Sample, r, l, t, b)

		# default
		else:
			r, l, t, b = 5, 5, 5, 5
			Sample = wx.EmptyBitmap(32, 32, wx.BITMAP_SCREEN_DEPTH)
			# draw default decoration
			dc = wx.MemoryDC()
			dc.SelectObject(Sample)
			dc.SetBrush(wx.Brush(BackgroundColor, wx.BRUSHSTYLE_SOLID))
			dc.SetPen(wx.TRANSPARENT_PEN)
			dc.DrawRectangle(0, 0, 32, 32)
			dc.SetPen(wx.GREY_PEN)
			dc.DrawRectangle(2, 2, 32-4, 32-4)
			dc.SelectObject(wx.NullBitmap)
			# store into library
			self.decorations[name] = (Sample, r, l, t, b)

		# build Bitmap
		W, H = Sample.GetSize()
		w, h = width, height
		Bitmap = wx.EmptyBitmap(w, h, wx.BITMAP_SCREEN_DEPTH)
		dc = wx.MemoryDC()
		dc.SelectObject(Bitmap)

		# Set background
		dc.SetPen(wx.TRANSPARENT_PEN)
		dc.SetBrush(wx.Brush(BackgroundColor, wx.BRUSHSTYLE_SOLID))
		dc.DrawRectangle(0, 0, width, height)

		# Draw corners                            x    y    w    h    x    y
		dc.DrawBitmap(Sample.GetSubBitmap(wx.Rect(0,   0,   l,   t)), 0,   0)
		dc.DrawBitmap(Sample.GetSubBitmap(wx.Rect(W-r, 0,   r,   t)), w-r, 0)
		dc.DrawBitmap(Sample.GetSubBitmap(wx.Rect(W-r, H-b, r,   b)), w-r, h-b)
		dc.DrawBitmap(Sample.GetSubBitmap(wx.Rect(0,   H-b, l,   b)), 0,   h-b)

		# draw borders
		B = wx.Brush(wx.BLACK, wx.BRUSHSTYLE_STIPPLE)
		#                                        x,    y,    w,     h
		B.SetStipple(Sample.GetSubBitmap(wx.Rect(l,    0,    W-l-r, t)))
		dc.SetBrush(B);         dc.DrawRectangle(l,    0,    w-l-r, t)
		B.SetStipple(Sample.GetSubBitmap(wx.Rect(l,    H-b,  W-l-r, b)))
		dc.SetBrush(B);         dc.DrawRectangle(l,    h-b,  w-l-r, b)
		B.SetStipple(Sample.GetSubBitmap(wx.Rect(0,    t,    l,     H-t-b)))
		dc.SetBrush(B);         dc.DrawRectangle(0,    t,    l,     h-t-b)
		B.SetStipple(Sample.GetSubBitmap(wx.Rect(W-r,  t,    r,     H-t-b)))
		dc.SetBrush(B);         dc.DrawRectangle(w-r,  t,    r,     h-t-b)

		dc.SelectObject(wx.NullBitmap)

		return Bitmap

	def Side(self, name):
		b, c, s = self.data[name]
		return s
 
Decorations = _decorationsLibrary("./resources/decorations/")
