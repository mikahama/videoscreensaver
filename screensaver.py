import os

import pygtk, gst, gobject

import gtk as Gtk
import gtk.gdk as Gdk

def is_screensaver_mode():
    return GsThemeWindow().get_anid()


class GsThemeWindow(Gtk.Window):
    __gtype_name__ = 'GsThemeWindow'

    def set_video(self):
        self.connect('destroy', self.on_destroy)

        self.playbin = gst.element_factory_make('playbin2')
        self.playbin.set_property('uri', '/home/mika/small.ogv')

        self.sink = gst.element_factory_make('xvimagesink')
        self.sink.set_property('force-aspect-ratio', True)

        self.playbin.set_property('video-sink', self.sink)

        self.bus = self.playbin.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message::eos", self.on_finish)

        self.playbin.set_state(gst.STATE_PLAYING)

        self.drawingarea = Gtk.DrawingArea()
        self.drawingarea.connect('realize', self.on_drawingarea_realized)
        self.add(self.drawingarea)

    def on_finish(self, bus, message):
        self.playbin.set_state(gst.STATE_PAUSED)

    def on_destroy(self, window):
        self.playbin.set_state(gst.STATE_NULL)
        gtk.main_quit()

    def on_drawingarea_realized(self, sender):
        self.sink.set_xwindow_id(self.drawingarea.window.xid)

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
    
    window.set_video()
    
    window.show()

    

    #image = Gtk.Image()
    #image.show()
    #window.add(image)
    #image_file = '/home/mika/Escritorio/6862638-chris-evans.jpg'
    #pixbuf = Gdk.pixbuf_new_from_file(image_file)
    #pixbuf = pixbuf.scale_simple(window.w, window.h, Gdk.INTERP_BILINEAR)

    #image.set_from_pixbuf(pixbuf)

    window.show_all()

    Gtk.main()