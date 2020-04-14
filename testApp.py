# 'testApp.py'
# 
# Roch schanen
# created 2020 April 06
# https://github.com/RochSchanen/rochpygui

# local imports
from base       import *
# from theme      import *
from layout     import *
from display    import *
# from buttons    import *
# from controls   import *
from plot       import *

from numpy import linspace

# create app
class myApp(App):

    def Start(self):
 
        # some Lorentzian lines to plot

        # shape parameters
        Full_Width =  0.0037
        Center     =  123.163
        Height     =  0.780
        lv, rv     = -2.5*Full_Width, +2.5*Full_Width
        npts       =  31.0

        # make lines
        t = linspace(Center+lv, Center+rv, npts)
        s = (t-Center)/Full_Width 
        x = Height/(1+s**2);
        y = Height*s/(1+s**2)

        # create plot
        G = GraphicScreen(self.Panel, 600, 600)

        G.SetXLabel("Generator frequency / Hz")
        G.SetXLimit(123.151, +123.175)
        G.SetXFormat(3, 3)
        G.SetXTicks(5)

        G.SetYLabel("Lockin output / V")
        G.SetYLimit(-0.51, +0.9)
        G.SetYFormat(1, 2)
        G.SetYTicks(9)

        # add plot
        Vx = G.bufferGraph.AddPlot('Vx', t, x)
        Vy = G.OnPaintGraph.AddPlot('Vy', t, y)

        Vx.SetPointStyle(['RED'])
        Vy.SetPointStyle(['BLUE'])

        Vx.SetLineStyle(['DOT'])
        Vy.SetLineStyle(['THICK'])

        G.RefreshBuffer()

        # set content
        Content = Group(VERTICAL)
        # Content.Place(D)
        Content.Place(G)

        # draw once and set size
        Content.DrawAllDecorations(self.Panel)
        return

myApp().MainLoop()
