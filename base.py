# 'base.py'
# content; The App/Frame/Panel classes.
# author; Roch schanen
# created; 2020 Mars 21
# repository; https://github.com/RochSchanen/rochpygui

# wxpython: https://www.wxpython.org/
import wx

# todo: use "BufferedPaintDC" instead of "DCPaint" ?

# modified Panel class
class _basePanel(wx.Panel):

    # superseed the __init__ method
    def __init__(self, parent):

        wx.Panel.__init__(
            self,
            parent = parent,
            id     = wx.ID_ANY,
            pos    = wx.DefaultPosition,
            size   = wx.DefaultSize,
            style  = wx.NO_BORDER,
            name   = "")

        # create BackgroundBitmap NULL reference
        self.BackgroundBitmap = None

        # bind paint event
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        return

    def _OnPaint(self, event):
        # draw only if bitmap is defined
        if self.BackgroundBitmap: 
            dc = wx.PaintDC(self) # BufferedPaintDC ?
            dc.DrawBitmap(self.BackgroundBitmap, 0, 0)
        return

# modified Frame class
class _baseFrm(wx.Frame):

    # superseed the __init__ method
    def __init__(self):

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
        return

# allow ESCAPE sequence when developping projects
ESCAPE = True

# modified App class
class App(wx.App):

    def OnInit(self):

        # Reference to App
        self.App = self
        # create and show Frame
        self.Frame = _baseFrm()     
        # reference to Panel
        self.Panel = self.Frame.Panel

        # user's Start
        self.Start()

        # adjust sizes
        if self.Frame.Panel.BackgroundBitmap:
            w, h = self.Frame.Panel.BackgroundBitmap.GetSize()
            self.Frame.SetClientSize((w, h))

        # bind key event
        self.Bind(wx.EVT_KEY_DOWN, self._OnKeyDown)

        # show result now
        self.Frame.Show(True)

        return True

    # to be Superseeded by user's code:
    def Start(self):
        pass

    # Exit on Esc: Debugging/Development stage
    def _OnKeyDown(self, event):
        key = event.GetKeyCode()
        if ESCAPE:
            if key == wx.WXK_ESCAPE: wx.Exit()
        else: event.Skip() # forward event
        return
