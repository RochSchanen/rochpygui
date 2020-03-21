# 'myapp.py'
# user's code
# Roch schanen
# created 2020 March 21
# https://github.com/RochSchanen/rochpygui

# minimum code to start an interface:

# local imports
from base import baseApp, startApp

# create app
class myApp(baseApp):

	def Start(self):
		# here the start up code
		pass

startApp(myApp)
