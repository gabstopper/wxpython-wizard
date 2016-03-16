import wx.grid
from TextObjectValidator import TextObjectValidator

class MainWindow(wx.Frame): #View
    def __init__(self, parent, title):
    #def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, parent, title=title, size=(650,500))
        #super(MainWindow, self).__init__(*args, **kwargs)
        
        self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)
        
        self.appIcon = self.GetIcon()
        self.SetIcon(self.appIcon)
        self.tbTray = TaskBarTray( self ) 
        self.CreateStatusBar()
        
        filemenu= wx.Menu()
        self.menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        self.menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        
        menuBar = wx.MenuBar()   # Creating the menubar.
        menuBar.Append(filemenu,"&File") 
        self.SetMenuBar(menuBar) 
        
        form = wx.Panel( self, name="ParentFrameForm" )
        
        self.description = DescriptionPanel( form )
        self.fileupload  = FileUploadView( form )
        self.texteditor  = TextEditorView( form )
        self.gridview    = GridView( form )
        self.listboxview = ListBoxView( form )
        
        self.navigation  = NavigationPanel( form )
        
        self.texteditor.Hide()
        self.gridview.Hide()
        self.listboxview.Hide()
        
        main_hSizer = wx.BoxSizer( wx.VERTICAL )
        
        main_hSizer.AddSpacer( 5 ) #spacer between text and top frame
        main_hSizer.AddF( self.description, wx.SizerFlags(0).Expand())
        main_hSizer.AddF( wx.StaticLine( form ), wx.SizerFlags(0).Expand().Border(wx.ALL, 5) )
        #main_hSizer.Add( self.description, 0, wx.EXPAND)
        #main_hSizer.Add( wx.StaticLine(form), 0, wx.ALL|wx.EXPAND, 5 )
        
        main_hSizer.AddSpacer(5)  
        
        #Keep panel borders same spacing to make UI panel switching smooth
        #main_hSizer.AddF( self.fileupload, wx.SizerFlags(1).Align(wx.CENTER).Border(wx.ALL, 5) )
        main_hSizer.AddF( self.fileupload, wx.SizerFlags(1).Align(wx.CENTER).Border(wx.ALL, 5) )
        #main_hSizer.AddF( self.fileupload, wx.SizerFlags(1).Align(wx.CENTER) )
        main_hSizer.AddF( self.texteditor, wx.SizerFlags(1).Expand().Border(wx.ALL, 5) )
        main_hSizer.AddF( self.gridview, wx.SizerFlags(1).Expand().Border(wx.ALL, 5) )
        main_hSizer.AddF( self.listboxview, wx.SizerFlags(1).Expand().Border(wx.ALL, 5) )
        
        #main_hSizer.Add ( self.fileupload, 1, wx.ALIGN_CENTER, 5 ) #proportion 1 to take space matching SetMinSize
        #main_hSizer.Add ( self.texteditor, 1, wx.EXPAND, 5 )
        #main_hSizer.Add ( self.gridview, 1, wx.EXPAND, 5 )
        
        main_hSizer.AddF( wx.StaticLine( form ), wx.SizerFlags(0).Expand().Border(wx.ALL, 5) )
        main_hSizer.AddF( self.navigation, wx.SizerFlags(0).Expand() )
        #main_hSizer.Add( wx.StaticLine(form), 0, wx.ALL|wx.EXPAND,5 ) #spacer between main panel and nav
        #main_hSizer.Add( self.navigation, 0, wx.EXPAND )
        main_hSizer.AddSpacer( 3 )

        form.SetSizer( main_hSizer )
        
        self.Center()
        self.SetSizeHints(650,500) #Don't let window resize below these dimensions
    
    def GetIcon(self):
        #if os.path.exists(fileName)
        img = wx.Image('icons/elephant_256_Bfn_icon.ico', wx.BITMAP_TYPE_ICO)
        try:
            if wx.Platform == "__WXMSW__":
                print "Getting 16x16 image for Windows"
                img = img.Scale(16, 16)
            elif wx.Platform == "__WXGTK__":
                print "Getting 22x22 image for Linux"
                img = img.Scale(22,22)
            # wxMac can be any size up to 128x128, so leave the source img alone....
            icon = wx.IconFromBitmap(wx.BitmapFromImage(img))
            print "Icon dimensions, height: %s, width: %s" % (icon.GetHeight(), icon.GetWidth())
        except:
            wx.LogError("Image could not be loaded, proceeding to load with empty image")
            icon = wx.EmptyIcon()
        return icon
                
