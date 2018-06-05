class CailianPressNews:

    def __init__(self, datetime, text):
        self._datetime = datetime
        self._text = text

    @property
    def datetime(self):
        return self._datetime

    @datetime.setter
    def datetime(self, value):
        self._datetime = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

