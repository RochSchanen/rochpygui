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
from controls 	import Control

class DiodesIndicator(Control):

	def Start(self):

		# build image library
		P = PNGlib()
		P.load("Dark")
		P.SetGrid(4, 3)
		P.SetSize((28, 52))
		P.Add("G0", 1, 3)
		P.Add("G1", 2, 3)
		P.Add("R0", 3, 3)
		P.Add("R1", 4, 3)

		# create diodes
		D1 = Display(self, P, ["G0", "G1"])
		D2 = Display(self, P, ["R0", "R1"])
		D3 = Display(self, P, ["G0", "G1"])

		# save locally
		self.diodes = [D1, D2, D3]

		# build control
		Content = Group(HORIZONTAL)
		for d in self.diodes: Content.Place(d)
		
		Content.DrawAllDecorations(self)
		self.SetSize(Content.GetSize())
	
		return

	def SetValue(self, Value):
	 	for i in range(len(self.diodes)):
	 		self.diodes[i].SetValue(
	 			1 if i == Value else 0)
	 	return

# create app
class myApp(App):

	def Start(self):

		# build image library
		P = PNGlib()
		P.load("Dark")
		P.SetGrid(4, 3)
		P.SetSize((28, 52))

		P.Add("R_R0", 1, 1)
		P.Add("R_R1", 2, 1)
		P.Add("R_P0", 3, 1)
		P.Add("R_P1", 4, 1)

		P.Add("G_R0", 1, 2)
		P.Add("G_R1", 2, 2)
		P.Add("G_P0", 3, 2)
		P.Add("G_P1", 4, 2)

		# create push button and bind event
		Bpush = Push(self.Panel, P, ["G_R0", "G_P1"])
		Bpush.BindEvent(self.PushButtonEventHandler)

		# create switch button and bind event
		# BSwitch = Switch(self.Panel, P, ["R0", "R1", "P0", "P1"])
		BSwitch = Switch(self.Panel, P, ["R_R0", "R_R1", "R_P0", "R_P1"])
		BSwitch.BindEvent(self.SwitchButtonEventHandler)

		# create two radio buttons, group them and bind events
		Bradio1 = Radio(self.Panel, P, ["G_R0", "G_P1"])
		Bradio2 = Radio(self.Panel, P, ["G_R0", "G_P1"])
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

		self.DI = DiodesIndicator(self.Panel)

		# set content
		Content = Group(VERTICAL)

		Content.Place(self.DI, decoration = "Ridge", border = (0, 0, 10, 10))
		
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
		self.DI.SetValue(0)
		return

	def SwitchButtonEventHandler(self, event):
		if event.status == 1:
			print("Switch button pressed")
		if event.status == 0:
			print("Switch button released")
		self.DI.SetValue(1)
		return

	def RadioButton1EventHandler(self, event):
		if event.status == 1:
			print("Radio button 1 pressed")
		if event.status == 0:
			print("Radio button 1 released")
		self.DI.SetValue(2)
		return

	def RadioButton2EventHandler(self, event):
		if event.status == 1:
			print("Radio button 2 pressed")
		if event.status == 0:
			print("Radio button 2 released")
		self.DI.SetValue(2)
		return

myApp().MainLoop()
