from fastapi import APIRouter, FastAPI
from fastapi import File, UploadFile

#app = APIRouter()
app = FastAPI()

@app.get("/")
async def test():
    return {"name": "hello world"}

@app.post("/pcfl")
async def process_pcfl(interval: float, target_file: UploadFile = File(...)):
    return {"data", target_file.filename }