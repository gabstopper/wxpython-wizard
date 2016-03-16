import wx

class TextObjectValidator(wx.PyValidator):
    
    def __init__(self, panel=None):
        wx.PyValidator.__init__(self)
        
        self.panel = panel
        print"Initialized validator with panel: %s"% self.panel

    def Clone(self):
        print "Cloned validator"
        return TextObjectValidator(self.panel)

    def Validate(self, win):
        """ Validate the contents of the given text control.
        """
        
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        print "TextCtrl: %s" % textCtrl
        print "Panel: %s" % self.panel
        print "Name: %s" % textCtrl.GetName()
        print "Text: %s: " % text
        
        if len(text) == 0:
            wx.MessageBox("A missing field is required before continuing!", "Error")
            textCtrl.SetBackgroundColour("light blue")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour(
                wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
            return True

    def TransferToWindow(self):
        """ Transfer data from validator to window.
            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        print "TransferToWindow"
        return True # Prevent wxDialog from complaining.


    def TransferFromWindow(self):
        """ Transfer data from window to validator.
            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        print "TransferFromWindow"
        return True # Prevent wxDialog from complaining.