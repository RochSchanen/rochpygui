# 'myapp.py'
# user's code
# Roch schanen
# created 2020 March 21
# https://github.com/RochSchanen/rochpygui

# minimum code to start an interface:

# local imports
from base   import baseApp
from colors import BackgroundColor
from layout import Group
from layout import HORIZONTAL, VERTICAL
from layout import LEFT, RIGHT, TOP, BOTTOM, CENTER
from layout import Decorations

# wxpython: https://www.wxpython.org/
import wx

# create app
class myApp(baseApp):

	def Start(self):

		# sub groups or graphic objetcs
		g1 = Group(VERTICAL,  50,  50)
		g2 = Group(VERTICAL, 100, 100)
		g3 = Group(VERTICAL, 150, 150)
		g4 = Group(VERTICAL, 200, 200)

		# Contents layout vertical:

		Content = Group(VERTICAL, w = 300, h = 300)
		Content.Place(g1)
		Content.Place(g2, LEFT, border = (20, 20, 20, 20), decoration = "Groove")
		Content.Place(g3, CENTER, border = (20, 20, 20, 20))
		Content.Place(g4, RIGHT, decoration = "Ridge", border = (20, 0, 0, 0))
		Content.Expand()

		# Contents layout horizontal:

		# Content = Group(HORIZONTAL, w = 700, h = 700)
		# Content.Place(g1)
		# Content.Place(g2, TOP, border = (20, 20, 20, 20), decoration = "Inset")
		# Content.Place(g3, CENTER, border = (20, 20, 20, 20))
		# Content.Place(g4, BOTTOM, decoration = "Outset", border = (20, 0, 0, 0))
		# Content.Expand()

		# draw once and set size
		Content.DrawAllDecorations(self.Frame.Panel)
		self.Frame.SetClientSize(Content.GetSize())

		return

myApp().MainLoop()
