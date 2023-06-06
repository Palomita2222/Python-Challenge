import tkinter as tk
from tkinter import ttk
import socket
import threading
#socket.gethostbyname(socket.gethostname())

sending = False
HOST =  "127.0.0.1" # Server IP address
PORT = 12345       # Server port
clients = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

def main():
    def place():
        Title.place(relx=0.03, rely=0)
        Challenge_indicator.place(relx=0.13, rely=0.18)
        Challenge.place(relx=0.13, rely=0.3)
        Send.place(relx=0.2, rely=0.82)

    def send():
        print(f"Challenge : {challenge.get()}")
        for client_socket in clients:
            client_socket.send(challenge.get().encode())
    
    
    def handle_client(client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    # Client disconnected
                    print("Client disconnected")
                    clients.remove(client_socket)
                    client_socket.close()
                    break
                else:
                    print(data)
            except (ConnectionAbortedError, ConnectionResetError):
                print("Client disconnected")
                clients.remove(client_socket)
                client_socket.close()
                break

    def waitForConnections():
        while True:
            server_socket.listen()
            client_socket, client_address = server_socket.accept()
            clients.append(client_socket)
            print(f"New client connected: {client_address}")
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.daemon = True
            thread.start()


    def getWaitForConnections():
        thread = threading.Thread(target=waitForConnections)
        thread.daemon = True
        thread.start()

    
    window = tk.Tk()
    window.geometry("300x300")
    window.resizable(False,False)
    window.title("Python Chall Console 1.0")
    Style = ttk.Style()
    Style.configure("W.TButton", font=("Calibri", "20", "bold"))

    challenge=tk.StringVar()
    Title = ttk.Label(window, text="Python Chall|Moderator Console", font="Calibri 15 bold underline")
    Challenge_indicator = ttk.Label(window, text="Enter Challenge:", font="Calibri 15 bold")
    Challenge =  ttk.Entry(window, textvariable=challenge, font="Calibri 15 bold")
    Send = ttk.Button(window, text="Start Challenge", command=send, style="W.TButton")

    getWaitForConnections()
    place()
    window.mainloop()


main()