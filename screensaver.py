import os

import pygtk

import gtk as Gtk
import gtk.gdk as Gdk

import webkit
import gobject

def is_screensaver_mode():
    return GsThemeWindow().get_anid()


class GsThemeWindow(Gtk.Window):
    __gtype_name__ = 'GsThemeWindow'


    def do_realize(self):
        anid = self.get_anid()
        if anid:
            self.window = Gdk.window_foreign_new(anid)
            self.window.set_events(Gdk.EXPOSURE_MASK | Gdk.STRUCTURE_MASK)
        else:
            self.window = Gdk.Window(
                self.get_parent_window(),
                width=600,
                height=600,
                window_type=Gdk.WINDOW_TOPLEVEL,
                wclass=Gdk.INPUT_OUTPUT,
                event_mask=self.get_events() | Gdk.EXPOSURE_MASK)

        self.window.set_user_data(self)
        x, y, self.w, self.h, depth = self.window.get_geometry()
        self.size_allocate(Gdk.Rectangle(x=x, y=y, width=self.w, height=self.h))
        self.set_default_size(self.w, self.h)

        self.set_flags(self.flags() | Gtk.REALIZED)
        self.set_decorated(False)
        self.style.attach(self.window)
        #self.style.set_background(self.window, Gdk.Color(0, 0, 0))
        #self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("black"))

    def get_anid(self):
        id = os.environ.get('XSCREENSAVER_WINDOW')
        return int(id, 16) if id else None

if __name__ == "__main__":
    window = GsThemeWindow()
    
    window.show()

    

    web_view = webkit.WebView()
    web_view.open("http://google.com")
    window.add(web_view)

    window.show_all()

    Gtk.main()