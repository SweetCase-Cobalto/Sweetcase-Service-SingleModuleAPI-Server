from system.client_list import ClientList


# Client Manager 인스턴스는 오직 하나만 존재해야 한다.
class ClientManager(object):
    client_list: ClientList
    """
        클라이언트 번호 관리
        TODO 하지만 Session을 도입했을 때 사용하지 않는 것을 고려해야 한다.
    """

    def __new__(cls, *args):
        # 싱글톤 패턴 적용
        # 이미 인스턴스가 있다면 새로 생성하지 않고 기존 것을 보낸다.
        if not hasattr(cls, 'instance'):
            cls.instance = super(ClientManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.client_list = ClientList()

    def generate_client_id(self) -> str:
        # 아이디를 생성하고 리스트에 추가한다.
        while True:
            client_id = ClientList.make_random_client_id(self.client_list.id_size)
            if self.client_list.add(client_id):
                break
        return client_id

    def remove_client_id(self, client_id: str):
        # 클라이언트 삭제
        self.client_list.remove(client_id)
