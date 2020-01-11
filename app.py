# 1. Flask에서 Flask 클래스를 임포트
from flask import Flask 

# 2. 임포트한 Flask 클래스를 객체화 시켜서 app이라는 변수에 저장. 이 app 변수가 바로 API 애플리케이션
# => app 변수에 API의 설정과 엔드포인트를 추가하면 API가 완성
app = Flask(__name__)

# 3. Flask의 route 데코레이터를 사용해 엔드포인트를 등록
@app.route("/ping", methods=["GET"])
# 4. 함수를 정의. route 데코레이터를 통해서 엔드포인트로 등록된 함수
def ping():
    return "pong"


# 실행 : FLASK_APP=app.py FLASK_DEBUG=1 flask run