from datetime import datetime


class GenericNotification:

    def __init__(self):
        self._type = 'GEN'
        self._message_template = '[{type:<5}][{timestamp:<19}] {message}\n'

    def wrap_message(self, p_message):
        return self._message_template.format(type=self._type,
                                             timestamp=datetime.strftime(datetime.now(), '%d.%m.%YT%H:%M:%S'),
                                             message=p_message)


class AlertNotification(GenericNotification):

    def __init__(self):
        super().__init__()
        self._type = 'ALERT'


class WarningNotification(GenericNotification):

    def __init__(self):
        super().__init__()
        self._type = 'WARN'


class ErrorNotification(GenericNotification):

    def __init__(self):
        super().__init__()
        self._type = 'ERROR'
