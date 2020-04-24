# 'testApp.py'
# 
# Roch schanen
# created 2020 April 06
# https://github.com/RochSchanen/rochpygui

# local imports
from base       import *
from layout     import *
from plot       import *
from visa       import *

from SR830 import _panel as lock_in

print(' ----------------------------------------------------')

# create app
class myApp(App):

    def Start(self):

        # LOCK-IN
        LOCKIN = lock_in(self.Panel)
        LOCKIN.SetVisa(VISA.open_resource('GPIB0::14::INSTR'))

        # INTERACTIVE GRAPH
        Full_Width =  0.0037
        Center     =  123.163
        Height     =  0.780
        lv, rv     = -2.5*Full_Width, +2.5*Full_Width
        npts       =  67.0
        t = linspace(Center+lv, Center+rv, npts)
        s = (t-Center)/Full_Width*2
        x = Height/(1+s**2);
        y = Height*s/(1+s**2)
        IG = InteractiveGraph(self.Panel)
        IG.Graph.SetXLabel("Generator frequency / Hz")
        IG.Graph.SetXLimit(123.151, +123.175)
        IG.Graph.SetXFormat(3, 3)
        IG.Graph.SetXTicks(5)
        IG.Graph.SetYLabel("Lockin output / V")
        IG.Graph.SetYLimit(-0.51, +0.9)
        IG.Graph.SetYFormat(1, 2)
        IG.Graph.SetYTicks(9)
        Vx = IG.Graph.AddBufferedPlot()
        Vx.SetData(t, x)
        Vx.SetPointStyle(['RED','SMALL'])
        Vy = IG.Graph.AddPlot()
        Vy.SetData(t, y)
        Vy.SetPointStyle(['BLUE','SMALL'])
        IG.Graph.RefreshBuffer()

        # set content
        Content = Group(HORIZONTAL)
        Content.Place(IG, decoration = 'Outset')
        Content.Place(LOCKIN, decoration = 'Outset')

        # done
        Content.DrawAllDecorations(self.Panel)
        return

myApp().MainLoop()

print(' ----------------------------------------------------')

