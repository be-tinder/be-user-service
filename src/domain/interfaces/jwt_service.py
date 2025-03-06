from abc import abstractmethod, ABC


class IJWTService(ABC):
    @abstractmethod
    def encode_jwt(self, user_id) -> str:
        pass

    @abstractmethod
    def decode_jwt(self, token):
        pass
