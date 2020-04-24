# 'theme.py'
# content; Theme class and default.
# author; Roch schanen
# created; 2020 April 05
# repository; https://github.com/RochSchanen/rochpygui

# wxpython: https://www.wxpython.org/
import wx

BackgroundColour = wx.Colour( 60,  60,  60)
TextColour       = wx.Colour(150, 150, 150)

_ImageLibraries = {

    # used by: "layout.py"
    "Decoration":{
        "path"      :"606060_DECOR.png",
        "Grid"      : (2, 2),
        "Size"      : (64, 64),
        "Offset"    : (0, 0),
        "Border"    : (8, 8, 8, 8),
        # sets:
        "Groove"    : [(1, 2)],
        "Ridge"     : [(1, 1)],
        "Inset"     : [(2, 2)],
        "Outset"    : [(2, 1)],
    },

    # used by: "plot.py"
    "Graph":{
        "path"      :"606060_GRAPH.png",
        "Grid"      : (4, 4),
        "Size"      : (62, 62),
        "Offset"    : (0, 0),
        # sets:
        "Drag"      : [(1, 1), (1, 2), (1, 1), (1, 2)],
        "Expand"    : [(2, 1), (2, 2), (2, 1), (2, 2)],
        "Shrink"    : [(3, 3), (3, 4), (3, 3), (3, 4)],
        "Yfit"      : [(1, 3), (1, 4), (1, 3), (1, 4)],
        "Xfit"      : [(2, 3), (2, 4), (2, 3), (2, 4)],
        "X Expand"  : [(3, 1), (3, 2), (3, 1), (3, 2)],
        "Y Expand"  : [(4, 1), (4, 2), (4, 1), (4, 2)],
        "Measure"   : [(4, 3), (4, 4), (4, 3), (4, 4)]
    },

    # used by: "display.py", "buttons.py"
    "Round LED":{
        "path"      :"606060_LED.png",
        "Grid"      : (8, 2),
        "Size"      : (20, 20),
        "Offset"    : (0, 0),
        # sets:
        "Red"       : [(1, 1), (2, 1)],
        "Green"     : [(3, 1), (4, 1)],
        "Blue"      : [(5, 1), (6, 1)],
        "Yellow"    : [(1, 2), (2, 2)],
        "White"     : [(3, 2), (4, 2)],
    },

    "Push":{
        "path"      :"606060_PUSH.png",
        "Grid"      : (8, 2),
        "Size"      : (28, 28),
        "Offset"    : (0, 0),
        # sets:
        "Blank"     : [(1, 1), (2, 1)],
        "Down"      : [(1, 2), (2, 2)],
        "Left"      : [(3, 2), (4, 2)],
        "Up"        : [(5, 2), (6, 2)],
        "Right"     : [(7, 2), (8, 2)],
    },

    "LEDSwitch":{
        "path"      :"606060_SWITCH.png",
        "Grid"      : (8, 3),
        "Size"      : (28, 52),
        "Offset"    : (0, 0),
        # sets:
        "Red"       : [(5, 1), (6, 1), (7, 1), (8, 1)],
        "Blue"      : [(1, 2), (2, 2), (3, 2), (4, 2)],
        "Green"     : [(5, 2), (6, 2), (7, 2), (8, 2)],
        "White"     : [(1, 3), (2, 3), (3, 3), (4, 3)],
        "Yellow"    : [(5, 3), (6, 3), (7, 3), (8, 3)]
    },

    "LEDRadio":{    # same as LEDSwitch but with only two states.
        "path"      :"606060_SWITCH.png",
        "Grid"      : (8, 3),
        "Size"      : (28, 52),
        "Offset"    : (0, 0),
        # sets:
        "Red"       : [(5, 1), (8, 1)],
        "Blue"      : [(1, 2), (4, 2)],
        "Green"     : [(5, 2), (8, 2)],
        "White"     : [(1, 3), (4, 3)],
        "Yellow"    : [(5, 3), (8, 3)]
    },

    # used by "graph.py", "plot.py"
   "DOT":{
        "path"      :"000000_DOT.png",
        "Grid"      : (4, 4),
        "Size"      : (25, 25),
        "Offset"    : (0, 0),
        # sets:
        "White"     : [(1, 1), (2, 1), (3, 1), (4, 1)],
        "Blue"      : [(1, 2), (2, 2), (3, 2), (4, 2)],
        "Red"       : [(1, 3), (2, 3), (3, 3), (4, 3)],
        "Green"     : [(1, 4), (2, 4), (3, 4), (4, 4)]
    }

}

