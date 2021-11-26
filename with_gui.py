import tkinter as tk
import tkinter.font as fnt
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import pyinotify
import pyudev
from datetime import datetime
import time
import os
import requests
import multiprocessing
import warnings
import cv2
import subprocess
from signal import SIGTERM
from process_count import getProcessCount
from kill_bitmap import cease_bitmap, cease_browser_activity

warnings.filterwarnings('ignore')
ADDRESS_FILE = 'old_ip_address.txt'

def Upload():
    global path
    global procCount
    procCount = getProcessCount()
    # print(procCount)
    path = filedialog.askdirectory(title = "Select the Folder you want to monitor", initialdir= "/home/mrantiparallel")
    print(path)
    my_file = open("security.txt", "a+")
    my_file.write(path + "\n")
    my_file.close()

    my_file_2 = open("warnings.txt", "a+")
    my_file_2.write(path + "\n")
    my_file_2.close() 

class EventHandler(pyinotify.ProcessEvent):
    '''Event Logs are written to text box here'''
    def process_IN_CREATE(self, event):
        if str(event.pathname).find('goutputstream') == -1:
            date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
            create_str = date_time + ": " + "Creating:" + event.pathname + "\n"
            my_file = open("security.txt", "a+")
            my_file.write(create_str+"\n")
            my_file.close()
            text_box.insert(tk.END, create_str)

            videoCaptureObject = cv2.VideoCapture(-1)
            result = True
            while(result):
                ret,frame = videoCaptureObject.read()
                filename = date_time + ": Intruder_Create.jpg"
                cv2.imwrite(filename,frame)
                result = False

            videoCaptureObject.release()
            cv2.destroyAllWindows()

    def process_IN_DELETE(self, event):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        remove_str = date_time + ": " + "Removing:" + event.pathname + "\n"
        my_file = open("security.txt", "a+")
        my_file.write(remove_str+"\n")
        my_file.close()
        text_box.insert(tk.END, remove_str)

        videoCaptureObject = cv2.VideoCapture(-1)
        result = True
        while(result):
            ret,frame = videoCaptureObject.read()
            filename = date_time + ": Intruder_Delete.jpg"
            cv2.imwrite(filename,frame)
            result = False
        videoCaptureObject.release()
        cv2.destroyAllWindows()

    def process_IN_MODIFY(self, event):
        if event.pathname != path:
            date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
            modify_str = date_time + ": " + "Accessed file was modified!\n"
            my_file = open("security.txt", "a+")
            my_file.write(modify_str+"\n")
            my_file.close()
            text_box.insert(tk.END, modify_str)

            videoCaptureObject = cv2.VideoCapture(-1)
            result = True
            while(result):
                ret,frame = videoCaptureObject.read()
                filename = date_time + ": Intruder_Modify.jpg"
                cv2.imwrite(filename,frame)
                result = False
            videoCaptureObject.release()
            cv2.destroyAllWindows()

    def process_IN_OPEN(self, event):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        if event.pathname != path and str(event.pathname).find('goutputstream') == -1:
            access_str =  date_time + ": " + "The following file was accessed:" + event.pathname + "\n"
            my_file = open("security.txt", "a+")
            my_file.write(access_str+"\n")
            my_file.close()
            text_box.insert(tk.END, access_str)

    def process_IN_MOVED_TO(self, event):
        if str(event.pathname).find('goutputstream') == -1:
            date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
            move_to_str =  date_time + ": " + "Files are being added to directory!!!\n"
            my_file = open("security.txt", "a+")
            my_file.write(move_to_str+"\n")
            my_file.close()
            text_box.insert(tk.END, move_to_str)
            if str(event.pathname).find('spawn_processes') != -1:
                process = subprocess.Popen([event.pathname])
                date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
                exec_str = date_time + ": Execution of unknown script commenced!\n"
                text_box2.insert(tk.END, exec_str)
                # print(date_time + ": Execution of unknown script commenced!")
                time.sleep(15)
                if (cease_browser_activity()):
                    browser_str = date_time + ": Un-identified Browser Activity! Terminating...\n"
                    # print(date_time + ": BROWSER ACTIVITY!!! Terminating...")
                    text_box2.insert(tk.END, browser_str)
                    my_file_2 = open("warnings.txt", "a+")
                    my_file_2.write(browser_str + "\n")
                    my_file_2.close()
                    videoCaptureObject = cv2.VideoCapture(-1)
                    result = True
                    while(result):
                        ret,frame = videoCaptureObject.read()
                        filename = date_time + ": Intruder_Browser.jpg"
                        cv2.imwrite(filename,frame)
                        result = False
                    videoCaptureObject.release()
                    cv2.destroyAllWindows()
                
                time.sleep(5)
                if getProcessCount() - procCount >= 5:
                    proc_str = date_time + ": More Than 5 Processes Of Infectious Nature are Being Spawned! Terminating...\n"
                    text_box2.insert(tk.END, proc_str)
                    my_file_2 = open("warnings.txt", "a+")
                    my_file_2.write(proc_str + "\n")
                    my_file_2.close()
                    cease_bitmap()
                    videoCaptureObject = cv2.VideoCapture(-1)
                    result = True
                    while(result):
                        ret,frame = videoCaptureObject.read()
                        filename = date_time + ": Intruder_Process_Spawn.jpg"
                        cv2.imwrite(filename,frame)
                        result = False
                    videoCaptureObject.release()
                    cv2.destroyAllWindows()

    def process_IN_MOVED_FROM(self, event):
        if str(event.pathname).find('goutputstream') == -1:
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
        if event.pathname != path and str(event.pathname).find('goutputstream') == -1:
            attrib_str =  date_time + ": " + "Following file metadata changed: " + event.pathname + "\n"
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
f.place(x=100, y=240)

