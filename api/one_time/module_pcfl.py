from api.one_time.one_time_module import OneTimeModule
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
import submodule.PCFL.pcfl as pcfl

import os


class ModulePCFL(OneTimeModule):


    interval: float
    file_data: UploadFile
    cur_url: str

    input_root: str = None
    output_root: str = None

    """
        pcfl 알고리즘 돌릴 때 쓴다.
        자세한 내용은 여길 참고해보자: https://github.com/Vector-7/PCFL

        :param interval: 간격
        :param file_data: 파일 데이터
        :cur_url: 현재 프로젝트 루트
        :input_root:
        :output_root:
    """

    def __init__(self, file_data: UploadFile, interval: float, client_id: str):
        super().__init__(client_id)
        self.interval = interval
        self.file_data = file_data
        self.cur_url = os.getcwd() # 프로젝트 루트

    async def pre_precess(self) -> None:
        """Client로부터 요청받은 파일 데이터를 tmp에 저장"""
        self.input_root = f"{self.cur_url}/tmp/{self.client_id}-input.mid"
        self.output_root = f"{self.cur_url}/tmp/{self.client_id}-output.mid"

        with open(self.input_root, 'wb') as f:
            # 데이터 복사 -> input 파일에 저장
            f.write(await self.file_data.read())

    async def process(self):
        # pcfl 알고리즘 수행
        config = pcfl.make_config(self.input_root, self.output_root, self.interval)
        pcfl.pcfl(config)
        os.unlink(self.input_root)

    async def post_process(self) -> tuple:
        """
        프로세스가 끝난 파일을 클라이언트에 보내기 위해 정리
        :return: (파일 데이터, 아웃풋 파일 위치(삭제하기 위해 리턴))
        """
        file_data = open(self.output_root, mode='rb')
        response = StreamingResponse(file_data, media_type='audio/mid')
        response.headers['Content-Disposition'] = "attachment; filename=output.mid"

        return response, self.output_root

    def remove_tmp_file_if_get_error(self):
        # 실패시 사용
        if self.input_root and os.path.isfile(self.input_root):
            os.unlink(self.input_root)
        elif self.output_root and os.path.isfile(self.output_root):
            os.unlink(self.output_root)
