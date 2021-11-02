import tkinter as tk
import pyinotify
import pyudev
from datetime import datetime
import os

path = '/home/mrantiparallel/Desktop/to_monitor'

class EventHandler(pyinotify.ProcessEvent):
    '''Event Logs are written to text box here'''
    def process_IN_CREATE(self, event):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        create_str = date_time + ": " + "Creating:" + event.pathname + "\n"
        text_box.insert(tk.END, create_str)

    def process_IN_DELETE(self, event):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        remove_str = date_time + ": " + "Removing:" + event.pathname + "\n"
        text_box.insert(tk.END, remove_str)

    def process_IN_MODIFY(self, event):
        if event.pathname != path:
            date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
            last_modified = os.path.getmtime(event.pathname)
            secs = last_modified / 1e9
            dt = datetime.fromtimestamp(secs)
            last_modified_time = dt.strftime("%d-%m-%Y, %H:%M:%S")
            modify_str = date_time + ": " + "Modified:" + event.pathname + "(Last Modified: " + last_modified_time + ")\n"
            text_box.insert(tk.END, modify_str)

    def process_IN_CLOSE_NOWRITE(self, event):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        if event.pathname != path:
            impermissible_str =  date_time + ": " + "READ-ONLY file was opened:" + event.pathname + "\n"
            text_box.insert(tk.END, impermissible_str)

    def process_IN_ACCESS(self, event):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        if event.pathname != path:
            access_str =  date_time + ": " + "The following file was accessed:" + event.pathname + "\n"
            text_box.insert(tk.END, access_str)

window = tk.Tk()

text_box = tk.Text(window)

text_box.pack(expand= True, fill= tk.BOTH)

button_start = tk.Button(
    text="Start Logging!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
)

button_start.pack()

button_stop = tk.Button(
    text="Stop Logging!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
)

button_stop.pack()

def log_event(action, device):
    if 'ID_FS_TYPE' in device:
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        formatted_str = date_time + ": " + '{0} - {1}\n'.format(action, device.get('ID_FS_LABEL'))
        text_box.insert(tk.END, formatted_str)

def handle_click_start(event):
    context = pyudev.Context()

    text_box.delete(1.0, tk.END)

    global wm, wdd, notifier, observer

    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_CLOSE_NOWRITE | pyinotify.IN_ACCESS # watched events

    monitor = pyudev.Monitor.from_netlink(context)

    monitor.filter_by('block')

    wm = pyinotify.WatchManager()  # Watch Manager

    date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

    start_str = date_time + ": " + "Started Logging!\n"

    text_box.insert(tk.END, start_str)

    wdd = wm.add_watch(path, mask, rec=True, auto_add= True) # Edit directory here
    
    notifier = pyinotify.ThreadedNotifier(wm, EventHandler())

    observer = pyudev.MonitorObserver(monitor, log_event)

    observer.start()

    notifier.start()

def handle_click_stop(event):
    date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

    stop_str = date_time + ": " + "Stopping Logging!\n"

    text_box.insert(tk.END, stop_str)

    wm.rm_watch(wdd.values(), rec= True)

    observer.stop()

    notifier.stop()

button_start.bind("<Button-1>", handle_click_start)
button_stop.bind("<Button-1>", handle_click_stop)

window.mainloop()