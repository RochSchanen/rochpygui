# 'colors.py'
# color definitions
# Roch schanen
# created 2017 sept 22

# wxpython: https://www.wxpython.org/
import wx

TextColor 		= wx.Colour(255, 255, 255)
BackgroundColor = wx.Colour( 80,  80,  80)

def dcClear(dc, x, y, w, h):

	dc.SetPen(wx.Pen(
		wx.Colour(150,0,0), 
		width = 1,
		style = wx.PENSTYLE_SOLID))

	# dc.SetPen(wx.TRANSPARENT_PEN)

	dc.SetBrush(wx.Brush(BackgroundColor, wx.SOLID))
	dc.DrawRectangle(x, y, w, h)
	return

def dcMark(dc, x, y, w, h):
	
	dc.SetBrush(wx.Brush(
		BackgroundColor, 
		wx.SOLID))
	
	dc.SetPen(wx.Pen(
		wx.Colour(150, 150, 150), 
		width = 1,
		style = wx.PENSTYLE_SOLID))

	dc.DrawRectangle(x, y, w, h)

	dc.SetPen(wx.Pen(
		wx.Colour(150, 0, 0), 
		width = 1,
		style = wx.PENSTYLE_SOLID))

	dc.DrawRectangle(x+5, y+5, w-2*5, h-2*5)

	return

# wx.Pen:

# properties:

# Cap
# Colour
# Dashes
# Join
# Stipple
# Style
# Width

# get properties
# GetCap, CAP_ROUND, CAP_PROJECTING, CAP_BUTT
# GetColour
# GetDashes
# GetJoin, JOIN_BEVEL, JOIN_ROUND, JOIN_MITER
# GetStipple
# GetStyle
# GetWidth

# Set properties:
# SetCap, CAP_ROUND, CAP_PROJECTING, CAP_BUTT
# SetColour
# SetDashes
# SetJoin, JOIN_BEVEL, JOIN_ROUND, JOIN_MITER
# SetStipple, Sets the bitmap for stippling
# SetStyle
# SetWidth

# Check Pen

# IsNonTransparent: Returns True if the pen is a valid non-transparent pen.
# IsOk: Returns True if the pen is initialised.
# IsTransparent: Returns True if the pen is transparent.
