"""
Defines the Logger class that should be used to display messages.
"""

class Logger(object):
    """
    Weefeesher Logger class.
    """

    @staticmethod
    def warning(msg):
        """
        Displays a warning message.
        """
        print '\033[1;34m /!\\ %s\033[0m' % msg

    @staticmethod
    def error(msg):
        """
        Displays an error message.
        """
        print '\033[1;31m --> %s\033[0m' % msg

    @staticmethod
    def info(msg):
        """
        Displays an informative message.
        """
        print '\033[35m [i] %s\033[0m' % msg

    @staticmethod
    def low(msg):
        """
        Displays an vuln with ``low`` associated risk.
        """
        print '\033[1;32m [i] %s\033[0m' % msg

    @staticmethod
    def medium(msg):
        """
        Displays an vuln with ``medium`` associated risk.
        """
        print '\033[1;33m [i] %s\033[0m' % msg

    @staticmethod
    def high(msg):
        """
        Displays an vuln with ``high`` associated risk.
        """
        print '\033[1;31m [i] %s\033[0m' % msg

    @staticmethod
    def critical(msg):
        """
        Displays an vuln with ``critical`` associated risk.
        """
        print '\033[1;35m [i] %s\033[0m' % msg

    @staticmethod
    def userinfo(msg):
        """
        Displays an user informative message.
        """
        print '\033[1;34m [>] %s\033[0m' % msg

    @staticmethod
    def ask(msg):
        """
        Asks for an user information.
        """
        return raw_input('\033[1;34m [<] %s\033[0m' % msg)

    @staticmethod
    def debug(msg):
        """
        Displays a debug message.
        """
        print '\033[1;32m [i] %s\033[0m' % msg
