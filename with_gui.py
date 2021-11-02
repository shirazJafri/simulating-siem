import tkinter as tk
from tkinter import filedialog
import pyinotify
import pyudev
from datetime import datetime
import time
import os

def Upload():
    global path
    path = filedialog.askdirectory(title = "Select the Folder you want to monitor")
    my_file = open("security.txt", "a+")
    my_file.write(path+"\n")
    my_file.close()

class EventHandler(pyinotify.ProcessEvent):
    '''Event Logs are written to text box here'''
    def process_IN_CREATE(self, event):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        create_str = date_time + ": " + "Creating:" + event.pathname + "\n"
        my_file = open("security.txt", "a+")
        my_file.write(create_str+"\n")
        my_file.close()
        text_box.insert(tk.END, create_str)

    def process_IN_DELETE(self, event):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        remove_str = date_time + ": " + "Removing:" + event.pathname + "\n"
        my_file = open("security.txt", "a+")
        my_file.write(remove_str+"\n")
        my_file.close()
        text_box.insert(tk.END, remove_str)

    def process_IN_MODIFY(self, event):
        if event.pathname != path:
            date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
            last_modified = os.path.getmtime(event.pathname)
            modify_str = date_time + ": " + "Modified:" + event.pathname + "(Last Modified: " + time.ctime(last_modified) + ")\n"
            my_file = open("security.txt", "a+")
            my_file.write(modify_str+"\n")
            my_file.close()
            text_box.insert(tk.END, modify_str)

    # def process_IN_OPEN(self, event):
    #     date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    #     if event.pathname != path:
    #         access_str =  date_time + ": " + "The following file was accessed:" + event.pathname + "\n"
    #         my_file = open("security.txt", "a+")
    #         my_file.write(access_str+"\n")
    #         my_file.close()
    #         text_box.insert(tk.END, access_str)

    def process_IN_MOVED_TO(self, event):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        move_to_str =  date_time + ": " + "Files are being added to directory!!!\n"
        my_file = open("security.txt", "a+")
        my_file.write(move_to_str+"\n")
        my_file.close()
        text_box.insert(tk.END, move_to_str)

    def process_IN_MOVED_FROM(self, event):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        move_from_str =  date_time + ": " + "Files are being taken out of directory!!!\n"
        my_file = open("security.txt", "a+")
        my_file.write(move_from_str+"\n")
        my_file.close()
        text_box.insert(tk.END, move_from_str)

    def process_IN_MOVE_SELF(self, event):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        move_self_str =  date_time + ": " + "The directory itself is being moved!!!\n"
        my_file = open("security.txt", "a+")
        my_file.write(move_self_str+"\n")
        my_file.close()
        text_box.insert(tk.END, move_self_str)

    def process_IN_ATTRIB(self, event):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        if event.pathname != path:
            attrib_str =  date_time + ": " + "The following file's metadata was altered':" + event.pathname + "\n"
            my_file = open("security.txt", "a+")
            my_file.write(attrib_str+"\n")
            my_file.close()
            text_box.insert(tk.END, attrib_str)
    
    def process_IN_DELETE_SELF(self, event):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        del_self_str =  date_time + ": " + "The directory itself is being deleted!!!\n"
        my_file = open("security.txt", "a+")
        my_file.write(del_self_str+"\n")
        my_file.close()
        text_box.insert(tk.END, del_self_str)

window = tk.Tk()

f = tk.Frame(window)
f.place(x=100, y=20)
scrollbar = tk.Scrollbar(f)
text_box = tk.Text(f, height=25, width=125, yscrollcommand=scrollbar.set)
scrollbar.config(command=text_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_box.pack(expand= True, fill= tk.BOTH)
button_upload = tk.Button(
    f,
    text="Upload!",
    width=25,
    height=3,
    bg="blue",
    fg="yellow",
    command = Upload
)
button_upload.pack()
button_start = tk.Button(
    f,
    text="Start Logging!",
    width=25,
    height=3,
    bg="blue",
    fg="yellow",
)

button_start.pack()

button_stop = tk.Button(
    f,
    text="Stop Logging!",
    width=25,
    height=3,
    bg="blue",
    fg="yellow",
)
button_stop.pack()

button_history = tk.Button(
    f,
    text="History!",
    width=25,
    height=3,
    bg="blue",
    fg="yellow",
)
button_history.pack()

def log_event(action, device):
    if 'ID_FS_TYPE' in device:
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        formatted_str = date_time + ": USB Event - " + '{0} - {1}\n'.format(action, device.get('ID_FS_LABEL'))
        my_file = open("security.txt", "a+")
        my_file.write(formatted_str+"\n")
        my_file.close()
        text_box.insert(tk.END, formatted_str)

def handle_click_start(event):
    context = pyudev.Context()

    text_box.delete(1.0, tk.END)

    global wm, wdd, notifier, observer

    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_OPEN | pyinotify.IN_MOVE_SELF | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM | pyinotify.IN_ATTRIB | pyinotify.IN_MODIFY | pyinotify.IN_DELETE_SELF# watched events

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

def history_log(event):
    my_file2 = open("security.txt", "r")
    text_box.delete(1.0, tk.END)
    for x in my_file2:
        text_box.insert(tk.END,x)

button_start.bind("<Button-1>", handle_click_start)
button_stop.bind("<Button-1>", handle_click_stop)
button_history.bind("<Button-1>", history_log)

window.mainloop()