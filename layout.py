# 'layout.py'
# content; The layout system. Group and Decorations.
# author; Roch schanen
# created; 2020 Mars 26
# repository; https://github.com/RochSchanen/rochpygui

# wxpython: https://www.wxpython.org/
import wx

from theme import BackgroundColour

# options
_opt = 1

# directions
HORIZONTAL  = _opt; _opt<<=1    
VERTICAL    = _opt; _opt<<=1   

# alignments
CENTER      = _opt; _opt<<=1
LEFT        = _opt; _opt<<=1
RIGHT       = _opt; _opt<<=1
TOP         = _opt; _opt<<=1
BOTTOM      = _opt; _opt<<=1

# The group class allows to group and align graphic objects.
# All graphic objects must have:
# - A positioning method: SetPostion((x, y))
# - A size method: GetSize() returning a tuple (w, h)
class Group:

	def __init__(
			self,
			direction = HORIZONTAL,   # default orientation of the group
			w         = 10,           # minimum width of this group
			h         = 10):          # minimum height of this group
		
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
		
		# done
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
		# get geometry
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
						# distribute the remainder
						# among the first items: 
						m=0
						if p>1: m=1; p -= 2
						# set new borders
						self.borders[i] = l+q+m, r+q+m, t, b

			# expand vertically
			if direction & VERTICAL:
				# compute parameters
				m = max(H, h)
				# modify borders
				for i in range(len(self.items)):
					name = self.decorations[i]
					align = self.alignments[i]
					# get current geometry
					iw, ih = self.items[i].GetSize()
					l, r, t, b = self.borders[i]
					L, R, T, B = 0, 0, 0, 0
					if name: L, R, T, B = \
						Decorations.GetGeometry(name)
					# compute current height
					s = ih + t+b + T+B
					# modify accordingly
					if align == TOP: 	t, b = t, b+m-s
					if align == BOTTOM: t, b = t+m-s, b
					if align == CENTER:
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
						# distribute the remainder
						# among the first items:
						m=0 
						if p>1: m=1; p -= 2
						# set new borders
						self.borders[i] = l, r, t+q+m, b+q+m

			# expand horizontally
			if direction & HORIZONTAL:
				# compute parameters
				m = max(W, w)
				# modify borders
				for i in range(len(self.items)):
					name = self.decorations[i]
					align = self.alignments[i]
					# get current geometry
					iw, ih = self.items[i].GetSize()
					l, r, t, b = self.borders[i]
					L, R, T, B = 0, 0, 0, 0
					if name: L, R, T, B = \
						Decorations.GetGeometry(name)
					# compute current width
					s = iw + l+r + L+R
					# modify accordingly
					if align == LEFT: 	l, r = l, r+m-s
					if align == RIGHT: 	l, r = l+m-s, r
					if align == CENTER:
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

		# reset all children positions
		x, y = 0, 0
		for item, alignment, decoration, border in zip(
			self.items, self.alignments, self.decorations, self.borders):
			# get geometry (width, height)
			w, h = item.GetSize()
			# get border (left, right, top, bottom)
			l, r, t, b = border 
			# get decors geometry
			L, R, T, B = 0, 0, 0, 0
			if decoration: L, R, T, B = \
				Decorations.GetGeometry(decoration)

			if self.direction == VERTICAL:
				# get horizontal offset
				if alignment == LEFT:   x = l+L
				if alignment == CENTER: x = W/2-w/2
				if alignment == RIGHT:  x = W-w-r-R
				# set position
				item.SetPosition((self.x + x, self.y + y + t+T))
				# shift vertical position for next item
				y += h + t+b + T+B

			if self.direction == HORIZONTAL:
				# get vertical offset
				if alignment == TOP:    y = t+T
				if alignment == CENTER: y = H/2-h/2
				if alignment == BOTTOM: y = H-h-b-B
				# set position
				item.SetPosition((self.x + x + l+L, self.y + y))
				# shift horizontal position for next item
				x += w + l+r + L+R
		# done
		return

	def GetPosition(self):
		return (self.x, self.y)

	def _GetMinSize(self):
		# current position start at 0, 0
		W, H = 0, 0
		for item, decoration, border in zip(
			self.items, self.decorations, self.borders):
			# get geometry (width, height)
			w, h = item.GetSize()
			# get border (left, right, top, bottom)
			l, r, t, b = border 
			# get decors geometry
			L, R, T, B = 0, 0, 0, 0
			if decoration: L, R, T, B = \
				Decorations.GetGeometry(decoration)
			# build size
			if self.direction == VERTICAL:
				W = max(W, w + L+R + l+r)
				H += h + T+B + t+b
			if self.direction == HORIZONTAL:
				W += w + L+R + l+r
				H = max(H, h + T+B + t+b)
			# coerce
			if decoration:
				# minimum 10x10 pixels inside a decoration
				if W < (L+R+10): W = (L+R+10)
				if H < (T+B+10): H = (T+B+10)
		#done
		return (W, H)

	def GetSize(self):
		# get geometry
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
		# set background color
		dc.SetPen(wx.TRANSPARENT_PEN)
		dc.SetBrush(wx.Brush(BackgroundColour, wx.SOLID))
		dc.DrawRectangle(0, 0, w, h)
		# draw decorations recursively
		self._DrawDecorations(dc)
		# release device context
		dc.SelectObject(wx.NullBitmap)
		# done        
		return

	def _DrawDecorations(self, dc):
		# check for empty contents
		if self.items: 
			for item, name, border in zip(
				self.items, self.decorations, self.borders):
				# check decoration
				if name:
					# Get geometry
					w, h = item.GetSize()
					x, y = item.GetPosition()
					l, r, t, b = border
					L, R, T, B = Decorations.GetGeometry(name)
					# get decoration bitmap
					Bitmap = Decorations.GetBitmap(
						name, w+l+r+L+R, h+t+b+T+B)
					# draw decoration
					dc.DrawBitmap(Bitmap, x-l-L, y-t-T)
				# draw children decoration
				if isinstance(item, Group):
					item._DrawDecorations(dc)
		return

