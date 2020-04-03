# 'buttons.py'
# Roch schanen
# created; 2020 Feb 7

# wxpython: https://www.wxpython.org/
import wx
import wx.lib.newevent

# local modules:
from display import Display

# root class for buttons
class _btn(Display):

	def __init__(
		self,
		parent,
		pnglib,
		names):

		Display.__init__(
			self,
			parent = parent,
			pnglib = pnglib,
			names  = names)

		# LOCALS
		self.radio = None
		self.ctr   = None
		self.evt   = None

		# BINDINGS
		self.Bind(wx.EVT_LEFT_DOWN,     self._onMouseDown)
		self.Bind(wx.EVT_LEFT_DCLICK,   self._onMouseDown)
		# capture double clicks events as secondary single clicks

		self._start()

		return

	def _start(self):
		pass

	# radio feature
	def _clear(self):
		pass

	# on EVT_LEFT_DOWN, the event.skip()
	# method must be called to preserve
	# the focus event to be processed
	def _onMouseDown(self, event):
		event.Skip() # allow focus events
		return

	# Bind the event to the parent handler
	def BindEvent(self, handler):
		# "handler" is a reference to a function defined by the parent
		self.ctr, self.evt = wx.lib.newevent.NewEvent()
		self.GetParent().Bind(self.evt, handler)
		return

	# Sends a event to parent using "status" as parameter
	def SendEvent(self):
		if self.ctr:
			event = self.ctr(caller=self, status=self.status)
			wx.PostEvent(self.GetParent(), event)
		return

# send event on mouse_down()
class Push(_btn):

	def _start(self):
		self.lock = False
		self.Bind(wx.EVT_LEFT_UP,      self._onMouseUp)
		self.Bind(wx.EVT_LEAVE_WINDOW, self._onMouseLeave)
		return

	def _onMouseDown(self, event):
		event.Skip() # allow focus events
		self.lock = True
		if self.radio:
			self.radio.Select(self)
		self.status = 1
		self.Refresh()
		self.SendEvent()
		return

	def _onMouseUp(self, event):
		if self.lock:
			self.lock = False
			self.status = 0
			self.Refresh()
		return

	def _onMouseLeave(self, event):
		if self.lock:
			self.lock = False
			self.status = 0
			self.Refresh()
		return

# send event on release
class Switch(_btn):

	def _start(self):
		self.lock = False
		self.Bind(wx.EVT_LEFT_UP, self._onMouseUp)
		self.Bind(wx.EVT_LEAVE_WINDOW, self._onMouseLeave)
		return

	def _onMouseDown(self, event):
		event.Skip() # allow focus events
		self.lock = True
		if self.radio:
			self.radio.Select(self)
		return

	def _onMouseUp(self, event):
		if self.lock:
			self.lock = False
			self.status ^= 1
			self.Refresh()
			self.SendEvent()
		return

	def _onMouseLeave(self, event):
		if self.lock:
			self.lock = False
		return

	# called by radio group
	def _clear(self):
		if self.status:
			self.status = 0
			self.Refresh()
			self.SendEvent()
		return

# send event on mouse_down()
class Radio(_btn):

	def _onMouseDown(self, event):
		event.Skip() # allow focus events
		if self.radio:
			self.radio.Select(self)
		if not self.status:
			self.status = 1		
			self.Refresh()
			self.SendEvent()
		return

	# called by a radio group to deselect self
	def _clear(self):
		if self.status:
			self.status = 0
			self.Refresh()
			self.SendEvent()
		return

class RadioCollect():

	def __init__(self, btns):
		self.btns = btns
		for b in self.btns:
			b.radio = self
		return

	def Select(self, btn):
		for b in self.btns:
			if b is not	btn:
				b._clear()
		return
