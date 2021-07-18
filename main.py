from fastapi import APIRouter, FastAPI
from fastapi import File, UploadFile
from fastapi import Query
from starlette.background import BackgroundTasks
from system.client_manager import ClientManager
import os

from api.one_time.module_pcfl import ModulePCFL

# app = APIRouter()
app = FastAPI()

# make instance of main engines
client_manager = ClientManager()


@app.post("/pcfl")
async def process_pcfl(background_tasks: BackgroundTasks,
                       interval: float = Query(..., ge=0.01, le=0.5),
                       target_file: UploadFile = File(...) ):
    # get client_id
    client_id = client_manager.generate_client_id()
    processor = None

    # Running Process
    try:
        processor = ModulePCFL(target_file, interval, client_id)

        await processor.pre_precess()
        await processor.process()
        output_data, output_file_root = await processor.post_process()

        client_manager.remove_client_id(client_id)
        background_tasks.add_task(os.unlink, output_file_root)

        return output_data

    except Exception as e:
        if processor:
            processor.remove_tmp_file_if_get_error()
        client_manager.remove_client_id(client_id)
        raise e
