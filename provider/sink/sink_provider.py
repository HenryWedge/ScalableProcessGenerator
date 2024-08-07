import abc
from core.event import AbstractEvent


class Sink:

    @abc.abstractmethod
    def send(self, event: AbstractEvent) -> None:
        pass


class SinkProvider:

    @abc.abstractmethod
    def get_sender(self, id) -> Sink:
        pass
