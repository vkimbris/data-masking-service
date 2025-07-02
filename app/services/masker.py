from abc import ABC, abstractmethod


class BaseMasker(ABC):

    @abstractmethod
    def mask(self):
        pass

    @abstractmethod
    def de_mask(self):
        pass


class PresidioMasker(BaseMasker):

    def __init__(self):
        pass

    def mask(self):
        pass

    def de_mask(self):
        pass