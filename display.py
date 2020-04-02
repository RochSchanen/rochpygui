# 'display.py'
# Roch schanen
# created; 2020 Jan 30

# wxpython: https://www.wxpython.org/
import wx

# local modules:
from colors import BackgroundColour

# Extract and store bitmaps from png files
class PNGlib():

	def __init__(self, path = "./resources/pngs/"):
		self.path   = path
		self.pngs   = {}
		self.Grid   = 1, 1
		self.Size   = None
		self.Offset = 0, 0
		return

	def load(self, name):
		path = self.path + name + ".png"
		self.Sample = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
		return

	# p is the number of columns
	# q is the number of lines
	def SetGrid(self, p, q):
		self.Grid = p, q
		return

	# default None ()
	def SetSize(self, Size):
		self.Size = Size
		return

	# default is None
	def SetOffset(self, X, Y):
		self.Offset = X, Y
		return

	# add bitmap to the dictionary
	# from the grid index
	def Add(self, name, m, n):
		# get geometry
		X, Y = self.Offset
		p, q = self.Grid
		W, H = self.Sample.GetSize()
		P, Q = W/p, H/q
		w, h = (P, Q) if self.Size == None else self.Size
		x, y = (m-1)*P + (P-w)/2, (n-1)*Q + (Q-h)/2
		Clip = wx.Rect(x, y, w, h)
		self.pngs[name] = self.Sample.GetSubBitmap(Clip)
		return

	#  get bitmap(s) from the dictionary by name(s)
	def Get(self, names):
		# return single image
		if not isinstance(names, list):
			return self.pngs[names]
		# return list of images
		pngs = []
		for name in names:
			pngs.append(self.pngs[name])
		# done
		return pngs

class Display(wx.Control):

	def __init__(
		self,
		parent,
		pnglib,
		names):

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
		# the set of images is defined by a name list
		self.names  = names
		# load the whole set of images:
		self.pngs   = pnglib.Get(names)

		# LOCAL
		# status is an index or a name
		self.status = 0

		# get png size from first image
		w, h = self.pngs[self.status].GetSize()
		self.SetSize((w, h))

		# set background color
		self.SetBackgroundColour(BackgroundColour)

		# BINDINGS
		self.Bind(wx.EVT_ERASE_BACKGROUND, self._onEraseBackground)
		self.Bind(wx.EVT_PAINT, self._onPaint)

		return

	def _onEraseBackground(self, event):
		# no operation (reduced flicker)
		pass 

	def _onPaint(self, event):
		v = self.status
		if isinstance(v, int): n = v
		if isinstance(v, str): n = self.names.index(v)
		dc = wx.BufferedPaintDC(self)
		dc.DrawBitmap(self.pngs[n], 0, 0)
		return

	def SetValue(self, Value):
		self.status = Value
		self.Refresh()
		return

	def GetValue(self):
		return self.status

