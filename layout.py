# 'layout.py'
# decorations located in ./resources/decorations/
# Roch schanen
# created 2017 sept 23

# wxpython: https://www.wxpython.org/
import wx

# colors:
from colors import BackgroundColor, dcClear, dcMark

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
	# Decorations are found in ".\resources\decorations\"
	# example: some_group.Place(some_item, CENTER, 'Groove', (10,10,5,5))

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
				item.SetPosition((self.x+x, self.y+y+b+s))
				
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

	def GetSize(self):

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

		# coerce to the minimum user size
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

			for item, decoration in zip(self.items, self.decorations):
		
				# Get geometry
				w, h = item.GetSize()
				x, y = item.GetPosition()

				if decoration:
					# get decoration geometry
					# s = Decors.Side(decoration)
					# dc.DrawBitmap(Decors.Get(decoration, w+2*s, h+2*s), x-s, y-s)
					dcMark(dc, x-5, y-5, w+2*5, h+2*5)

				else:
					dcClear(dc, x, y, w, h)

				if isinstance(item, Group):
					# draw children decoration
					item._DrawDecorations(dc)

		return