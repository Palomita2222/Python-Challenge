import tkinter as tk
from tkinter import ttk
import time
import math
import socket
import threading
import os

is_running = False
start_time = 0
elapsed_time = 0

HOST = input("What is the IP of the server >> ")  # Server IP address
name = os.getlogin()
print(name)
PORT = 12345   # Server port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def End():
    window = tk.Tk()
    window.geometry("170x40")
    window.title("Sent!")
    window.resizable(False,False)
    Sent_widget = ttk.Label(window, text="Code sent!", font="Calibri 20 bold")
    Sent_widget.place(relx=0.05, rely=0.1)

def main():
    def starttimer():
        global is_running
        global start_time
        if not is_running:
            is_running = True
            start_time = time.time()
            update_time()

    def update_time():
        if is_running:
            elapsed_time = time.time() - start_time
            Timer.set(math.floor(elapsed_time*10)/10)
            Timer_widget.after(50, update_time)

    def place():
        Title.place(x=50, y=0)
        Timer_widget.place(x=310, y=0)
        Challenge_text.place(x=50, y=50)
        Code_text.place(x=50, y=100, width=300, height=300)
        Send.place(relx=0.5, rely=0.93, anchor="center")

    def send():
        global is_running
        code = Code_text.get("1.0", "end-1c")
        is_running = False
        message = f"{name}:\n{code}\nTime:{str(math.floor(elapsed_time*10)/10)}"
        client_socket.send(message.encode())
        window.destroy()
        End()
    
    def wait_for_server():
        data = client_socket.recv(1024).decode()
        if data != "":
            Challenge.set(f"Challenge : {data}")
            starttimer()
    
    def run_wait_for_server():
        thread = threading.Thread(target=wait_for_server)
        thread.daemon = True
        thread.start()
    
    window = tk.Tk()
    window.geometry("400x450")
    window.resizable(False,False)
    window.title("Python Challenge 1.0")
    Style = ttk.Style()
    Style.configure("W.TButton", font=("Calibri", "15", "bold"))
    Challenge = tk.StringVar()
    Challenge.set(f"Challenge :")
    Timer = tk.IntVar()
    Title = ttk.Label(window, text="Python Challenge", font="Calibri 20 bold underline")
    Challenge_text = ttk.Label(window, text="Challenge:", textvariable=Challenge, font="Calibri 15 bold")
    Timer_widget = ttk.Label(window, text=0.0, textvariable=Timer, font="Calibri 20 bold")
    Code_text = tk.Text(window, height=10, width=40, font="Calibri 13")  # Use Text widget for multi-line input
    Send = ttk.Button(window, text="Send Code", command=send, style="W.TButton")
    place()
    run_wait_for_server()
    window.mainloop()

main()