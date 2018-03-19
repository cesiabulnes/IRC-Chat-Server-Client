import tkinter as tk
from tkinter import messagebox
import ChatClient as client
import BaseDialog as dialog
import BaseEntry as entry
import threading
import argparse
import utils
import logging
import os


class SocketThreadedTask(threading.Thread):
    def __init__(self, socket, callback):
        threading.Thread.__init__(self)
        self.socket = socket
        self.callback = callback

    def run(self):
        while True:
            try:
                message = self.socket.receive()

                if message == '/quit':
                    self.callback('> You have been disconnected from the chat room.')
                    self.socket.disconnect()
                    break
                else:
                    self.callback(message)
            except OSError:
                break


class ChatDialog(dialog.BaseDialog):
    def body(self, master):
        tk.Label(master, text="Enter host:").grid(row=0, sticky="w")
        tk.Label(master, text="Enter port:").grid(row=1, sticky="w")

        self.hostEntryField = tk.Entry(master)
        self.portEntryField = tk.Entry(master)

        self.hostEntryField.grid(row=0, column=1)
        self.portEntryField.grid(row=1, column=1)
        return self.hostEntryField

    def validate(self):
        host = str(self.hostEntryField.get())

        try:
            port = int(self.portEntryField.get())

            if(port >= 0 and port < 65536):
                self.result = (host, port)
                return True
            else:
                tk.messagebox.showwarning("Error", "The port number has to be between 0 and 65535. Both values are inclusive.")
                return False
        except ValueError:
            tk.messagebox.showwarning("Error", "The port number has to be an integer.")
            return False


class ChatWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.initUI(parent)

    def initUI(self, parent):
        self.messageScrollbar = tk.Scrollbar(parent, orient=tk.VERTICAL)
        self.messageScrollbar.grid(row=0, column=3, sticky="ns")

        self.messageTextArea = tk.Text(parent, bg="white", state=tk.DISABLED, yscrollcommand=self.messageScrollbar.set, wrap=tk.WORD)
        self.messageTextArea.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.usersListBox = tk.Listbox(parent, bg="white")
        self.usersListBox.grid(row=0, column=4, padx=5, sticky="nsew")

        self.entryField = entry.BaseEntry(parent, placeholder="Enter message.", width=80)
        self.entryField.grid(row=1, column=0, padx=5, pady=10, sticky="we")

        self.send_message_button = tk.Button(parent, text="Send", width=10, bg="#CACACA", activebackground="#CACACA")
        self.send_message_button.grid(row=1, column=1, padx=5, sticky="we")

    def update_chat_window(self, message):
        self.messageTextArea.configure(state='normal')
        self.messageTextArea.insert(tk.END, message)
        self.messageTextArea.configure(state='disabled')

    def send_message(self, **callbacks):
        message = self.entryField.get()
        self.set_message("")

        callbacks['send_message_to_server'](message)

    def set_message(self, message):
        self.entryField.delete(0, tk.END)
        self.entryField.insert(0, message)

    def bind_widgets(self, callback):
        self.send_message_button['command'] = lambda sendCallback = callback : self.send_message(send_message_to_server=sendCallback)
        self.entryField.bind("<Return>", lambda event, sendCallback = callback : self.send_message(send_message_to_server=sendCallback))
        self.messageTextArea.bind("<1>", lambda event: self.messageTextArea.focus_set())


class ChatGUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.initUI(parent)

        self.ChatWindow = ChatWindow(self.parent)

        self.clientSocket = client.Client()

        self.ChatWindow.bind_widgets(self.clientSocket.send)
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

    def initUI(self, parent):
        self.parent = parent
        self.parent.title("ChatApp")

        screenSizeX = self.parent.winfo_screenwidth()
        screenSizeY = self.parent.winfo_screenheight()

        frameSizeX = 800
        frameSizeY = 600

        framePosX = (screenSizeX - frameSizeX) / 2
        framePosY = (screenSizeY - frameSizeY) / 2

        self.parent.geometry('%dx%d+%d+%d' % (frameSizeX, frameSizeY, framePosX, framePosY))
        self.parent.resizable(True, True)

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.mainMenu = tk.Menu(self.parent)
        self.parent.config(menu=self.mainMenu)

        self.subMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label='File', menu=self.subMenu)
        self.subMenu.add_command(label='Connect', command=self.connect_to_server)
        self.subMenu.add_command(label='Exit', command=self.on_closing)

    def connect_to_server(self):
        if self.clientSocket.is_client_connected:
            return

        dialogResult = ChatDialog(self.parent).result

        if dialogResult:
            self.clientSocket.connect(dialogResult[0], dialogResult[1])

            if self.clientSocket.is_client_connected:
                SocketThreadedTask(self.clientSocket, self.ChatWindow.update_chat_window).start()
            else:
                tk.messagebox.showwarning("Error", "Unable to connect to the server.")

    def on_closing(self):
        if self.clientSocket.is_client_connected:
            self.clientSocket.send('/quit')

        self.parent.destroy()


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser("IRC Chat Client")
    argument_parser.add_argument(
        "-hostname",
        help="Hostname of the IRC Chat Server which the client should connect to",
        type=str
    )
    argument_parser.add_argument(
        "-u",
        help="Username of the IRC Chat Server which the client should claim itself as",
        type=str,
        required=True
    )
    argument_parser.add_argument(
        "-p",
        help="Port of the IRC Chat Server which the client should connect to",
        type=int
    )
    argument_parser.add_argument(
        "-c",
        help="Path of the Configuration file",
        type=str,
        required=True
    )
    argument_parser.add_argument(
        "-t",
        help="Test File",
        type=str
    )
    argument_parser.add_argument(
        "-L",
        help="Log file name, for log messages",
        type=str
    )

    arguments = argument_parser.parse_args()
    config_object = utils.get_config_from_file(getattr(arguments, "c"))

    hostname_setting = getattr(arguments, "hostname")
    if hostname_setting is None:
        hostname_setting = config_object.get("last_server_used")
        if hostname_setting is None:
            raise RuntimeError("No host setting from parameters or config file")

    username_setting = getattr(arguments, "u")

    port_setting = getattr(arguments, "p")
    if port_setting is None:
        port_setting = int(config_object.get("port"))
        if port_setting is None:
            raise RuntimeError("No port setting from parameters or config file")

    test_file_setting = getattr(arguments, "t")
    if test_file_setting is not None:
        if not os.path.exists(test_file_setting):
            raise RuntimeError("Specified test file does not exist")

    log_file_name_setting = getattr(arguments, "L")
    if log_file_name_setting is None:
        log_file_name_setting = config_object.get("default_log_file")
    log_enabled_setting = config_object.get("log", "False")
    if log_enabled_setting == "False":
        log_enabled_setting = False
    elif log_enabled_setting == "True":
        log_enabled_setting = True
    default_debug_mode_setting = config_object.get("default_debug_mode", "False")
    if default_debug_mode_setting == "False":
        default_debug_mode_setting = False
    elif default_debug_mode_setting not in [
        "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"
    ]:
        raise RuntimeError("default_debug_mode setting invalid")

    logger = logging.getLogger("chat_app")
    if default_debug_mode_setting is not False:
        logger.setLevel(getattr(logging, default_debug_mode_setting))
    if log_enabled_setting and log_file_name_setting:
        logger.addHandler(logging.FileHandler(log_file_name_setting))
    else:
        logger.addHandler(logging.NullHandler())

    root = tk.Tk()
    chatGUI = ChatGUI(root)
    chatGUI.clientSocket.connect(
        hostname_setting, port_setting, username_setting
    )
    if chatGUI.clientSocket.is_client_connected:
        SocketThreadedTask(chatGUI.clientSocket, chatGUI.ChatWindow.update_chat_window).start()
    if test_file_setting is not None:
        commands = utils.get_file_lines(test_file_setting)
        commands_fixed = \
            filter(lambda command_line: not command_line.startswith("#"),
                   map(lambda command_line: command_line.strip(), commands))
        for command in commands_fixed:
            chatGUI.clientSocket.send(command)
    root.mainloop()
