import tkinter as tk
from tkinter import filedialog
import pyinotify
import pyudev
from datetime import datetime
 #
def Upload():
    global path
    path = filedialog.askdirectory(initialdir = "/home/hamza", title = "Select the Folder you want to monitor")
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
        print("Hello2")
        text_box.insert(tk.END, create_str)

    def process_IN_DELETE(self, event):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        remove_str = date_time + ": " + "Removing:" + event.pathname + "\n"
        my_file = open("security.txt", "a+")
        my_file.write(remove_str+"\n")
        my_file.close()
        print("Hello3")        
        text_box.insert(tk.END, remove_str)

    def process_IN_MODIFY(self, event):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        if event.pathname != path:
            modify_str =  date_time + ": " + "Modified:" + event.pathname + "\n"
            my_file = open("security.txt", "a+")
            my_file.write(modify_str+"\n")
            my_file.close()
            print("Hello4")            
            text_box.insert(tk.END, modify_str)
    def process_IN_CLOSE_NOWRITE(self, event):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        if event.pathname != path:
            impermissible_str =  date_time + ": " + "READ-ONLY file was opened:" + event.pathname + "\n"
            my_file = open("security.txt", "a+")
            my_file.write(impermissible_str+"\n")
            my_file.close()
            print(impermissible_str)
            text_box.insert(tk.END, impermissible_str)


window = tk.Tk()

f = tk.Frame(window)
f.place(x=100, y=20)
#text_box = tk.Text(window)
##text_box.pack()
scrollbar = tk.Scrollbar(f)
text_box = tk.Text(f, height=25, width=125, yscrollcommand=scrollbar.set)
scrollbar.config(command=text_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_box.pack()
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
        formatted_str = date_time + ": " + '{0} - {1}\n'.format(action, device.get('ID_FS_LABEL'))
        my_file = open("security.txt", "a+")
        my_file.write("USB inserted : "+formatted_str+"\n")
        my_file.close()
        text_box.insert(tk.END, formatted_str)
def handle_click_start(event):
    context = pyudev.Context()

    text_box.delete(1.0, tk.END)

    global wm, wdd, notifier, observer

    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_CLOSE_NOWRITE # watched events

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