# Extract and store bitmaps from png files
class _lib():

    def __init__(self):
        self.pngs   = {}
        self.Grid   = 1, 1
        self.Size   = None
        self.Offset = 0, 0
        return

    def Load(self, path):
        self.Sample = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        return

    # p is the number of columns
    # q is the number of lines
    def SetGrid(self, Grid):
        self.Grid = Grid
        return

    # default None ()
    def SetSize(self, Size):
        self.Size = Size
        return

    # default is None
    def SetOffset(self, Offset):
        self.Offset = Offset
        return

    # add bitmap to the dictionary
    # from the grid index
    def Add(self, Name, Position):
        # get parameters
        m, n = Position
        X, Y = self.Offset
        p, q = self.Grid
        W, H = self.Sample.GetSize()
        # get grid size
        P, Q = W/p, H/q
        # get image size
        w, h = (P, Q) if self.Size == None else self.Size
        # get clipping origin
        x, y = (m-1)*P + (P-w)/2 + X , (n-1)*Q + (Q-h)/2 + Y
        # set clip geometry
        Clip = wx.Rect(x, y, w, h)
        # clip and store new image and name
        self.pngs[Name] = self.Sample.GetSubBitmap(Clip)
        return

    #  get bitmap(s) from the dictionary by name(s)
    def Get(self, names):
        # return single image
        if not isinstance(names, list):
            return self.pngs[names]
        # return list of images
        pngs = []
        for name in names:
            pngs.append(self.pngs[name])
        # done
        return pngs

_fontLibrary = {
    "Helvetica":{
        "size"      : 12,
        "familly"   : wx.FONTFAMILY_ROMAN,
        "style"     : wx.FONTSTYLE_NORMAL,
        "weight"    : wx.FONTWEIGHT_NORMAL,
        "underline" : False,
        "faceName"  : "Helvetica",
        "encoding"  : wx.FONTENCODING_DEFAULT
    }    
}

class _Theme():

    def __init__(self):
        self.path   = "./resources/themes/dark/"
        self.libs   = {}
        self.fonts  = {}
        return

    def GetFont(self, FontName = "Helvetica"):
        if FontName in _fontLibrary:
            ref = _fontLibrary[FontName]
            siz = ref["size"]
            fam = ref["familly"]
            sty = ref["style"]
            wei = ref["weight"]
            und = ref["underline"]
            fac = ref["faceName"]
            enc = ref["encoding"]
            font = wx.Font(siz,fam,sty,wei,und,fac,enc)
        else:
            print("in 'theme.py',")
            print("undefined FontName '%s'." % FontName)
            font = None
        # done
        return font

    def GetValue(self, libName, valName):
        # check libName exists
        if libName in _ImageLibraries.keys():
            ref = _ImageLibraries[libName]
            # check setName exists in libName
            if valName in ref.keys():
                value = ref[valName]
            else:
                print("in 'theme.py',")
                print("in libName '%s'," % libName)
                print("Undefined valName '%s'." % valName)
                value = None
        else:
            print("in 'theme.py',")
            print("undefined libName '%s'." % libName)
            value =  None
        return value

    def GetImages(self, libName, setName):
        # check libName exists
        if libName in _ImageLibraries.keys():
            ref = _ImageLibraries[libName]
            # check setName exists in libName
            if setName in ref.keys():
                imageSet = ref[setName]
                # check libName instance
                if libName in self.libs.keys():
                    lib = self.libs[libName]
                    # collect set
                    names = []
                    l = len(setName)-1
                    for name in lib.pngs.keys():
                        if name[0:l] == setName:
                            names.append(name)
                    # no image found -> add new set
                    if not names:
                        for i in range(len(imageSet)):
                            Name = setName+"_"+str(i)
                            Position = imageSet[i]
                            lib.Add(Name, Position)
                            names.append(Name)
                # instanciate libName and SetName
                else:
                    # create new lib
                    lib = _lib()
                    lib.Load(self.path+ref["path"])
                    lib.SetOffset(ref["Offset"])
                    lib.SetGrid(ref["Grid"])
                    lib.SetSize(ref["Size"])
                    # add new set of images (indexed)
                    names = []
                    for i in range(len(imageSet)):
                        Name = setName+"_"+str(i)
                        Position = imageSet[i]
                        lib.Add(Name, Position)
                        names.append(Name)
                    # instanciate
                    self.libs[libName] = lib
            else:
                print("in 'theme.py',")
                print("in libName '%s'," % libName)
                print("Undefined setName '%s'." % setName)
                lib, names =  None, None
        else:
            print("in 'theme.py',")
            print("undefined libName '%s'." % libName)
            lib, names =  None, None

        return lib, names

Theme = _Theme()
