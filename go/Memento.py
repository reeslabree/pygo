# this is a hard pattern to implement in python
# as such inspiration taken from our friend the refactoring guru
# https://refactoring.guru/design-patterns/memento/python/example
###########################################################################
# MEMENTO PATTERN USED
#

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from random import sample
from string import ascii_letters, digits
import pickle
from copy import deepcopy

class Originator():
    _state_ = None
    def __init__(self, state) -> None:  # state is a dictionary - not sure how to annotate that
        self._state = state

    def update_state(self, state) -> None:
        self._state = state

    def save_memento(self) -> Memento:
        return ConcreteMemento(self._state)

    def restore(self, memento: Memento) -> None:
        self._state = memento.get_state()

    def current_state(self):
        return self._state

class Memento(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    def get_date(self) -> str:
        pass

class ConcreteMemento(Memento):
    def __init__(self, state) -> None:  # state is a dictionary and idk how to annotate that
        self._state = state
        self._date = str(datetime.now())[:19]
        self._id = self._generate_state_id()

    def _generate_state_id(self, length: int = 10) -> None:
        return ''.join(sample(ascii_letters, length))


    def get_state(self) -> str:
        return self._state

    def get_name(self) -> str:
        return f"{self._date} / ({self._id[0:5]}...)"

    def get_date(self) -> str:
        return self._date

class Caretaker():
    def __init__(self, originator: Originator) -> None:
        self._mementos = []
        self._originator = originator

    def backup(self) -> None:
        print('made backup') #TODO remove me
        self._mementos.append(self._originator.save_memento())

    def undo(self) -> bool:
        if not len(self._mementos):
            return False

        print('popped backup') #TODO remove me

        memento = self._mementos.pop()
        print(f'Restoring state to: {memento.get_name()}')

        try:
            self._originator.restore(memento)
        except Exception:
            print('encountered exception')
            self.undo()

        return True

    def show_history(self) -> None:
        for memento in self._mementos:
            print(memento.get_name())

    def show_detailed_history(self) -> None:
        for memento in self._mementos:
            print(memento.get_name())
            print(memento._state)

    def write_file(self, filename='.savefile') -> None:
        with open(filename, 'wb') as handle:
            pickle.dump(self._mementos[len(self._mementos) - 1], handle, protocol=pickle.HIGHEST_PROTOCOL)

    def read_file(self, filename='.savefile') -> None:
        with open(filename, 'rb') as handle:
            self._mementos = [pickle.load(handle)]
        #self._mementos = [deepcopy(data)]
