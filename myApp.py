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
from layout import LEFT, RIGHT, TOP, BOTTOM

# create app
class myApp(baseApp):

	def Start(self):

		g1 = Group(VERTICAL, 100, 100)
		g2 = Group(VERTICAL, 100, 100)
		g3 = Group(VERTICAL, 100, 100)
		g4 = Group(VERTICAL, 100, 100)

		# Content = Group()
		Content = Group(HORIZONTAL, w = 800, h = 300)

		Content.Place(g1)
		Content.Place(g2, border = (20, 20, 20, 20), decoration = "yes")
		Content.Place(g3, border = (20, 20, 20, 20))
		Content.Place(g4, decoration = "yes")
		# Content.Expand(VERTICAL)
		Content.Expand(HORIZONTAL)
		# Content.Expand(HORIZONTAL + VERTICAL)

		Content.DrawAllDecorations(self.Frame.Panel)
		self.Frame.SetClientSize(Content.GetSize())
		
		return

myApp().MainLoop()
