import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
#Shit UI very bad

TCP_IP = 'localhost' 
TCP_PORT = 1600

class ClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("Конечный клиент")
        self.text_area = scrolledtext.ScrolledText(master, width=50, height=20)
        self.text_area.pack()
        #Помогите мне, что это вобще такое

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((TCP_IP, TCP_PORT))
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        buffer = ''
        while True:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if not data:
                    break
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    self.display_message(line)
            except:
                break

    def display_message(self, message):
        self.text_area.insert(tk.END, message + '\n')
        self.text_area.see(tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    app = ClientGUI(root)
    root.mainloop()