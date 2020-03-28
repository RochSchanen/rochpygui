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

# create app
class myApp(baseApp):

	def Start(self):

		# sub groups or graphic objetcs
		g1 = Group(VERTICAL,  50,  50)
		g2 = Group(VERTICAL, 100, 100)
		g3 = Group(VERTICAL, 150, 150)
		g4 = Group(VERTICAL, 200, 200)

		# Contents layout
		Content = Group(HORIZONTAL, w = 700, h = 300)
		Content.Place(g1)
		Content.Place(g2, TOP, border = (20, 20, 20, 20), decoration = "yes")
		Content.Place(g3, CENTER, border = (20, 20, 20, 20))
		Content.Place(g4, BOTTOM, decoration = "yes", border = (20, 0, 0, 0))
		Content.Expand()

		# draw once and set size
		Content.DrawAllDecorations(self.Frame.Panel)
		self.Frame.SetClientSize(Content.GetSize())

		return

myApp().MainLoop()
