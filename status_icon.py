import pygtk
pygtk.require('2.0')
import gtk

from format_sizes import human_readable

class StatusIcon(object):
    def __init__(self, menuItems):
        self.statusIcon = gtk.StatusIcon()
        self.statusIcon.set_from_stock(gtk.STOCK_NETWORK)
        self.updateTooltip({})

        self.menu = gtk.Menu()
        for label, callable in menuItems:
            menuItem = gtk.MenuItem(label)
            menuItem.connect('activate', callable)
            self.menu.append(menuItem)

        self.statusIcon.connect('popup-menu', self.showMenu, self.menu)

    def updateTooltip(self, devices_map):
        result = ['pay4bytes']
        for device_name, device_stats in devices_map.items():
            result.append('%s: RX %s x TX %s' %
                          (device_name,
                           human_readable(device_stats.receive.bytes),
                           human_readable(device_stats.transmit.bytes)))
        self.statusIcon.set_tooltip("\n".join(result))

    def show(self):
        self.statusIcon.set_visible(True)

    def hide(self):
        self.statusIcon.set_visible(False)

    def showMenu(self, widget, button, time, data = None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, gtk.status_icon_position_menu,
                           3, time, self.statusIcon)
