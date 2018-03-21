import Util

class User:
    def __init__ (self, client_socket, username='', nickname='', name='', password='', level='user', status='', banned=False):
        self._client_socket = client_socket
        self._username = username
        self._nickname = nickname
        self._password = password
        self._level = level
        self._status = "Online"
        self._banned = banned

    @property
    def name(self):
        return self._name

    @property
    def socket(self):
        return self._client_socket

    @property
    def password(self):
        return self.password

    @property
    def banned(self):
        return self._banned

    @property
    def username(self):
        return self._username

    @property
    def nickname(self):
        return self._nickname

    @property
    def level(self):
        return self._level

    @property
    def password(self):
        return self._password

    @property
    def status(self):
        return self._status

    @username.setter
    def username(self, new_username):
        self._username = new_username

    @nickname.setter
    def nickname(self, new_nickname):
        self._nickname = new_nickname

    @level.setter
    def level(self, new_level):
        self._level = new_level

    @password.setter
    def password(self, new_password):
        self._password = new_password

    @status.setter
    def status(self, new_status):
        self._status = new_status

    @name.setter
    def name(self, new_name):
        self._name= new_name

    @password.setter
    def password(self, new_password):
        self._password= new_password

    @banned.setter
    def banned(self, new_banned):
        self._banned= new_banned