class TaskBarTray(wx.TaskBarIcon):
    TBMENU_CLOSE   = wx.NewId()
    TBMENU_ABOUT = wx.NewId()
    TBMENU_HELP = wx.NewId()
    
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        
        self.frame = frame
        self.SetIcon(self.frame.appIcon)
       
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)
    
    def CreatePopupMenu(self, evt=None):
        """
        This method is called by the base class when it needs to popup
        the menu for the default EVT_RIGHT_DOWN event.  Just create
        the menu how you want it and return it from this function,
        the base class takes care of the rest.
        """
        menu = wx.Menu()
        menu.Append(self.TBMENU_HELP, "Help")
        menu.Append(self.TBMENU_ABOUT, "About")
        menu.AppendSeparator()
        menu.Append(self.TBMENU_CLOSE,   "Quit")
        return menu
        
    def OnTaskBarActivate(self, evt):
        pass
 
    def OnTaskBarLeftClick(self, evt):
        print "OnTaskBarLeftClick"
        menu = self.CreatePopupMenu()
        self.PopupMenu(menu)
        menu.Destroy()
        
class DescriptionPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.BackgroundColour  = (200, 240, 200)      # light green
        self.instruction = "Welcome to the basic wizard. Let's add some additional blah in here and see how windows handles this. This will help you design a basic flow showing and hiding panels.thrn thr string just keeps going on on and on and on and on. On a related note, this is where the panel based description will reside"
        title = wx.StaticText( self, wx.ALL, self.instruction )
        font = wx.SystemSettings.GetFont( wx.SYS_DEFAULT_GUI_FONT )
        font.SetStyle( wx.SLANT )
        title.SetFont( font )
        title.Wrap( 500 )
        
        descriptionSizer = wx.BoxSizer( wx.HORIZONTAL )
        descriptionSizer.AddStretchSpacer(1) #center title
        descriptionSizer.Add( title, 0, wx.CENTER, 5 )
        descriptionSizer.AddStretchSpacer(1)
        
        self.SetMinSize((500, 72)) #So smaller text doesn't adjust top level panel up or down
        self.SetSizer( descriptionSizer )
   
class FileUploadView(wx.Panel):
    UPLOAD = wx.NewId()
    UPLOAD_TXT = wx.NewId()
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.BORDER_DEFAULT)
   
        self.BackgroundColour = ("yellow")
        vertSizer = wx.BoxSizer(wx.VERTICAL) #wrap the staticbox and sizer
        
        box = wx.StaticBox(self, wx.ID_ANY, "This is an example file browse window")
        boxSizer = wx.StaticBoxSizer( box, wx.VERTICAL )
        
        hbox = wx.BoxSizer( wx.HORIZONTAL ) 
        hbox.Add( wx.StaticText( self, wx.ID_ANY, "Does Kiley like elephants: " ))
        hbox.AddStretchSpacer(1)
        hbox.Add( wx.TextCtrl( self, self.UPLOAD_TXT, size=(140, -1), validator=TextObjectValidator(self) ))
        hbox.Add( wx.Button( self, self.UPLOAD, 'Test' ))
        
        hbox2 = wx.BoxSizer( wx.HORIZONTAL ) 
        hbox2.Add( wx.StaticText( self, wx.ID_ANY, "Does anyone like elephants: " ))
        hbox2.AddStretchSpacer(1)
        hbox2.Add( wx.TextCtrl( self, size=(140, -1) ))
        hbox2.Add( wx.Button( self, wx.ID_ANY, 'Test' ) )
        
        hbox3 = wx.BoxSizer( wx.HORIZONTAL ) 
        hbox3.Add( wx.StaticText( self, wx.ID_ANY, "Click to add the file oh yea extend: " ))
        hbox3.AddStretchSpacer(1)
        hbox3.Add( wx.TextCtrl( self, size=(140, -1) ))
        hbox3.Add( wx.Button( self, wx.ID_ANY, 'Submit' ) )
        
        hbox4 = wx.BoxSizer ( wx.HORIZONTAL )
        hbox4.AddSpacer(5)
        
        #This will expand the controls left to right evenly
        boxSizer.Add( hbox, 0, wx.EXPAND, 5 )
        boxSizer.AddSpacer(5)
        boxSizer.Add( hbox2, 0, wx.EXPAND, 5 )
        boxSizer.AddSpacer(5)
        boxSizer.Add( hbox3, 0, wx.EXPAND, 5 )
        boxSizer.AddSpacer(5)
        boxSizer.Add( hbox4, 0, wx.EXPAND, 5 )
      
        vertSizer.Add( boxSizer )
        self.SetSizer( vertSizer )

