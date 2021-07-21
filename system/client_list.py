import random
from typing import Dict
import threading
import string


class ClientCharacterNode:
    # 트라이 노드(철자 단위)
    def __init__(self, is_word: bool):
        self.child_nodes: Dict[str, ClientCharacterNode] = {}
        self.is_word: bool = is_word


class ClientList:
    client_list_header: ClientCharacterNode
    client_control_mutex: threading.Lock
    id_size: int

    """
        :var client_list_header: 클라이언트 리스트(트라이) 헤더
        :var client_control_mutex: 클라이언트 추가 및 삭제 시 순차적으로 진행해야 
            데이터 오류가 발생하지 않으므로 Lock을 설정
        :var id_size: 클라이언트 아이디 길이
        
        :function: add: 데이터 추가 (단 중복 불기)
        :function search: 데이터 검색
        :function remove: 데이터 삭제
    """

    def __init__(self, id_size=20):
        self.client_list_header = ClientCharacterNode(False)
        self.client_control_mutex = threading.Lock()
        self.id_size = id_size

    def add(self, client_id: str) -> bool:
        """
        :param client_id: 추가할 클라이언트 아이디
        :return: True(성공시), False(실패시)
        """

        def _add() -> bool:
            # Atom Function

            """
            :return: bool
                False mean client id is already exist
                True mean success
            """

            cur_node = self.client_list_header
            for char in client_id:
                if not char in cur_node.child_nodes:
                    cur_node.child_nodes[char] = ClientCharacterNode(False)
                cur_node = cur_node.child_nodes[char]

            if cur_node.is_word:
                # 이미 데이터가 존재하는 경우
                return False
            else:
                cur_node.is_word = True
                return True

        if not isinstance(client_id, str) or len(client_id) != self.id_size:
            # 에러처리
            raise TypeError(f"client id must be string and size {self.id_size}")


        # Process
        self.client_control_mutex.acquire()
        result = _add()
        self.client_control_mutex.release()
        return result

    def search(self, client_id: str) -> bool:
        """

        :param client_id:
        :return: True(성공... 알지?
        """
        # client id 처리
        if not isinstance(client_id, str) or len(client_id) != self.id_size:
            raise TypeError(f"client id must be string and size {self.id_size}")

        cur_node = self.client_list_header
        for i in range(len(client_id)):
            if client_id[i] in cur_node.child_nodes:
                cur_node = cur_node.child_nodes[client_id[i]]
            else:
                return False

        return True if cur_node.is_word else False

    def remove(self, client_id: str) -> None:

        """
        :param client_id:
        :return: X
        """

        if not isinstance(client_id, str) or len(client_id) != self.id_size:
            raise TypeError(f"client id must be string and size {self.id_size}")

        cur_node = self.client_list_header

        def _remove(node: ClientCharacterNode, key: str, cur_len: int) -> bool:
            if cur_len == len(key):
                # Checking last char is word
                # 근데 이건 데이터 길이가 일치하다는 조건 하에 있기 때문에
                # True로 처리
                return True
                # return False if not node.is_word else True
            else:
                char = key[cur_len]
                # 중간부분일 경우
                if char in node.child_nodes and _remove(node.child_nodes[char], key, cur_len + 1):
                    # 하위 검색에 의해 데이터가 일치할 경우
                    # 어차피 데이터 길이는 일정하기 때문에 바로 삭제한다.
                    del node.child_nodes[char]
                    return True
                else:
                    # 데이터가 불일치 할 경우
                    return False

        _remove(cur_node, client_id, 0)

    """ Static Methods """

    @staticmethod
    def make_random_client_id(id_size: int = 20) -> str:
        client_id: str = ""
        alphabets = string.ascii_lowercase
        for _ in range(id_size):
            """
                random 0 or 1
                if 1 ~ 3 then generate number
                else if 4 ~ 10 then generate alphabet
            """
            if 1 <= random.randint(1, 10) <= 3:
                # Setting Number
                client_id += str(random.randint(0, 9))
            else:
                client_id += random.choice(alphabets)
        return client_id


if __name__ == "__main__":
    c = ClientList()
    c1 = ClientList.make_random_client_id()
    c2 = ClientList.make_random_client_id()

    c.add(c1)
    c.add(c2)
    c.remove(c1)
    print(c.search(c1))