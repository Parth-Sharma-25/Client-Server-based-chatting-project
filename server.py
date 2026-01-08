import socket
import threading
import tkinter as tk

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9999))
server.listen()

client_socket = None

def start_server():
    global client_socket
    chat_box.insert(tk.END, "Server is listening...\n")
    client_socket, addr = server.accept()
    chat_box.insert(tk.END, f"Connected to {addr}\n")
    threading.Thread(target=receive_msg, daemon=True).start()

def receive_msg():
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            chat_box.insert(tk.END, f"Client: {msg}\n")
            if "exit" in msg.lower():
                break
        except:
            break

def send_msg():
    msg = entry.get()
    if msg and client_socket:
        client_socket.send(msg.encode())
        chat_box.insert(tk.END, f"You: {msg}\n")
        entry.delete(0, tk.END)

root = tk.Tk()
root.title("Server Chat")
root.geometry("500x400")
root.configure(bg="cyan")

chat_box = tk.Text(
    root,
    bg="white",
    fg="darkgreen",
    font=("Consolas", 11)
)
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(
    root,
    bg="white",
    fg="green",
    font=("Consolas", 11)
)
entry.pack(padx=10, pady=5, fill=tk.X)

send_button = tk.Button(
    root,
    text="Send",
    command=send_msg,
    bg="green",
    fg="white"
)
send_button.pack(pady=5)

threading.Thread(target=start_server, daemon=True).start()

root.mainloop()

if client_socket:
    client_socket.close()
server.close()
