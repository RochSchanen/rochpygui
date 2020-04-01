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

		HEADER = Group(HORIZONTAL, h = 50)
		BODY   = Group(HORIZONTAL, 200, 200)
		FOOTER = Group(HORIZONTAL, h = 50)  

		# set content
		Content = Group(VERTICAL)
		Content.Place(HEADER, decoration = "Groove")
		Content.Place(BODY, decoration = "Groove")
		Content.Place(FOOTER, decoration = "Groove")

		# expand
		Content.Expand()

		# draw once and set size
		Content.DrawAllDecorations(self.Frame.Panel)
		self.Frame.SetClientSize(Content.GetSize())

		return

myApp().MainLoop()
