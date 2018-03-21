
class Channel:
    def __init__ (self, name):
        self.users = []
        self.channel_name = name

    def welcome_user(self, username):
        all_users = self.get_all_users_in_channel()

        for user in self.users:
            if user.username == username:
                chatMessage = '\n\n> {0} have joined the channel {1}!\n|{2}'.format("You", self.channel_name, all_users).encode('utf8')
                user._client_socket.sendall(chatMessage)
            else:
                chatMessage = '\n\n> {0} has joined the channel!\n|{1}'.format(username, all_users).encode('utf8')
                user._client_socket.sendall(chatMessage)

    def broadcast_message(self, chatMessage, username=''):
        for user in self.users:
            if user.username == username:
                user._client_socket.sendall(">You: {0}".format(chatMessage).encode('utf8'))
            else:
                user._client_socket.sendall(">{0}: {1}".format(username, chatMessage).encode('utf8'))

    def private_message(self, message, sender, username=''):
        for user in self.users:
            if user.username == username:
                chatMessage = '\n\n> PRIVMSG from {0} {1}\n'.format(sender, message).encode('utf8')
                user._client_socket.sendall(chatMessage)

    def get_all_users_in_channel(self):
        return ' '.join([user.username for user in self.users])

    def remove_user_from_channel(self, user):
        self.users.remove(user)
        leave_message = "\n> {0} has left the channel {1}\n".format(user.username, self.channel_name)
        self.broadcast_message(leave_message)
