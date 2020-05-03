# 'base.py'
# content; The App/Frame/Panel classes.
# author; Roch schanen
# created; 2020 Mars 21
# repository; https://github.com/RochSchanen/rochpygui

# wxpython: https://www.wxpython.org/
import wx

# todo: should I use "BufferedPaintDC"
#       instead of "DCPaint" at (1)

# simple Panel class
class _basePanel(wx.Panel):
    # superseed the __init__ method
    def __init__(self, parent):
        # call parent class __init__()
        wx.Panel.__init__(
            self,
            parent = parent,
            id     = wx.ID_ANY,
            pos    = wx.DefaultPosition,
            size   = wx.DefaultSize,
            style  = wx.NO_BORDER,
            name   = "")
        # BackgroundBitmap
        self.BackgroundBitmap = None
        # bind paint event
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        # done
        return

    def _OnPaint(self, event):
        # redraw if BackgroundBitmap is defined
        if self.BackgroundBitmap: 
            dc = wx.PaintDC(self) # (1)
            dc.DrawBitmap(self.BackgroundBitmap, 0, 0)
        return

# simple Frame class
class _baseFrm(wx.Frame):
    # superseed the __init__ method
    def __init__(self):
        # call parent class __init__()
        wx.Frame.__init__(
            self,
            parent = None,
            id     = wx.ID_ANY,
            title  = "",
            pos    = wx.DefaultPosition,
            size   = wx.DefaultSize,
            style  = wx.DEFAULT_FRAME_STYLE
                    ^ wx.RESIZE_BORDER
                    ^ wx.MAXIMIZE_BOX,
            name   = "")
        # Create panel
        self.Panel = _basePanel(self)
        # done
        return

# set _ESCAPE = True to allow the ESCAPE key
#  when developping projects. The default is:
_ESCAPE = False

# simple App class
class App(wx.App):

    def OnInit(self):
        # make reference to App
        self.App = self
        # create and show Frame
        self.Frame = _baseFrm()     
        # reference to Panel
        self.Panel = self.Frame.Panel
        # call user's Start code
        self.Start()
        # adjust widow size to BackgroundBitmap size
        if self.Frame.Panel.BackgroundBitmap:
            w, h = self.Frame.Panel.BackgroundBitmap.GetSize()
            self.Frame.SetClientSize((w, h))
        # bind key event (for ESCAPE key)
        self.Bind(wx.EVT_KEY_DOWN, self._OnKeyDown)
        # show the frame
        self.Frame.Show(True)
        # done
        return True

    # User's code:
    def Start(self):
        # Superseeded Start method
        pass

    # Exit on Esc: Debugging/Development stage
    def _OnKeyDown(self, event):
        key = event.GetKeyCode()
        if _ESCAPE:
            if key == wx.WXK_ESCAPE:
                wx.Exit()
                return
        event.Skip() # forward event
        return

    # def __del__(self):
    #     return

###########################################################

# minimal sample code to create an user Application

# from base import *

# class myApp(App):

#     def Start(self):
#         # code here
#         return

# myApp().MainLoop()
