# template from refactoring guru
# https://refactoring.guru/design-patterns/observer/python/example

from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List
import pygame

class Publisher(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
       pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
       pass

    @abstractmethod
    def notify(self) -> None:
       pass


class ConcretePublisher(Publisher):
    _message:str = 'black'
    _turn:str = ''

    _observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)
 
    def notify(self) -> None:
        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def update(self, player:str, message:str) -> None: 
        print(player, ' ', message)
        self._message = message
        self._turn = player
        self.notify()


class Observer(ABC):
    message = ''

    def get_message(self) -> str:
        return self.message

    @abstractmethod
    def update(self, subject: Publisher) -> None:
        pass

class MessageObserver(Observer):
    def update(self, subject: Publisher) -> None: 
        self.message = subject._message
        print('message obs: ', self.message) 

class PlayerObserver(Observer):
    def update(self, subject: Publisher) -> None:
        self.message = subject._turn
        print('player obs: ', self.message)
