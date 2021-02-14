class NotCorrectProvidedArgument(ValueError):
    def __init__(self, message: str):
        self.message = message


class TooManyArgumentsProvided(ValueError):
    def __init__(self, message: str):
        self.message = message
