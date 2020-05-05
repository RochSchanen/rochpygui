# 'testApp.py'
# 
# Roch schanen
# created 2020 April 06
# https://github.com/RochSchanen/rochpygui

# numpy: https://numpy.org/
from numpy import linspace

# IMPORTS
from base       import *
from layout     import *
from plot       import *
from visa       import *

from SR830    import _panel as lock_in
from AG33521A import _panel as generator 

print('----------------------------------------------------')
# "Escape key" shuts down App (during development)
import base
base._ESCAPE = True

# create App
class myApp(App):

    def Start(self):
        # instantiate generator
        GNTR = generator(self.Panel)
        GNTR.SetVisa(VISA.open_resource('GPIB0::06::INSTR'))
        # instantiate lock-in
        LCKN = lock_in(self.Panel)
        LCKN.SetVisa(VISA.open_resource('GPIB0::14::INSTR'))
        SETUP = Group(VERTICAL)
        SETUP.Place(GNTR, deco = 'Outset')
        SETUP.Place(LCKN, deco = 'Outset')
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
        IG.Graph.SetYLabel("Lock-in output / V")
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
        # set-up Main
        Main = Group(HORIZONTAL)
        Main.Place(IG,    deco = 'Outset')
        Main.Place(SETUP, deco = None)
        # set-up content
        content = Group(VERTICAL)
        content.Place(Main)
        # expansion
        content.Expand()
        Main.Expand()
        # SETUP.Expand()
        # done
        content.DrawAllDecorations(self.Panel)
        return

myApp().MainLoop()

print('----------------------------------------------------')

