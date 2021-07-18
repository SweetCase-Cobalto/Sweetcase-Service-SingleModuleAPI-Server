"""
    Class OneTimeModule

    딘 한번의 입력으로 결과가 바로 나오는
    알고리즘을 API화 할 때 사용하는 모듈

    입력 한번에 결과가 나오는 알고리즘을 서비스 하려면
    이 클래스를 상속받으면 된다.
"""

from abc import abstractmethod
from api.module import Module


class OneTimeModule(Module):

    def __init__(self, client_id: str):
        super().__init__(client_id)

    @abstractmethod
    async def pre_precess(self):
        pass

    @abstractmethod
    async def process(self):
        pass

    @abstractmethod
    async def post_process(self):
        pass
