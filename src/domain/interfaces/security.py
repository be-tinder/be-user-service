from abc import abstractmethod, ABC


class IJWTService(ABC):
    @abstractmethod
    def encode_jwt(self, user_id, is_refresh) -> str:
        pass

    @abstractmethod
    def decode_jwt(self, token, is_refresh) -> str:
        pass
