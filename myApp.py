# 'myapp.py'
# user's code
# Roch schanen
# created 2020 March 21
# https://github.com/RochSchanen/rochpygui

# local imports
from base		import *
from layout		import *
from display 	import *
from buttons	import *

# create app
class myApp(App):

	def Start(self):

		# build image library
		P = PNGlib()
		P.load("test")
		P.SetGrid(1, 2)
		P.SetSize((50, 50))
		P.SetOffset(27, -27)
		P.Add("Off", 1, 1)
		P.SetOffset(23, -18)
		P.Add("On", 1, 2)

		# create push button and bind event
		Bpush = Push(self.Panel, P, ["Off", "On"])
		Bpush.BindEvent(self.PushButtonEventHandler)

		# create switch button and bind event
		BSwitch = Switch(self.Panel, P, ["Off", "On"])
		BSwitch.BindEvent(self.SwitchButtonEventHandler)

		# create two radio buttons, group them and bind events
		Bradio1 = Radio(self.Panel, P, ["Off", "On"])
		Bradio2 = Radio(self.Panel, P, ["Off", "On"])
		# Bradio2 = Switch(self.Panel, P, ["Off", "On"])
		RadioCollect([Bradio1, Bradio2])
		Bradio1.BindEvent(self.RadioButton1EventHandler)
		Bradio2.BindEvent(self.RadioButton2EventHandler)

		HEADER = Group(HORIZONTAL)
		BODY   = Group(HORIZONTAL)
		FOOTER = Group(HORIZONTAL)  

		HEADER.Place(Bpush)
		BODY.Place(BSwitch)
		FOOTER.Place(Bradio1)
		FOOTER.Place(Bradio2)

		# set content
		Content = Group(VERTICAL)

		Content.Place(HEADER, decoration = "Groove")
		Content.Place(BODY,   decoration = "Groove")
		Content.Place(FOOTER, decoration = "Groove")

		# expand
		Content.Expand()

		# draw once and set size
		Content.DrawAllDecorations(self.Panel)

		return

	def PushButtonEventHandler(self, event):
		print("Push Button Pressed")
		return

	def SwitchButtonEventHandler(self, event):
		if event.status == 1:
			print("Switch button pressed")
		if event.status == 0:
			print("Switch button released")
		return

	def RadioButton1EventHandler(self, event):
		if event.status == 1:
			print("Radio button 1 pressed")
		if event.status == 0:
			print("Radio button 1 released")
		return

	def RadioButton2EventHandler(self, event):
		if event.status == 1:
			print("Radio button 2 pressed")
		if event.status == 0:
			print("Radio button 2 released")
		return

myApp().MainLoop()
