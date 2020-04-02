# 'myapp.py'
# user's code
# Roch schanen
# created 2020 March 21
# https://github.com/RochSchanen/rochpygui

# local imports
from base		import *
from layout		import *
from display	import PNGlib, Display

# create app
class myApp(App):

	def Start(self):

		# build image library
		P = PNGlib()
		P.load("test")
		P.SetGrid(1, 2)
		P.SetSize((110, 100))
		P.Add("img1", 1, 1)
		P.Add("img2", 1, 2)

		# create two diplays (each can display two images)
		# use images of the same size for the same display control
		D1 = Display(self.Panel, P, ["img1", "img2"])
		D2 = Display(self.Panel, P, ["img1", "img2"])

		HEADER = Group(HORIZONTAL)

		BODY   = Group(HORIZONTAL)
		BODY.Place(D1)
		BODY.Place(D2)

		FOOTER = Group(HORIZONTAL)  

		# set display value
		D1.SetValue("img1")
		D2.SetValue("img2")

		# set content
		Content = Group(VERTICAL)

		Content.Place(HEADER, decoration = "Groove")
		Content.Place(BODY,   decoration = "Groove")
		Content.Place(FOOTER, decoration = "Groove")

		# expand
		# Content.Expand()

		# draw once and set size
		Content.DrawAllDecorations(self.Panel)

		return

myApp().MainLoop()
