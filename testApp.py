# 'testApp.py'
# 
# Roch schanen
# created 2020 April 06
# https://github.com/RochSchanen/rochpygui

# local imports
from base       import *
from theme      import *
from layout     import *
from display    import *
from buttons    import *
from controls   import *

from plot import _plot

# create app
class myApp(App):

    def Start(self):

        # create plot
        P = _plot(self.Panel, 500, 500)

        # set content
        Content = Group(VERTICAL)
        Content.Place(P)

        # draw once and set size
        Content.DrawAllDecorations(self.Panel)
        return

myApp().MainLoop()
