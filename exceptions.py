
from flask import Flask, jsonify

class AuthError(Exception):
    def __init__(self, message=''):
        self.message = message
        print(self.message)

    def __str__(self):
        return self.message


class NotFound(Exception):
    def __init__(self, message=''):
        self.message = message
        print(self.message)

    def __str__(self):
        return self.message

