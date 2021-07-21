# Sweetcase-Service-SingleModuleAPI-Server
![fastapi](https://img.shields.io/badge/fastapi-109989?style=flat-square&logo=FASTAPI&logoColor=white)
![nginx](https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white)
![aws](https://img.shields.io/badge/AWS_EC2-232F3E?style=flat-square&logo=amazon-aws&logoColor=white)
### 직접 만든 알고리즘이나 Library를 웹상으로 지원하기 위한 서비스 (Backend, Single Module API)
해당 프로젝트에 대한 설명은 [Frontend Repo](https://github.com/SweetCase-Cobalto/Sweetcase-Service-client) 를 참고하세요<br />

* Single Module API
    * 해당 서비스 백엔드 시스템은 Single Module API입니다.
    * [Png 파일을 ico로 전환하는 서비스](https://convertio.co/kr/png-ico/) 처럼 회원 가입 없이 클릭 한번에 해결이 가능한 서비스들을 제공하는 시스템입니다.
    * 그 이상의 서비스(회원 가입 + 에디터 처럼 여러 작업을 수행향 하는 서비스)는 별개의 서버에 운영 예정입니다.
### 파일 루트
```
project
    `-api
    `-model
    `-submodule
    `-system
    `-tmp
    `-main.py
```
* api: 알고리즘을 서비스화 하기 위해 API를 작성하는 디렉토리 입니다.
* model: 클라이언트로부터 데이터를 받을 때 데이터 포맷을 정의하는 디렉토리 입니다. 모든 클래스는 **반드시 FastAPI.BaseModel로부터 상속받아야 합니다.**
* submodule: 서비스 하고자 하는 알고리즘의 Github Repo를 submodule로 보관합니다.
    * [참고: git submodule 사용법]("https://git-scm.com/book/ko/v2/Git-%EB%8F%84%EA%B5%AC-%EC%84%9C%EB%B8%8C%EB%AA%A8%EB%93%88")
    * **주의**: 파이썬으로 작성된 알고리즘을 권장합니다. 그렇지 않은 경우, 따로 프로세스를 생성해서 데이터를 송수신 해야 하는 코드를 따로 작성해야 합니다.
* system: 백엔드 시스템을 관리하는 기능을 작성하는 디렉토리
  * ClientList: 클라이언트가 서버에 접속했을 때 서버는 각 클라이언트 마다 20자 고유 번호를 배정합니다.
* tmp: 알고리즘이 작동할 때 임시파일을 저장하는 디렉토리 입니다.
  * **주의**: 반드시 해당 파일의 맨 앞부분은 **클라이언트 고유 아이디**로 설정해야 합니다.
* main.py: 최상위 실행부 입니다.