# 'myapp.py'
# user's code
# Roch schanen
# created 2020 March 21
# https://github.com/RochSchanen/rochpygui

# minimum code to start an interface:

# local imports
from base   import baseApp
from colors import BackgroundColor
from layout import Group, HORIZONTAL, VERTICAL

# create app
class myApp(baseApp):

	def Start(self):

		g1 = Group(VERTICAL, 100, 100)
		g2 = Group(VERTICAL, 100, 100)


		Content = Group(HORIZONTAL)
		Content.Place(g1)
		Content.Place(g2, decoration = "yes")

		Content.DrawAllDecorations(self.Frame.Panel)
		self.Frame.SetClientSize(Content.GetSize())
		
		return

myApp().MainLoop()
