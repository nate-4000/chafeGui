import socket
import threading
import tkinter as tk

SERVER_ADDRESS = ("masterxeon.hopto.org", 3337)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(SERVER_ADDRESS)
username = ""

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print("Received message:", message)
        except:
            client_socket.close()
            return
        if message.startswith('CHANGE\n'):
            new_content = message[7:]
            temp = chat_box.get("1.0", tk.END)
            chat_box.delete("1.0", tk.END)
            chat_box.insert(tk.END, temp + new_content + '\n')
            print("added")
            root.update()
        if message == "ALIVEREQ\n":
            client_socket.send("ALIVEOK\n".encode())

def send_message(event=None):
    message = input_box.get()
    if message == '/quit':
        client_socket.send("DISCONNECT\n".encode())
        root.quit()
    client_socket.send(("%s: %s\n" % (username, message)).encode())
    input_box.delete(0, tk.END)


def set_username(event=None):
    global username
    username = username_box.get()
    chat_box.insert(tk.END, username + " set as username\n")
    username_box.delete(0, tk.END)
    username_box.config(state=tk.DISABLED)
    input_box.config(state=tk.NORMAL)
    input_box.focus()

root = tk.Tk()
root.title("Chat Client")

chat_frame = tk.Frame(root)
chat_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

chat_box = tk.Text(chat_frame)
chat_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

input_frame = tk.Frame(root)
input_frame.pack(side=tk.BOTTOM, fill=tk.X)

username_box = tk.Entry(input_frame)
username_box.pack(side=tk.LEFT)
username_box.bind("<Return>", set_username)

input_box = tk.Entry(input_frame)
input_box.pack(side=tk.LEFT, fill=tk.X, expand=True)
input_box.bind("<Return>", send_message)
input_box.config(state=tk.DISABLED)

send_button = tk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT)

message_thread = threading.Thread(target=receive_messages)
message_thread.start()

root.mainloop()
client_socket.close()
