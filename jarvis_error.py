class WeatherError(Exception):

    '''Raise when weather app fails to grab weather'''
    def __init__(self, message, *args):
        self.message = messages
        self.args = args
        super(WeatherError, self).__init__(message, *args)