class _decorationsLibrary():

	registeredDecorations = {
		"Groove":  (4, 3, 4, 3, 3, 3, 3, 3),
		"Ridge" :  (3, 4, 3, 4, 3, 3, 3, 3),
		"Inset" :  (4, 4, 4, 4, 3, 3, 3, 3),
		"Outset":  (4, 4, 4, 4, 3, 3, 3, 3)}
		# todo: use info files to define geometry
		# elements are L, R, T, B, l, r, t, b

	# decorations elements are "name":(Sample, l, r, t, b)
	def __init__(self, Path):
		self.path = Path
		self.decorations = {} 
		return

	def _GetSampleAndGeometry(self, Name):

		# check if name is in library
		if Name in self.decorations:
			# get geometry and sample from library
			Sample, l, r, t, b = self.decorations[Name]

		# check if name is in defintions
		elif Name in self.registeredDecorations:
			# get geometry
			L,R,T,B,l,r,t,b = self.registeredDecorations[Name]
			# get path to decoration file
			path = self.path + Name + ".png"
			# load raw bitmap
			Raw = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
			# clip edges to make decoration sample
			W, H = Raw.GetSize()
			Clip = wx.Rect(L, T, W-L-R, H-T-B)
			Sample = Raw.GetSubBitmap(Clip)
			# store into library
			self.decorations[Name] = (Sample, l, r, t, b)

		# default (name was not found anywhere)
		else:
			# get geometry
			r, l, t, b = 3, 3, 3, 3
			# create sample bitmap
			Sample = wx.EmptyBitmap(32, 32, wx.BITMAP_SCREEN_DEPTH)
			# create dc
			dc = wx.MemoryDC()
			dc.SelectObject(Sample)
			# set background color
			dc.SetBrush(wx.Brush(BackgroundColour, wx.BRUSHSTYLE_SOLID))
			dc.SetPen(wx.TRANSPARENT_PEN)
			dc.DrawRectangle(0, 0, 32, 32)
			# draw decoration (grey line countour)
			dc.SetPen(wx.GREY_PEN)
			dc.DrawRectangle(1, 1, 32-2*1, 32-2*1)
			# release dc
			dc.SelectObject(wx.NullBitmap)
			# store into library
			self.decorations[Name] = (Sample, l, r, t, b)

		return Sample, l, r, t, b

	# get the sample and expand it to the required size
	def GetBitmap(self, name, width, height):
		# get geometry and sample
		Sample, l, r, t, b = self._GetSampleAndGeometry(name)
		W, H = Sample.GetSize()
		w, h = width, height
		# create Bitmap
		Bitmap = wx.EmptyBitmap(w, h, wx.BITMAP_SCREEN_DEPTH)
		# create dc
		dc = wx.MemoryDC()
		dc.SelectObject(Bitmap)
		# set background color
		dc.SetPen(wx.TRANSPARENT_PEN)
		dc.SetBrush(wx.Brush(BackgroundColour, wx.BRUSHSTYLE_SOLID))
		dc.DrawRectangle(0, 0, width, height)
		# top
		tile = Sample.GetSubBitmap(wx.Rect(l, 0, W-l-r, t))
		self._TileHorizontally(dc, tile,   l, 0, w-l-r)
		# bottom
		tile = Sample.GetSubBitmap(wx.Rect(l, H-b, W-l-r, b))
		self._TileHorizontally(dc, tile,   l, h-b, w-l-r)
		# left
		tile = Sample.GetSubBitmap(wx.Rect(0, t, l, H-t-b))
		self._TileVertically(dc, tile,     0, t,    h-t-b)
		# right
		tile = Sample.GetSubBitmap(wx.Rect(W-r, t, r, H-t-b))
		self._TileVertically(dc, tile,     w-r, t,    h-t-b)
		# top left
		tile = Sample.GetSubBitmap(wx.Rect(0, 0, l, t))
		dc.DrawBitmap(tile,                0, 0)
		# top right
		tile = Sample.GetSubBitmap(wx.Rect(W-r, 0, r, t))
		dc.DrawBitmap(tile,                w-r, 0)
		# bottom left
		tile = Sample.GetSubBitmap(wx.Rect(0, H-b, l, b))
		dc.DrawBitmap(tile,                0, h-b)
		# bottom right
		tile = Sample.GetSubBitmap(wx.Rect(W-r, H-b, r, b))
		dc.DrawBitmap(tile,                w-r, h-b)
		# release dc
		dc.SelectObject(wx.NullBitmap)
		# done
		return Bitmap

	def _TileHorizontally(self, dc, tile, x, y, width):
		w, h = tile.GetSize()
		for i in range(width / w):
			dc.DrawBitmap(tile, x, y)
			x += w
		remainder = width % w
		if remainder:
			clip = wx.Rect(0, 0, remainder, h)
			dc.DrawBitmap(tile.GetSubBitmap(clip) , x, y)
		return

	def _TileVertically(self, dc, tile, x, y, height):
		w, h = tile.GetSize()
		for i in range(height / h):
			dc.DrawBitmap(tile, x, y)
			y += h
		remainder = height % h
		if remainder: 
			clip = wx.Rect(0, 0, w, remainder)
			dc.DrawBitmap(tile.GetSubBitmap(clip) , x, y)
		return

	def GetGeometry(self, name):
		Sample, l, r, t, b = self._GetSampleAndGeometry(name)
		return l, r, t, b

# create empty library
# (The library fills up as decorations get requested)
Decorations = _decorationsLibrary("./resources/decorations/")
