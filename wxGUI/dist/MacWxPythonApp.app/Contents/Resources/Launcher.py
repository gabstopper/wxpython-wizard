import wx
import os
from wx.lib.wordwrap import wordwrap
from PanelTracker import PanelTracker
from GUI import MainWindow

print wx.version()

class Model:
    def __init__(self):
        pass #This will reference class objects for each data set collected

class Controller:
    def __init__(self, app):
        self.model = Model()

        self.app = app
        print "Default system font: %s" % wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT).GetFaceName()
        
        self.view = MainWindow(None, "Test GUI File Parser and JSON Convertor")
        self.view.Show()
        
        self.page = PanelTracker([
                                  self.view.fileupload,
                                  self.view.texteditor,
                                  self.view.gridview,
                                  self.view.listboxview
                                  ])
        
        self.view.Bind(wx.EVT_CLOSE, self.OnClose)
        self.view.Bind(wx.EVT_MENU, self.OnAbout, self.view.menuAbout)
        self.view.Bind(wx.EVT_MENU, self.OnMenuExit, self.view.menuExit)
        
        self.view.tbTray.Bind(wx.EVT_MENU, self.OnAbout, id=self.view.tbTray.TBMENU_ABOUT)
        self.view.tbTray.Bind(wx.EVT_MENU, self.OnTaskBarHelp, id=self.view.tbTray.TBMENU_HELP)
        self.view.tbTray.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.view.tbTray.TBMENU_CLOSE)
        
        self.view.fileupload.Bind(wx.EVT_BUTTON, self.OnFileUpload, id=self.view.fileupload.UPLOAD)
        
        self.view.navigation.Bind(wx.EVT_BUTTON, self.OnCancel, self.view.navigation.cancelClick)
        self.view.navigation.Bind(wx.EVT_BUTTON, self.OnNext, self.view.navigation.nextClick)
        self.view.navigation.Bind(wx.EVT_BUTTON, self.OnFinish, self.view.navigation.finishClick)
        self.view.navigation.Bind(wx.EVT_BUTTON, self.OnBack, self.view.navigation.backClick)
            
    def OnFileUpload(self, event):
        wildcard = 'Python source (*.py)|*.py'
        dlg = wx.FileDialog(None, message="Choose a Python file", defaultDir=os.getcwd(),
            defaultFile="", wildcard=wildcard, style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            ctrl = self.view.FindWindowById(self.view.fileupload.UPLOAD_TXT)
            ctrl.WriteText(path)
            ctrl.SetBackgroundColour("light blue")
            print "OnFileUpload Called by %s, returned path: %s" % (event.GetEventObject(), path)
        dlg.Destroy()
    
    def OnCancel(self, event):
        print "Cancel clicked by user"
        dlg = wx.MessageDialog( self.view, "Are you sure you want to exit?", 
            "Cancel pressed", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
        reply = dlg.ShowModal()
        if reply == wx.ID_YES:
            dlg.Destroy()
            self.view.Close(True) #No veto in OnClose
        dlg.Destroy() 
        
    def OnNext(self, event):
        if self.page.current.Validate():    #Validate current page before advancing
            self.view.Freeze()
            self.page.current.Hide()
            self.page.next.Show()
            print "Current page is now: %s"%self.page.current
            self.page.current.GetParent().Layout()  #now current
            self.view.navigation.backClick.Show()
            if self.page.isLast:
                self.view.navigation.nextClick.Hide()
                self.view.navigation.finishClick.Show()
            self.view.navigation.Layout()
            self.view.Thaw()
    
    def OnBack(self, event):
        self.view.Freeze()
        self.page.current.Hide()
        self.page.previous.Show()
        print "Current page is now: %s, isFirst: %s" % (self.page.current,self.page.isFirst)
        self.page.current.GetParent().Layout()
        if self.page.isFirst:
            if self.view.navigation.backClick.IsShown():
                self.view.navigation.backClick.Hide()
            if self.view.navigation.finishClick.IsShown():
                self.view.navigation.finishClick.Hide()
            if not self.view.navigation.nextClick.IsShown():
                self.view.navigation.nextClick.Show()
        else:
            if not self.view.navigation.backClick.IsShown():
                self.view.navigation.backClick.Show()
            if not self.view.navigation.nextClick.IsShown():
                self.view.navigation.nextClick.Show()
            if self.view.navigation.finishClick.IsShown():
                self.view.navigation.finishClick.Hide()
        self.view.navigation.Layout()
        self.view.Thaw() 
                   
    def OnFinish(self, event):
        print "Finish clicked, close app, maybe prompt user to save any data if necessary"    
        
    def OnAbout(self, event):
        aboutinfo = wx.AboutDialogInfo()
        aboutinfo.Name = "My About Box"
        aboutinfo.Version = "1.0.0 Beta"
        aboutinfo.Copyright = "(C) 2016 S'up yo"
        aboutinfo.Description = wordwrap(
            "This is an example application written in wxPython to "
            "act as a step-by-step wizard",
            350, wx.ClientDC(self.view))
        aboutinfo.Developers = ["David LePage"]
        aboutinfo.License = wordwrap("Completely and totally open source!", 550, wx.ClientDC(self.view))
        wx.AboutBox(aboutinfo)
       
    def OnTaskBarHelp(self, event):
        print "Clicked Help"
    
    def OnTaskBarClose(self, evt):
        print "TaskBarClose, calling close here"
        self.view.Close(True)  #prevent veto
           
    def OnExit(self, event):
        print "Called OnExit"
        self.view.Close()
    
    def OnMenuExit(self, event):
        print "Called OnMenuExit"
        self.view.Close(True)
            
    def OnClose(self, event):
        print "Controller ->Can Veto in OnClose: %s, id: %s" % (event.CanVeto(),event.GetId())
        if event.CanVeto():
            print "Can veto, going to lower window"
            if wx.Platform == "__WXMSW__":
                self.view.Close(True)
            else:
                self.app.BringWindowToLower() #Mac, lower to dock
        else:
            self.view.tbTray.RemoveIcon()
            if wx.Platform == "__WXMSW__":  #Seems to be required for Windows. On mac, when closed from dock a second call will segfault when closed from dock
                self.view.tbTray.Destroy()
            self.view.Destroy()
                
class MyApp(wx.App):    #Override to support Mac
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)

        # This catches events when the app is asked to activate by some other process
        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)
        
    def MacReopenApp(self):
        """Called when the doc icon is clicked, and ???"""
        print "Mac Dock item clicked, reoping app"
        self.GetTopWindow().Raise()

    def OnActivate(self, event):
        # if this is an activate event, rather than something else, like iconize.
        print "OnActivate Called"
        if event.GetActive():
            self.BringWindowToFront()
        event.Skip()
    
    def BringWindowToLower(self):
        print "Bring Window to Lower called, specifically for Mac"
        try:
            self.GetTopWindow().Lower()
        except:
            pass
        
    def BringWindowToFront(self):
        print "Bring Window To Front called"
        try: # it's possible for this event to come when the frame is closed
            self.GetTopWindow().Raise()
        except:
            pass
    
    def MacNewFile(self):
        pass
    
    def MacPrintFile(self, file_path):
        pass
    
    def OpenFileMessage(self, filename):
        pass
    
    def MacOpenFile(self, filename):
        pass   
     
app = MyApp(False) 
controller = Controller(app)
#import wx.lib.inspection 
#wx.lib.inspection.InspectionTool().Show()  
app.MainLoop()
    
