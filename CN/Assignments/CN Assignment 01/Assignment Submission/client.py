from tkinter import *
import tkinter as tk
import socket as c
from time import sleep
import threading

socket_client = c.socket(c.AF_INET, c.SOCK_STREAM)
tx2 = ""


def send_message():
    tx2 = message_text_input.get("1.0", "end")
    message_list_box.insert(tk.END, str("You: " + tx2))
    message_text_input.delete('1.0', tk.END)
    socket_client.send(tx2.encode())
    tx2 = ""


def recieve_message():
    while True:
        reply = socket_client.recv(1024).decode()
        message_list_box.insert(tk.END, str(reply))


tx = ""


def text():
    tx = port_number_input.get("1.0", "end")
    socket_client.connect(('localhost', int(tx)))
    thread_for_recv_message = threading.Thread(target=recieve_message, )
    thread_for_send_message = threading.Thread(target=send_message, )
    thread_for_recv_message.start()
    thread_for_send_message.start()


# binding root objet to tkinter
messenger_app = tk.Tk()

# adding background color
messenger_app.configure(bg="gray")

# Giving Label to the client window
messenger_app.title("Instant LAN Messenger Client (by Bilal and Muaaz)")

# Setting the default size of the client window
messenger_app.geometry("500x600")

# Port number input taking field
port_number_input = Text(messenger_app, height=1, width=30)

# Label for port number input
label = Label(messenger_app, text="Enter Port number")
label.config(font=("Ariel", 14, 'bold'), bg='gray', fg='white')

# Creating a frame for connect and disconnect buttons
button_frame = tk.Frame(messenger_app)
# Giving background color
button_frame.configure(bg="gray")

# Creating listening and disconnecting button
start_listening_to_port_button = Button(
    button_frame, text="Start Listening to port", command=text)
disconnect_from_port_button = Button(
    button_frame, text="Disconnect  from port", command=messenger_app.destroy)

# Manisfesting Portnumber heading, port number input field and buttons on the GUI

label.grid(row=0, sticky='ew', pady=10)
port_number_input.grid(column=0, columnspan=3, row=1, padx=30)
messenger_app.grid_columnconfigure(0, weight=1)
button_frame.grid(column=0, row=2, sticky='nsew')
start_listening_to_port_button.pack(side='left', pady=10, padx=(110, 0))
disconnect_from_port_button.pack(side='right', pady=10, padx=(0, 110))

# Creating message text input field

message_text_input = Text(messenger_app, height=3, width=40)

# Manifesting message text input field
message_text_input.grid(row=3, pady=10)

# Creating message send button and binding it with a lambda function
send_message_button = Button(messenger_app, text="Send Message",
                             command=lambda: threading.Thread(target=send_message).start())

# Manifesting send message button
send_message_button.grid(row=4)

# Creating a Frame and a scrollbar

converation_frame = tk.Frame(messenger_app)
scrollbar = tk.Scrollbar(converation_frame, orient=VERTICAL)

# Creating a message box to display messages and binding it with a scrollbar
message_list_box = tk.Listbox(
    converation_frame, width=70, height=20, yscrollcommand=scrollbar)

# Configuring scrollbar with message box
scrollbar.config(command=message_list_box.yview)

# Manifesting scrollbar and messagebox
scrollbar.pack(side=RIGHT, fill=Y)
message_list_box.pack(pady=10, padx=10)

# Manifesting conversation frame
converation_frame.grid(row=5)

# Manifesting the complete GUI
tk.mainloop()