ff = tk.Frame(window)
ff.place(x=1000, y=250)

t2 = tk.Frame(window)
t2.place(x=100, y=480)


scrollbar = tk.Scrollbar(f)
text_box = tk.Text(f, height=12, width=105, yscrollcommand=scrollbar.set)
scrollbar.config(command=text_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_box.pack(expand= True, fill= tk.BOTH)



scrollbar2 = tk.Scrollbar(t2)
text_box2 = tk.Text(t2, height=8, width=105, yscrollcommand=scrollbar.set, fg="red")
scrollbar2.config(command=text_box.yview)
scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
text_box2.pack(expand= True, fill= tk.BOTH)


user_name = Label(window, 
                  text = "Logging").place(x=100, y=220)  

user_name2 = Label(window, 
                  text = "Warning", foreground= 'red').place(x=100, y=460)  
# f = tk.Frame(window)
# f.place(x=100, y=20)
# scrollbar = tk.Scrollbar(f)
# text_box = tk.Text(f, height=25, width=125, yscrollcommand=scrollbar.set)
# scrollbar.config(command=text_box.yview)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# text_box.pack(expand= True, fill= tk.BOTH)

window.title("Security Information and Event Management (SIEM)")
window.geometry('850x850')
#window.configure(background='white')
#window.resizable(width=0, height=0)

w = Label(window, text='Security Information and Event Management System', font = fnt.Font(size = 16, family='Corbel'))
w.pack(padx = 0, pady = 10)

img = ImageTk.PhotoImage(master=window, file = r'ss1.png')
panel = tk.Label(window, image = img)

panel.image = img

panel.pack(side = "top", fill = "both")

button_upload = tk.Button(
    ff,
    text="Upload!",
    font = fnt.Font(size = 12, family='Tahoma bold'),
    width=25,
    height=3,
    bg="blue",
    fg="white",
    command = Upload
)
button_upload.pack(padx = 10, pady = 10)

button_start = tk.Button(
    ff,
    text="Start Logging!",
    font = fnt.Font(size = 12, family='Tahoma bold'),
    width=25,
    height=3,
    bg="blue",
    fg="white",
)

button_start.pack(padx = 10, pady = 10)

button_stop = tk.Button(
    ff,
    text="Stop Logging!",
    font = fnt.Font(size = 12, family='Tahoma bold'),
    width=25,
    height=3,
    bg="red",
    fg="white",
)
button_stop.pack(padx = 10, pady = 10)

button_history = tk.Button(
    ff,
    text="History!",
    font = fnt.Font(size = 12, family='Tahoma bold'),
    width=25,
    height=3,
    bg="blue",
    fg="white",
)
button_history.pack(padx = 10, pady = 10)
# button_upload = tk.Button(
#     f,
#     text="Upload!",
#     width=25,
#     height=3,
#     bg="blue",
#     fg="yellow",
#     command = Upload
# )
# button_upload.pack()
# button_start = tk.Button(
#     f,
#     text="Start Logging!",
#     width=25,
#     height=3,
#     bg="blue",
#     fg="yellow",
# )

# button_start.pack()

# button_stop = tk.Button(
#     f,
#     text="Stop Logging!",
#     width=25,
#     height=3,
#     bg="blue",
#     fg="yellow",
# )
# button_stop.pack()

# button_history = tk.Button(
#     f,
#     text="History!",
#     width=25,
#     height=3,
#     bg="blue",
#     fg="yellow",
# )
# button_history.pack()

def log_event(action, device):
    if 'ID_FS_TYPE' in device:
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        formatted_str = date_time + ": USB Event - " + '{0} - {1}\n'.format(action, device.get('ID_FS_LABEL'))
        my_file = open("security.txt", "a+")
        my_file.write(formatted_str+"\n")
        my_file.close()
        text_box2.insert(tk.END, formatted_str)

        videoCaptureObject = cv2.VideoCapture(-1)
        result = True
        while(result):
            ret,frame = videoCaptureObject.read()
            filename = date_time + ": Intruder_USB-Event.jpg"
            cv2.imwrite(filename,frame)
            result = False
        videoCaptureObject.release()
        cv2.destroyAllWindows()

def log_input_event(action, device):
    if 'ID_INPUT_MOUSE' in device and device.sys_name.startswith('event'):
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        formatted_str = date_time + ": Hardware Input Event - " + '{0} - {1}\n'.format(action, device.parent['NAME'])
        my_file = open("security.txt", "a+")
        my_file.write(formatted_str+"\n")
        my_file.close()
        text_box.insert(tk.END, formatted_str)

def handle_click_start(event):
    context = pyudev.Context()

    text_box.delete(1.0, tk.END)

    global wm, wdd, notifier, observer, ip_process, input_observer

    monitor = pyudev.Monitor.from_netlink(context)

    input_monitor = pyudev.Monitor.from_netlink(context)

    monitor.filter_by(subsystem= 'block')

    input_monitor.filter_by(subsystem= 'input')

    try:
        path
    except NameError:
        pass
    else:
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_OPEN | pyinotify.IN_MOVE_SELF | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM | pyinotify.IN_ATTRIB | pyinotify.IN_DELETE_SELF# watched events
        wm = pyinotify.WatchManager()  # Watch Manager
        wdd = wm.add_watch(path, mask, rec=True, auto_add= True)
        notifier = pyinotify.ThreadedNotifier(wm, EventHandler())
        notifier.start()

    ip_process = multiprocessing.Process(target= threading_function, args= ())

    date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

    start_str = date_time + ": " + "Started Logging!\n"

    text_box.insert(tk.END, start_str)

    observer = pyudev.MonitorObserver(monitor, log_event)

    input_observer = pyudev.MonitorObserver(input_monitor, log_input_event)

    input_observer.start()

    ip_process.start()

    observer.start()

def handle_click_stop(event):
    date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

    stop_str = date_time + ": " + "Stopping Logging!\n"

    text_box.insert(tk.END, stop_str)

    try:
        path
    except NameError:
        pass
    else:
        wm.rm_watch(wdd.values(), rec= True)
        notifier.stop()

    input_observer.stop()

    observer.stop()

    ip_process.terminate()

def history_log(event):
    my_file2 = open("security.txt", "r")
    text_box.delete(1.0, tk.END)
    for x in my_file2:
        text_box.insert(tk.END,x)

    my_file_2 = open("warnings.txt", "r")
    text_box2.delete(1.0, tk.END)
    for x in my_file_2:
        text_box2.insert(tk.END,x)

def detect_ip_changes():
    # [detect_ip_change ends]

    def persist_ip(ip):
        f = open(ADDRESS_FILE, 'w')
        f.write(ip)
        f.close()
    # [persist_ip ends]

    def read_old_ip():
        f = open(ADDRESS_FILE, 'r')
        oldIp = f.read()
        f.close()
        return oldIp
    # [read_old_ip ends]

    change = False

    currIp = requests.get('https://api.ipify.org').text

    if not os.path.isfile(ADDRESS_FILE):
        persist_ip('127.0.0.1')

    oldIp = read_old_ip()

    if currIp != oldIp and oldIp != '127.0.0.1':
        change = True
        date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        ip_change_str =  date_time + ": " + "Network change! IP address changed from {} to {}\n".format(oldIp, currIp)
        my_file = open("security.txt", "a+")
        my_file.write(ip_change_str+"\n")
        my_file.close()
        text_box.insert(tk.END, ip_change_str)

    persist_ip(currIp)
    
    return change

def threading_function():
    while True:
        change = detect_ip_changes()

        time.sleep(30)

button_start.bind("<Button-1>", handle_click_start)
button_stop.bind("<Button-1>", handle_click_stop)
button_history.bind("<Button-1>", history_log)

window.mainloop()
