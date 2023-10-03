from pytube import YouTube

def download_video(url, progress_callback, status_callback, item):
    try:
        yt = YouTube(url, on_progress_callback=progress_callback, on_complete_callback=status_callback)

        video = yt.streams.get_by_itag(item)

        if video:
            video.download(filename=yt.title.replace(" ","_"), output_path="~/Downloads", filename_prefix="fuzzy_")
        else:
            raise Exception("Invalid stream selection")
    except Exception as e:
        status_callback(f"Download failed: {str(e)}")
