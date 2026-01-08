import socket
import threading
import tkinter as tk

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("Your LAN ip address", 9999))

def receive_msg():
    while True:
        try:
            dat = client.recv(1024).decode()
            if not dat:
                break
            chat_box.insert(tk.END, f"Server: {dat}\n")
        except:
            break

def send_msg():
    mesg = entry.get()
    if mesg:
        client.send(mesg.encode())
        chat_box.insert(tk.END, f"You: {mesg}\n")
        entry.delete(0, tk.END)
        if "exit" in mesg.lower():
            root.destroy()

root = tk.Tk()
root.title("Client Chat")
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

threading.Thread(target=receive_msg, daemon=True).start()

root.mainloop()

client.close()
