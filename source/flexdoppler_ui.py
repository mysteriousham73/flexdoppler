import wx, wx.adv, platform

TRAY_TOOLTIP = 'FlexDoppler'
TRAY_ICON = 'icon.png'

class FDTrayIcon(wx.adv.TaskBarIcon):


    def __init__(self, radios):
        self.radios = radios
        super(FDTrayIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        self.menu = menu
        self.create_menu_item(menu, 'Start Tuning', self.do_nothing)
        menu.AppendSeparator()
        self.create_menu_item(menu, 'XVTRA', self.do_nothing)
        self.create_menu_item(menu, '    144 MHz', self.do_nothing)
        self.create_menu_item(menu, '    430 MHz', self.do_nothing)
        menu.AppendSeparator()
        self.create_menu_item(menu, 'XVTRB', self.do_nothing)
        self.create_menu_item(menu, '    144 MHz', self.do_nothing)
        self.create_menu_item(menu, '    430 MHz', self.do_nothing)
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Radios', self.do_nothing)
        for radio in self.radios:
            self.add_radio_menu_item(menu, radio, self.select_radio)
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Exit', self.on_exit)
        return menu


    def create_menu_item(self, menu, label, func):
        item = wx.MenuItem(menu, -1, label)
        menu.Bind(wx.EVT_MENU, func, id=item.GetId())
        menu.Append(item)
        return item

    def add_radio_menu_item(self, menu, radio, func):
        label = "    " + radio['model'] + " at " + radio['ip'] + ":" + radio['port']
        item = wx.MenuItem(menu, -1, label)
        if (radio['selected']):
            if (platform.system() == 'Windows'):
                font = item.GetFont()
                font.SetWeight(wx.BOLD)
                item.SetFont(font)
            else:
                item.SetItemLabel(item.GetItemLabel() + " *")

        menu.Bind(wx.EVT_MENU, lambda evt, temp=radio: func(evt, temp), id=item.GetId())

        menu.Append(item)
        return item

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        self.radios.timeout_radios(5)

    def select_radio(self, event, radio):
        self.radios.select_radio(radio)

    def do_nothing(self, event):
        pass
        #print("Do Nothing")

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)