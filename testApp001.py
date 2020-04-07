# 'testApp000.py'
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

class DiodesIndicator(Control):

	def Start(self):
		self.diodes = []
		Content = Group(HORIZONTAL)
		colors = ["Red", "Blue", "Green"]
		for i in range(3):
			lib, names = Theme.GetImages("LED", colors[i])
			self.diodes.append(Display(self, lib, names))
			Content.Place(self.diodes[i])
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

		# create diode indicator control
		self.d = DiodesIndicator(self.Panel)

		HEADER = Group(HORIZONTAL)
		# create push button, bind event and place
		lib, names = Theme.GetImages("Push", "Left")
		p = Push(self.Panel, lib, names)
		p.BindEvent(self.PushButtonEventHandler)
		HEADER.Place(p)

		BODY   = Group(HORIZONTAL)
		# create switch button and bind event
		lib, names = Theme.GetImages("LEDSwitch", "Blue")
		s = Switch(self.Panel, lib, names)
		s.BindEvent(self.SwitchButtonEventHandler)
		BODY.Place(s)

		FOOTER = Group(HORIZONTAL)  
		# create two radio buttons, group them and bind events
		lib, names = Theme.GetImages("LEDRadio", "Green")
		r1 = Radio(self.Panel, lib, names)
		r1.BindEvent(self.RadioButton1EventHandler)
		r2 = Radio(self.Panel, lib, names)
		r2.BindEvent(self.RadioButton2EventHandler)
		RadioCollect([r1, r2])
		FOOTER.Place(r1)
		FOOTER.Place(r2)

		# set content
		Content = Group(VERTICAL, w = 200)
		Content.Place(self.d, decoration = "Outset")
		Content.Place(HEADER, decoration = "Groove")
		Content.Place(BODY, decoration = "Ridge")
		Content.Place(FOOTER, decoration = "Inset")

		# draw once and set size
		Content.DrawAllDecorations(self.Panel)
		return

	def PushButtonEventHandler(self, event):
		print("Push Button Pressed")
		self.d.SetValue(0)
		return

	def SwitchButtonEventHandler(self, event):
		if event.status == 1:
			print("Switch button pressed")
		if event.status == 0:
			print("Switch button released")
		self.d.SetValue(1)
		return

	def RadioButton1EventHandler(self, event):
		if event.status == 1:
			print("Radio button 1 pressed")
		if event.status == 0:
			print("Radio button 1 released")
		self.d.SetValue(2)
		return

	def RadioButton2EventHandler(self, event):
		if event.status == 1:
			print("Radio button 2 pressed")
		if event.status == 0:
			print("Radio button 2 released")
		self.d.SetValue(2)
		return

myApp().MainLoop()
