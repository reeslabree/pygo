class Subject:
    def register_observer(self, observer):
        raise NotImplementedError

    def remove_observer(self, observer):
        raise NotImplementedError

    def notify_observers(self):
        raise NotImplementedError


class Observer:
    def update_score(self, w_score, b_score, player):
        raise NotImplementedError


class DisplayElement:
    def display_score(self):
        raise NotImplementedError
