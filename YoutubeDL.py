import threading
from time import sleep
from random import randint
import PySimpleGUIQt as sg
from pytube import YouTube
import glob
import subprocess
import os
from moviepy.editor import *
import shutil
from pathlib import Path

download_directory = ""
download_count = 0
file_size = 0
status = ''
home_dir = Path.home()
print(home_dir)
save_dir = str(home_dir) + '/Downloads'
print(save_dir)

def bars_callback(self, bar, attr, value,old_value=None):
    # Every time the logger progress is updated, this function is called        
    percentage = (value / self.bars[bar]['total']) * 100
    print(bar,attr,percentage)


def progress_function(stream = None, chunk = None, bytes_remaining = None):
    global download_count, file_size
    #Gets the percentage of the file that has been downloaded.
    print(file_size, bytes_remaining)
    download_count = (100*(file_size-bytes_remaining))/file_size
    print('{:00.0f}% downloaded'.format(download_count))


def download_file(window, link):
    global status, save_dir
    print('start downloading')
    status = 'start downloading'
    video = YouTube(link, on_progress_callback=progress_function)
    video_type = video.streams.filter(progressive = True, file_extension = "mp4").first()
    title = video.title
    print ("Fetching: {}...".format(title))
    status = "Downloading: {}...".format(title)
    global file_size
    file_size = video_type.filesize
    print(file_size)
    video_type.download()
    download_count = 100
    print('download completed.')
    status = 'Download completed.'
    dir = glob.glob("*.mp4")
    print(dir)
    name = [n.split('.')[0] for n in dir]
    print(name)
    #cmd = 'ffmpeg -i \"{0}.mp4\" \"{0}.mp3\"'.format(name[0])
    #subprocess.call(cmd, shell=True)
    videoclip = VideoFileClip('{}.mp4'.format(name[0]))
    audioclip = videoclip.audio
    status = 'Converting MP3 file.'
    audioclip.write_audiofile('{}.mp3'.format(name[0]))
    audioclip.close()
    videoclip.close()
    shutil.move('{}.mp3'.format(name[0]), '{}/{}.mp3'.format(save_dir, name[0]))
    os.remove(name[0]+".mp4")
    status = 'Finish Download {}.mp3'.format(name[0])

sg.theme('DarkAmber') 

progress_bar = [
    [sg.ProgressBar(100, size=(40, 20), pad=(0, 0), key='Progress Bar'),
     sg.Text("  0%", size=(4, 1), key='Percent'),],
]

layout = [
    [sg.Input(key='link',size=(40, 1)), sg.Button('Download',size=(10, 1)) ],
    [sg.Column(progress_bar, key='Progress', visible=False)],
    [sg.Text(key='-STATUS-')]
]

def main():
    global status, download_count
    window       = sg.Window('YoutubeDL', layout, size=(600, 200), finalize=True,
        use_default_focus=False)
    download     = window['Download']
    progress_bar = window['Progress Bar']
    percent      = window['Percent']
    progress     = window['Progress']
    while True:
        event, values = window.read(timeout=100)
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Download':
            download_count = 0
            status = ""

            print(values)
            link = values['link']
            count = 0
            download.update(disabled=True)
            progress_bar.update_bar(current_count=0, max=100)
            progress.update(visible=True)
            thread = threading.Thread(target=download_file, args=(window, link), daemon=True)
            thread.start()
        progress_bar.update_bar(current_count=download_count)
        percent.update(value='{:00.0f}%'.format(download_count))
        window['-STATUS-'].update(status)
        window.refresh()
        if download_count == 100:
            sleep(1)
            download.update(disabled=False)
        #    progress.update(visible=False)

    window.close()


if __name__ == "__main__":
    main()
