import socket
import json
import threading
from tkinter import *
import tkinter as tk

# Connect to the server
server_ip = '127.0.0.1'
server_port = 82

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Create a global variable for the chat text box
txt = None


def send_msg(name, msg, typ):
    data = (name, msg, typ)
    client_socket.send(json.dumps(data).encode('utf-8'))

def recieve_msg(name):
    while True:
        rec = client_socket.recv(1024).decode('utf-8')
        if rec != '':
            (user, msgA, typ) = json.loads(rec)
            if user != name:
                WriteText(user, msgA)

def WriteText(user, msgA):
    txt.insert(END, "\n" + user + ": " + msgA)

def on_closing():
    client_socket.close()
    app.destroy()

def chat_app(name):
    root = Tk()
    root.title("Yoav's chat app")

    BG_GRAY = "#ABB2B9"
    BG_COLOR = "#17202A"
    TEXT_COLOR = "#EAECEE"

    FONT = "Helvetica 14"
    FONT_BOLD = "Helvetica 13 bold"

    lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome " + name , font=FONT_BOLD, pady=10, width=20, height=1).grid(row=0)
    
    
    global txt
    txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    txt.grid(row=1, column=0, columnspan=2)

    scrollbar = Scrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)

    e = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
    e.grid(row=2, column=0)

    def send():
        send = "You -> " + e.get()
        txt.insert(END, "\n" + send)
        msg = e.get()
        send_msg(name, msg, 1)
        e.delete(0, END)
    def exit_app():
        root.destroy()
        #client_socket.close()

    send_button = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send)
    send_button.grid(row=2, column=1)

    exit_button = Button(root, text="Exit", font=FONT_BOLD, bg=BG_GRAY, command=exit_app)
    exit_button.grid(row=0, column=1, columnspan=1)
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def submit_name():
    name = name_entry.get()
    if name != "":
        send_msg(name, "", 0)
        app.destroy()
        main_Run(name)

def main_Run(name):
    t1 = threading.Thread(target=chat_app, args=(name,))
    t2 = threading.Thread(target=recieve_msg, args=(name,))
    t2.start()
    t1.start()
    t1.join()

app = tk.Tk()
app.title("Chat App - Enter Your Name")

label = tk.Label(app, text="Enter Your Name:", width=40, height=7)
label.pack()

name_entry = tk.Entry(app)
name_entry.pack()

submit_button = tk.Button(app, text="Submit", command=submit_name)
submit_button.pack()

app.mainloop()

