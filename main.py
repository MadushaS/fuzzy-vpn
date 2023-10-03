from app.gui import YouTubeDownloaderApp
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def main():
    app = YouTubeDownloaderApp()
    app.window.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()