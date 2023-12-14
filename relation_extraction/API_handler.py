from abc import ABCMeta, abstractmethod

class APIHandler(metaclass=ABCMeta):
    @property
    @classmethod
    @abstractmethod
    def API_endpoint():
        """Property used to define the API_endpoint for the subclass of APIHandler"""
        pass

    @classmethod        
    @abstractmethod
    def send_request(request): 
        pass
