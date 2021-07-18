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

    def __init__(self, file_data: UploadFile, interval: float, client_id: str):
        super().__init__(client_id)
        self.interval = interval
        self.file_data = file_data
        self.cur_url = os.getcwd()

    async def pre_precess(self) -> None:
        """Client로부터 요청받은 파일 데이터를 tmp에 저장"""
        self.input_root = f"{self.cur_url}/tmp/{self.client_id}-input.mid"
        self.output_root = f"{self.cur_url}/tmp/{self.client_id}-output.mid"

        with open(self.input_root, 'wb') as f:
            f.write(await self.file_data.read())

    async def process(self):
        config = pcfl.make_config(self.input_root, self.output_root, self.interval)
        pcfl.pcfl(config)
        os.unlink(self.input_root)

    async def post_process(self) -> tuple:
        file_data = open(self.output_root, mode='rb')
        return StreamingResponse(file_data, media_type='audio/mid'), self.output_root

    def remove_tmp_file_if_get_error(self):
        if self.input_root and os.path.isfile(self.input_root):
            os.unlink(self.input_root)
        elif self.output_root and os.path.isfile(self.output_root):
            os.unlink(self.output_root)

