from flask import Flask, request, jsonify, current_app
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text

class CustomJSONEncoder(JSONEncoder):
    """ 
    - Default JSON encoder는 set을 JSON으로 변환할 수 없음
    - 커스텀으로 작성해 set을 list로 변환해 JSON으로 처리 할 수 있게끔 구현
    """
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        
        return JSONEncoder.default(self, obj)


#==================== 쿼리문 시작 ====================#

def get_user(user_id):
    """
    생성한 사용자의 정보를 DataBase에서 읽어 들임
    """
    user = current_app.database.execute(text("""
        SELECT
            id,
            name,
            email,
            profile
        FROM users
        WHERE id = :user_id
    """), {
        "user_id" : user_id
    }).fetchone()

    return {
        "id" : user["id"],
        "name" : user["name"],
        "email" : user["email"],
        "profile" : user["profile"]
    } if user else None


def insert_user(user):
    """
    - 사용자 정보를 DataBase에 입력하는 함수
    - 만일 필드 이름이 틀리거나 필드가 부재인 경우 오류가 발생
    - 새로 사용자가 생성되면 새로 생성된 사용자의 id를 lastrowid를 통해 읽어 들임
    """
    return current_app.database.execute(text("""
        INSERT INTO users (
            name,
            email,
            profile,
            hashed_password
        ) VALUES (
            :name,
            :email,
            :profile,
            :password
        )
    """), user).lastrowid


def insert_tweet(user_tweet):
    """
    작성한 트윗을 DataBase에 입력하는 함수
    """
    return current_app.database.execute(text("""
        INSERT INTO tweets (
            user_id,
            tweet
        ) VALUES (
            :id,
            :tweet
        )
    """), user_tweet).rowcount


def insert_follow(user_follow):
    """
    팔로우한 사용자를 DataBase에 입력하는 함수
    """
    return current_app.database.execute(text("""
        INSERT INTO users_follow_list (
            user_id,
            follow_user_id
        ) VALUES (
            :id,
            :follow
        )
    """), user_follow).rowcount


def insert_unfollow(user_unfollow):
    """
    언팔로우한 사용자를 DataBase에 입력하는 함수
    """
    return current_app.database.execute(text("""
        DELETE FROM users_follow_list
        WHERE user_id = :id
        AND follow_user_id = :unfollow
    """), user_unfollow).rowcount


def get_timeline(user_id):
    """
    타임라인을 읽어들이는 함수
    """
    timeline = current_app.database.execute(text("""
        SELECT
            t.user_id,
            t.tweet
        FROM tweets t
        LEFT JOIN users_follow_list ufl ON ufl.user_id = :user_id
        WHERE t.user_id = :user_id
        OR t.user_id = ufl.follow_user_id
    """), {
        "user_id" : user_id
    }).fetchall()

    return [{
        "user_id" : tweet["user_id"],
        "tweet" : tweet["tweet"]
    } for tweet in timeline]

#==================== 쿼리문 끝 ====================#


#==================== API 시작 ====================#

def create_app(test_config = None):
    """
    - Flask가 create_app이라는 이름의 함수를 자동으로 팩토리 함수로 인식해서 해당 함수를 통해서 Flask 실행
    - create_app 함수가 test_config라는 인자를 받는 단위 테스트를 실행시킬 때 테스트용 데이터베이스 등의 테스트 설정 정보를 적용하기 위함
    """

    app = Flask(__name__)

    app.json_encoder = CustomJSONEncoder

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    # sqlalchemy의 create_engine 함수를 사용해 데이터베이스와 연결
    database = create_engine(app.config["DB_URL"], encoding="utf-8", max_overflow=0)
    # 위에서 발생한 engine 객체를 Flask 객체에 저장함으로써 create_app함수 외부에서도 데이터베이스를 사용할 수 있게 함
    app.database = database 


    @app.route("/ping", methods=["GET"])
    def ping():
        return "pong"


    @app.route("/sign-up", methods=["POST"])
    def sign_up():
        new_user = request.json
        new_user_id = insert_user(new_user)
        new_user = get_user(new_user_id)

        return jsonify(new_user)


    @app.route("/tweet", methods=["POST"])
    def tweet():
        user_tweet = request.json
        tweet = user_tweet["tweet"]

        if len(tweet) > 300:
            return "300자를 초과했습니다", 400

        insert_tweet(user_tweet)

        return "success", 200


    @app.route("/follow", methods=["POST"])
    def follow():
        payload = request.json
        insert_follow(payload)

        return 'success', 200

    
    @app.route("/unfollow", methods=["POST"])
    def unfollow():
        payload = request.json
        insert_unfollow(payload)

        return "success", 200

    
    @app.route("/timeline/<int:user_id>", methods=["GET"])
    def timeline(user_id):    
        return jsonify({
            "user_id" : user_id,
            "timeline" : get_timeline(user_id)
        })

    
    return app

#==================== API 끝 ====================#

# FLASK_APP=app.py FLASK_DEBUG=1 flask run