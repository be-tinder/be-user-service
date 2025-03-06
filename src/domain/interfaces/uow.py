from abc import ABC


class IUoW(ABC):
    def commit(self):
        pass

    def rollback(self):
        pass
