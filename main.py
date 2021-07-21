from fastapi import APIRouter, FastAPI
from fastapi import File, UploadFile
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware

from starlette.background import BackgroundTasks
from system.client_manager import ClientManager
import os

from api.one_time.module_pcfl import ModulePCFL

# set FastAPI
app = FastAPI(docs_url=None, redoc_url=None)
# app = FastAPI()

# Set CORS
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# make instance of main engines
# 클라이언트 번호를 관리하는 데 사용해야 하므로
# 절대 두개 이상 인스턴스를 생성하는 일이 없을 것
client_manager = ClientManager()

@app.post("/pcfl")
async def process_pcfl(background_tasks: BackgroundTasks,
                       interval: float = Query(..., ge=0.01, le=0.5),
                       target_file: UploadFile = File(...) ):
    """
    PCFL은 Midi 파일에서 연속된 서스테인 간격을 넓혀 Fl Studio에 정삭적으로 임포트하기 위해
    사용되는 알고리즘
    참고: https://github.com/Vector-7/PCFL

    :param background_tasks: 클라이언트 아이디 후 처리를 위한 Background
    :param interval: 서스테인 사이의 간격
    :param target_file: midi 파일
    :return: output data
        # 실패 시 아무러 데이터를 출력하지 않는다.
    """

    # 클라이언트 아이디 자동 생성
    client_id = client_manager.generate_client_id()
    processor = None

    # Running Process
    try:
        # 프로세서 생성
        processor = ModulePCFL(target_file, interval, client_id)

        # 프로세싱
        await processor.pre_precess()
        await processor.process()
        output_data, output_file_root = await processor.post_process()

        # 후처리
        client_manager.remove_client_id(client_id) # 작업이 끝났으므로 클라이언트 아이디 삭제
        background_tasks.add_task(os.unlink, output_file_root)
        # background_tasks는 해당 함수가 끝나고 실행이 된다.
        # 여기서는 작업이 끝나고 아웃풋 데이터를 삭제하는 데 사용된다.
        return output_data

    except Exception as e:
        # 에러처리
        if processor:
            # 더미파일 삭제
            processor.remove_tmp_file_if_get_error()
        client_manager.remove_client_id(client_id)
        raise e
