# 'testApp.py'
# 
# Roch schanen
# created 2020 April 06
# https://github.com/RochSchanen/rochpygui

# local imports
from base		import *
from theme 		import *
from layout		import *
from display 	import *
from buttons	import *
from controls 	import *

from plot import _ClipScreen
from plot import _ClipScreenDragBuffer

# create app
class myApp(App):

	def Start(self):

		C = _ClipScreen(self.Panel, 400, 400)
		C.buffer = wx.Bitmap("./milkyway.jpg", wx.BITMAP_TYPE_PNG)
		D = _ClipScreenDragBuffer(C)
		C.ToolSelect(D)		

		BODY   = Group(VERTICAL)
		BODY.Place(Text(self.Panel, "Title"))
		BODY.Place(C)

		# set content
		Content = Group(VERTICAL)
		Content.Place(BODY, decoration = "Outset")

		# draw once and set size
		Content.DrawAllDecorations(self.Panel)
		return

myApp().MainLoop()
