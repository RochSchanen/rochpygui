# 'testApp.py'
# 
# Roch schanen
# created 2020 April 06
# https://github.com/RochSchanen/rochpygui

# local imports
from base       import *
# from theme      import *
from layout     import *
# from display    import *
# from buttons    import *
# from controls   import *
from plot       import *

# create app
class myApp(App):

    def Start(self):

        # create plot
        P = Plot(self.Panel, 600, 600)

        P.SetXLabel("Generator frequency / Hz")
        P.SetXLimit(123.0019, +123.0051)
        P.SetXFormat(3, 4)
        P.SetXTicks(5)

        P.SetYLabel("Lockin output / V")
        P.SetYLimit(-1.10, +1.10)
        P.SetYFormat(1, 2)
        P.SetYTicks(9)

        # set content
        Content = Group(VERTICAL)
        Content.Place(P)

        # draw once and set size
        Content.DrawAllDecorations(self.Panel)
        return

myApp().MainLoop()
