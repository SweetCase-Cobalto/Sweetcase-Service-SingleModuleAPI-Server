from system.client_list import ClientList


# Client Manager 인스턴스는 오직 하나만 존재해야 한다.
class ClientManager(object):
    client_list: ClientList

    def __new__(cls, *args):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ClientManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.client_list = ClientList()

    def generate_client_id(self) -> str:
        while True:
            client_id = ClientList.make_random_client_id(self.client_list.id_size)
            if self.client_list.add(client_id):
                break
        return client_id

    def remove_client_id(self, client_id: str):
        self.client_list.remove(client_id)
