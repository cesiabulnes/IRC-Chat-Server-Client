import socket
import sys
import logging


class Client:
    def __init__(self):
        self.is_client_connected = False
        self.client_socket = None
        self.logger = logging.getLogger("chat_app")

    def connect(self, host='', port=50000, username=None):
        self.logger.info("Chat client connecting")
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            self.is_client_connected = True
            self.logger.info("Chat client connected")

            # Username provided - send it as the first client message
            if username is not None:
                self.send(username)
        except socket.error as errorMessage:
            self.logger.error("Chat client connection error {error_message}".format(
                error_message=errorMessage
            ))
            if errorMessage.errno == socket.error.errno:
                sys.stderr.write('Connection refused to ' + str(host) + ' on port ' + str(port))
            else:
                sys.stderr.write('Failed to create a client socket: Error - %s\n', errorMessage[1])

    def disconnect(self):
        self.logger.info("Chat client disconnecting")
        if self.is_client_connected:
            self.client_socket.close()
            self.is_client_connected = False
            self.client_socket = None
            self.logger.info("Chat client disconnected")

    def send(self, data):
        self.logger.info("Chat client sending a message")
        if not self.is_client_connected:
            self.logger.error("Chat client cannot send a message - not connected")
            return

        self.client_socket.send(data.encode('utf8'))

    def receive(self, size=4096):
        self.logger.info("Chat client is receiving a message")
        if not self.is_client_connected:
            self.logger.error("Chat client cannot receive a message - not connected")
            return ""

        message = self.client_socket.recv(size).decode('utf8')
        self.logger.info("Chat client received a message: {message}".format(
            message=message
        ))
        return message