class TextEditorView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
    
        self.BackgroundColour = ("yellow")
        font = wx.SystemSettings.GetFont( wx.SYS_DEFAULT_GUI_FONT )
        
        boxSizer = wx.BoxSizer( wx.VERTICAL )         
        
        txt = wx.StaticText( self, wx.ID_ANY, "Enter some data here: " )
        txt.SetFont( font )
        self.ctrl = wx.TextCtrl( self, wx.ID_ANY, style=wx.TE_MULTILINE)
      
        hbox = wx.BoxSizer( wx.HORIZONTAL ) 
        hbox.Add( txt )
       
        boxSizer.Add(hbox, 0, wx.EXPAND)
        boxSizer.AddSpacer(5)
        boxSizer.Add( self.ctrl, 1, wx.EXPAND )
        boxSizer.AddSpacer(5)
        
        self.SetSizer( boxSizer )

class ListBoxView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.BackgroundColour = ("pink")
        picks= ['first', 'second', 'third']
        leftbox = wx.CheckListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choices=picks, name="leftbox")
        rightbox = wx.CheckListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choices=picks, name="leftbox")
        
        vbox = wx.BoxSizer( wx.VERTICAL )
        hbox = wx.BoxSizer( wx.HORIZONTAL )
        hbox.AddStretchSpacer(1)
        hbox.Add( leftbox )
        hbox.Add( rightbox )
        hbox.AddStretchSpacer(1)
              
        vbox.AddF( hbox, wx.SizerFlags(0).Expand() )
      
        self.SetSizer( vbox )
                        
class NavigationPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.BackgroundColour  = ("light blue")      # light blue 
        navSizer = wx.BoxSizer ( wx.HORIZONTAL )
        
        self.cancelClick = wx.Button( self, wx.ID_ANY, 'Cancel' )
        self.backClick = wx.Button( self, wx.ID_ANY, 'Back' )
        self.nextClick = wx.Button( self, wx.ID_ANY, 'Next' )
        self.finishClick = wx.Button( self, wx.ID_ANY, 'Finish' )
        navSizer.Add( self.cancelClick, 0, wx.ALL, 5 )
        navSizer.AddStretchSpacer(1)
        navSizer.Add( self.backClick, 0, wx.ALL, 5 )
        navSizer.Add( self.nextClick, 0, wx.ALL, 5 )
        navSizer.Add( self.finishClick, 0, wx.ALL, 5)
        
        self.finishClick.Hide()
        self.backClick.Hide()
        
        self.SetSizer( navSizer )

class GridView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        hsizer = wx.BoxSizer ( wx.HORIZONTAL )
               
        grid = wx.grid.Grid(self, wx.ID_ANY)
        grid.CreateGrid(100, 10) #x=10, y=100 (rows by columns)
       
        grid.SetColLabelSize(15)
        grid.SetRowLabelSize(35)
        grid.SetCellRenderer(0,0,wx.grid.GridCellAutoWrapStringRenderer())
       
        grid.SetCellValue(0, 0, 'wxGrid is good')
        grid.SetCellValue(0, 3, 'This is read.only')
        grid.SetReadOnly(0, 3)

        # Colours can be specified for grid cell contents
        grid.SetCellValue(3, 3, 'blue on grey')
        grid.SetCellTextColour(3, 3, wx.BLUE)
        grid.SetCellBackgroundColour(3, 3, wx.LIGHT_GREY)

        # We can specify the some cells will store numeric
        # values rather than strings. Here we set grid column 5
        # to hold floating point values displayed with width of 6
        # and precision of 2
        grid.SetColFormatFloat(5, 6, 2)
        grid.SetCellValue(0, 6, '3.1415')

        hsizer.Add( grid )
        self.SetSizer( hsizer )