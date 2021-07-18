"""
    module_input_model.py

    Class ModuleInputModel

    FastAPI의 BaseModel의 하위 클래스로
    파리미터 를 받을 때 이 클래스를 상속받아서 사용해야 한다.
"""

from pydantic import BaseModel

class ModuleInputModel(BaseModel):
    pass