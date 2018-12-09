from .notification import AlertNotification, WarningNotification, ErrorNotification


class Notifier:

    def __init__(self, p_notify_filename):
        self._notify_filename = p_notify_filename
        self._alert = AlertNotification()
        self._warn = WarningNotification()
        self._error = ErrorNotification()
        self._notify = {'alert': self._alert, 'warning': self._warn, 'error': self._error}

    def process_notification(self, p_notification, p_sensor):
        if p_sensor.check_rule(p_notification.rule):
            i_message = p_sensor.fill_message(p_notification.message)
            i_message = self._notify[p_notification.type].wrap_message(i_message)
            with open(self._notify_filename, 'a') as f:
                f.write(i_message)
