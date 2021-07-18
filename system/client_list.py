import random
from typing import Dict
import threading
import string


class ClientCharacterNode:
    def __init__(self, is_word: bool):
        self.child_nodes: Dict[str, ClientCharacterNode] = {}
        self.is_word: bool = is_word


class ClientList:
    """ 트라이 기반 클라이언트 리스트 """

    def __init__(self, id_size=20):
        self.client_list_header = ClientCharacterNode(False)
        self.client_control_mutex = threading.Lock()
        self.id_size = id_size

    def add(self, client_id: str) -> bool:

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
                return False
            else:
                cur_node.is_word = True
                return True

        # atom method for add function

        if not isinstance(client_id, str) or len(client_id) != 20:
            raise TypeError(f"client id must be string and size {self.id_size}")

        self.client_control_mutex.acquire()
        result = _add()
        self.client_control_mutex.release()
        return result

    def search(self, client_id: str) -> bool:

        if not isinstance(client_id, str) or len(client_id) != 20:
            raise TypeError(f"client id must be string and size {self.id_size}")

        cur_node = self.client_list_header
        for i in range(len(client_id)):
            if client_id[i] in cur_node.child_nodes:
                cur_node = cur_node.child_nodes[client_id[i]]
            else:
                return False

        return True if cur_node.is_word else False

    def remove(self, client_id: str) -> None:

        if not isinstance(client_id, str) or len(client_id) != 20:
            raise TypeError(f"client id must be string and size {self.id_size}")

        cur_node = self.client_list_header

        def _remove(node: ClientCharacterNode, key: str, cur_len: int) -> bool:
            if cur_len == len(key):
                # Checking last char is word
                return False if len(node.child_nodes) > 0 else True
            else:
                char = key[cur_len]
                if char in node.child_nodes:
                    if not _remove(node.child_nodes[char], key, cur_len + 1):
                        return False
                    else:
                        if cur_len + 1 == len(key) or not node.child_nodes[char].is_word:
                            del node.child_nodes[char]
                            return True
                        else:
                            return False
                else:
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
