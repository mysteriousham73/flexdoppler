import wx, wx.adv, re, sys
import flexdoppler_radios, flexradio_network, macdoppler_network
from flexdoppler_ui import FDTrayIcon

# fix for pyinstaller packages app to avoid ReactorAlreadyInstalledError
if 'twisted.internet.reactor' in sys.modules:
    del sys.modules['twisted.internet.reactor']

from twisted.internet import wxreactor
wxreactor.install()

from twisted.internet import reactor

def main():
    print("FlexDoppler!")
    print("")

    radios = flexdoppler_radios.Radios()

    app = wx.App(False)
    #todo:  implement config, maybe a more generic lib than wx
    #todo:  sub xvtr all, pan all, slice all

    config = wx.Config("flexdoppler")
    selected_radio_serial = config.Read("selected_radio_serial")
    app.SetAppDisplayName("FlexDoppler")
    app.SetAppName("FlexDoppler")
    FDTrayIcon(radios)

    app.SetClassName("FlexDoppler")
    app.SetVendorDisplayName("FlexDoppler")
    app.SetVendorName("FlexDoppler")

    listener = reactor.listenMulticast(4992, flexradio_network.RadioDiscovery(radios),
                                       listenMultiple=True)

    mdlistener = reactor.listenMulticast(9932, macdoppler_network.listener(),
                        listenMultiple=True)

    reactor.registerWxApp(app)

    reactor.run()



if __name__ == '__main__':
    main()
