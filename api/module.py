from abc import ABCMeta


class Module(metaclass=ABCMeta):
    client_id: str

    def __init__(self, client_id: str):
        self.client_id = client_id