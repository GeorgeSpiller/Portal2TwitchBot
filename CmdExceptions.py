class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class CommandNotRecognised(Error):
    """Exception raised for errors in the portal2 console.

    Attributes:
        command -- the raw command string that was passed to the console
        message -- explanation of the error
    """

    def __init__(self, command, message):
        self.command = command
        self.message = message
