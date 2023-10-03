import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from pytube import YouTube
from app.downloader import download_video
import requests
import tempfile

class YouTubeDownloaderApp:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("app/resources/yt-downloader.glade")
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("main_window")
        self.url_entry = self.builder.get_object("url_entry")
        self.progress_bar = self.builder.get_object("progress_bar")
        self.status_label = self.builder.get_object("status_label")
        self.quality_combo = self.builder.get_object("quality_combo")
        self.audio_only_check = self.builder.get_object("audio_only_check")
        self.download_panel = self.builder.get_object("download_box")
        self.thumbnail_image = self.builder.get_object("thumbnail_image")
        self.video_info_text = self.builder.get_object("video_title_label")  

        # resize the thumbnail image
        self.thumbnail_image.set_size_request(200, 200)  

        # hide the download panel by default
        self.download_panel.set_no_show_all(True)

    def on_check_button_clicked(self, button):
        url = self.url_entry.get_text().strip()
        self.status_label.set_text("Fetching video info...")
        try:
            yt = YouTube(url)
            self.populate_quality_options(yt)
            self.update_video_info(yt)
            self.download_panel.set_no_show_all(False)
            self.download_panel.show_all()
            self.status_label.set_text("Video info fetched successfully.")
        except Exception as e:
            self.status_label.set_text(f"Failed to fetch video info: {str(e)}")

    def update_video_info(self,yt):
        try:
            self.video_info_text.set_text(f"Title: {yt.title}\nAuthor: {yt.author}\nLength: {yt.length // 60}:{yt.length % 60} minutes")
            response = requests.get(yt.thumbnail_url)
            if response.status_code == 200:
                # Save the image to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                    tmp_file.write(response.content)
                    # Set the image from the temporary file
                    self.thumbnail_image.set_from_file(tmp_file.name)

            else:
                self.status_label.set_text("Please enter a valid YouTube URL.")
        except Exception as e:
            self.status_label.set_text(f"Failed to fetch video info: {str(e)}")
        

    def populate_quality_options(self,yt):
        # Clear existing options
        self.quality_combo.remove_all()
        quality_list = Gtk.ListStore(str,int)

        # Fetch available streams
        streams = yt.streams.filter(type='audio') if self.audio_only_check.get_active() else yt.streams
        for stream in streams:
            progressiveness = "(Audio only)" if stream.type=="audio" else "(Video Only)" if not stream.is_progressive else ""
            quality_list.append([f"{stream.resolution} - {stream.abr} - {stream.mime_type} {progressiveness}",stream.itag])

        self.quality_combo.set_model(quality_list)
        self.quality_combo.set_active(0)

    def on_main_window_destroy(self, *args):
        Gtk.main_quit()

    def on_download_button_clicked(self, button):
        url = self.url_entry.get_text().strip()
        if url:
            download_video(url, self.update_progress, self.update_status, item=self.quality_combo.get_model()[self.quality_combo.get_active()][1])
        else:
            self.status_label.set_text("Please enter a valid YouTube URL.")

    def update_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        fraction = (total_size - bytes_remaining) / total_size
        GLib.idle_add(self.progress_bar.set_fraction, fraction)
        GLib.idle_add(self.progress_bar.set_text, f"Downloading... {int(fraction * 100)}%")

    def update_status(self, status, whatever=None):
        if isinstance(status, Stream):
            status_message = f"Download complete: {status.title}"
        else:
            status_message = status
        print(status_message)
        print(whatever)
        self.status_label.set_text(status_message)

    def on_about_button_clicked(self, button):
        dialog = self.builder.get_object("about_dialog")
        dialog.run()
        dialog.hide()

    def on_about_close_button_clicked(self, button):
        dialog = self.builder.get_object("about_dialog")
        dialog.hide()
