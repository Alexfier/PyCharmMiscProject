from abc import ABC, abstractmethod

class APIClient(ABC):
    """ Abstract API Client """
    @abstractmethod
    def get_info(self):
        pass