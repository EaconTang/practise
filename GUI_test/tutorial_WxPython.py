#coding=utf-8
"""
Scripts4Test wxPython, buil a JSON Editor
"""
import os
import wx


class Editor(wx.Frame):
    """derived from a wxFrame,then onerwrite its __init__() method"""
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(-1,-1))     #"-1" means default size

        #a text box is a single-line field by default
        self.control = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.CreateStatusBar()      #add a statusbar
        fileMenu = wx.Menu()        #setup a menu(not menubar)

        #event handling
        menuOpen = fileMenu.Append(wx.ID_OPEN,"&Open","Open a file")
        self.Bind(wx.EVT_MENU,self.OnOpen,menuOpen)      #open file

        menuAbout = fileMenu.Append(wx.ID_ABOUT,"&About","Information about this app")
        self.Bind(wx.EVT_MENU,self.OnAbout,menuAbout)    #click "About" to excute OnAbout method

        menuExit = fileMenu.Append(wx.ID_EXIT,"&Exit","Exit the app")
        self.Bind(wx.EVT_MENU,self.OnExit,menuExit)      #exit

        menuBar = wx.MenuBar()      #create a menubar
        menuBar.Append(fileMenu,"&File")
        self.SetMenuBar(menuBar)    # add this menubar to the frame

        self.Show()     #pack the Show() method

    def OnExit(self,event):
        self.Close()

    def OnAbout(self,event):
        """show a dialog messagebox with a OK button"""
        dlg = wx.MessageDialog(self,"A simple Json Editor","About",wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnOpen(self,event):
        """open file"""
        self.dirname = ""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        #the return of ShowModal is the ID of the pressed button
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()

class MainWondow(wx.Frame):
    """ """
    def  __init__(self,parent,title):
        self.dirname = ""
        wx.Frame.__init__(self,parent,title=title,size=(-1,-1))
        self.control = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.CreateStatusBar()

        #setup menu
        filemenu = wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN,"&Open","Open a file")
        menuExit = filemenu.Append(wx.ID_EXIT,"&Exit","Quit the program")
        menuAbout = filemenu.Append(wx.ID_ABOUT,"&About","Information about this program")

        #events
        self.Bind(wx.EVT_MENU,self.OnOpen,menuOpen)
        self.Bind(wx.EVT_MENU,self.OnExit,menuExit)
        self.Bind(wx.EVT_MENU,self.OnAbout,menuAbout)

        #create menubar
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File",)
        self.SetMenuBar(menuBar)

        #create sizer2
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
        for i in range(6):          #add buttons to sizer2
            self.buttons.append(wx.Button(self,-1,"Button &"+str(i)))
            self.sizer2.Add(self.buttons[i],1,wx.EXPAND)

        #use some sizers to see layout option
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        #"1","0",means the proportion of control&sizer2("0" means no growth)
        self.sizer.Add(self.control,1,wx.EXPAND)        #EXPAND,it would auto-resize
        self.sizer.Add(self.sizer2,0,wx.SHAPED)         #SHAPED,it would remain its size

        #layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        self.Show()

    def OnOpen(self,e):
        """open file;if choose OK,read it"""
        dlg = wx.FileDialog(self,"Choose a file",self.dirname,"","*.*",wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            with open(os.path.join(self.dirname,self.filename),"r") as f:
                textContent = f.read()
                self.control.SetValue(textContent)
        dlg.Destroy()


    def OnExit(self,e):
        self.Close()

    def OnAbout(self,e):
        dlg = wx.MessageDialog(self,"A simple Editor","About",wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

class ExampleFrame(wx.Frame):
    """a simple frame with a panel containing a label"""
    def __init__(self,parent):
        wx.Frame.__init__(self,parent)
        panel = wx.Panel(self)
        wx.StaticText(panel,label="Your quote:",pos=(20,30))
        self.Show()

class ExamplePanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.quote = wx.StaticText(self,label="Your quote:",pos=(20,30))

        #a multiline textctrl
        self.logger = wx.TextCtrl(self,pos=(300,20),size=(200,300),style=wx.TE_MULTILINE|wx.TE_READONLY)

        #a button
        self.button = wx.Button(self,label="Save",pos=(200,325))
        self.Bind(wx.EVT_BUTTON,self.OnClick,self,button)

        #the edit control
        self.lblname = wx.StaticText(self,label="Your name:",pos=(20,60))
        self.editname = wx.TextCtrl(self,value="Enter here your name",pos=(150,60),size=(140,-1))
        self.Bind(wx.EVT_TEXT,self.EvtText,self.editname)
        self.Bind(wx.EVT_CHAR,self.EvtChar,self.editname)

        #the combobox control
        self.sampleList = ['friends','advertising','web search','Yellow Pages']
        self.lblhear = wx.StaticText(self,label="how did you hear from us?",pos=(20,90))
        self.edithear = wx.ComboBox(self,pos=(150,90),size=(95,-1),choices=self.sampleList,
                                    style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX,self.EvtComboBox,self.edithear)
        self.Bind(wx.EVT_TEXT,self.EvtText,self.edithear)

        #checkbox
        self.insure = wx.CheckBox(self,label="Do yo want Insured Shipment?",pos=(20,180))

        #radio boxes
        radioList = ['blue','red','yellow','orange','green','purple','navy bule','black','gray']
        rb = wx.RadioBox(self,label="What color would you like?",pos=(20,210),choices=radioList,
                         majorDimension=3,style=wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX,self.EvtRadioBox,rb)

    def EvtRadioBox(self,event):
        self.logger.AppendText('EvtRadioBox: %d\n'%event.GetInt())
    def EvtComboBox(self,event):
        self.logger.AppendText('EvtComboBox: %d\n'%event.GetString())
    def OnClick(self,event):
        self.logger.AppendText("Click on object with Id: %d\n"%event.GetId())
    def EvtText(self,event):
        self.logger.AppendText("EvtText: %s\n"%event.GetString())
    def EvtChar(self,event):
        self.logger.AppendText("EvtChar: %d\n"%event.GetKeyCode())
    def EvtCheckBox(self,event):
        self.logger.AppendText("EvtCheckBox: %d\n"%event.Checked())



def main():
    app = wx.App()
    frame = wx.Frame(None)
    panel = ExamplePanel(frame)
    frame.Show()
    app.MainLoop()


def aTest():
    """Scripts4Test"""
    app = wx.App()
    wxFrame = wx.Frame(None,wx.ID_ANY,"JSON Editor")
    wxFrame.Show()
    app.MainLoop()


#------------------------
if __name__ == "__main__":
    main()


