import threading
from time import sleep
from random import randint
import PySimpleGUIQt as sg

download_count = 0

def download_file(window):
    global download_count
    for count in range(0, 101, 2):     # Download file block by block
        sleep(0.1) 
        download_count = count

sg.theme("DarkBlue")

progress_bar = [
    [sg.ProgressBar(100, size=(40, 20), pad=(0, 0), key='Progress Bar'),
     sg.Text("  0%", size=(4, 1), key='Percent'),],
]

layout = [
    [sg.Button('Download')],
    [sg.Column(progress_bar, key='Progress', visible=False)],
]
window       = sg.Window('Title', layout, size=(600, 80), finalize=True,
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
        count = 0
        download.update(disabled=True)
        progress_bar.update_bar(current_count=0, max=100)
        progress.update(visible=True)
        thread = threading.Thread(target=download_file, args=(window, ), daemon=True)
        thread.start()
    
    progress_bar.update_bar(current_count=download_count)
    percent.update(value=f'{download_count:>3d}%')
    window.refresh()
    if download_count == 100:
        sleep(1)
        download.update(disabled=False)
        progress.update(visible=False)

window.close()
