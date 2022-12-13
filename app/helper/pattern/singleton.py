class Singleton(type):
    """
    Singleton pattern, use it like: class Class(metaclass=Singleton):
    Only one instance of the singleton class can exist
    https://stackoverflow.com/questions/29697870/how-to-always-use-the-same-instance-of-a-class-in-python
    """
    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance
