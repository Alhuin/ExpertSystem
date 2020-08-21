class Error(Exception):
    """Base class for other exceptions"""
    pass


class CustomError(Error):
    """Raised when I programmatically raise an error"""
    # print(Error)
    pass


class ParadoxError(Error):
    def __init__(self, fact):
        self.fact = fact

    def __str__(self):
        return repr(self.fact)
    """Raised when a paradox is detected"""
    # print(Error)
    pass


class Syntax(Error):
    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        return repr(self.rule)
    """Raised when a paradox is detected"""
    # print(Error)
    pass
