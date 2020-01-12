# 1. 필요한 Flask의 모듈들을 임포트한다.
# jsonify : dictionary 객체를 JSON으로 변환하여 HTTP 응답으로 보낼 수 있게 된다.
# request : 사용자가 HTTP 요청을 통해 전송한 JSON 데이터를 읽어들일 수 있다.
from flask import Flask, jsonify, request

# 3. flask.json 모듈에서 JSONEncoder 클래스를 임포트한다.
from flask.json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        # 4. JSON으로 변경하고자 하는 객체(obj)가 set인 경우 list로 변경해서 리턴한다.
        if isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)

app = Flask(__name__)
app.users = {}
app.id_count = 1
app.tweets = []

# 5. CustomJSONEncoder 클래스를 Flask의 defalut JOSONEncoder로 지정해준다.
# => 이러면 jsonify 함수가 호출될 때마다 JSONEncoder가 아닌 CustomJSONEncoder 클래스가 사용된다.
app.json_encoder = CustomJSONEncoder


@app.route("/sign-up", methods=["POST"])
def sign_up():
    # 2. HTTP 요청을 통해 전송된 회원 정보를 읽어 들인다.
    # request : 엔드포인트에 전송된 HTTP 요청 정보(헤더, 바디 등등)를 저장하고 있다.
    # request.json : 해당 HTTP 요청을 통해 전송된 JSON 데이터를 파이썬 dictionary로 변환해준다.
    new_user = request.json
    new_user["id"] = app.id_count
    
    app.users[app.id_count] = new_user
    
    app.id_count += 1

    return jsonify(new_user)


@app.route("/tweet", methods=["POST"])
def tweet():
    payload = request.json
    user_id = int(payload["id"])
    tweet = payload["tweet"]

    if user_id not in app.users:
        return "사용자가 존재하지 않습니다.", 400

    if len(tweet) > 300:
        return "300자를 초과했습니다.", 400

    user_id = int(payload["id"])
    app.tweets.append({
        "user_id": user_id,
        "tweet" : tweet
    })

    return "작성 완료", 200


@app.route("/follow", methods=["POST"])
def follow():
    payload = request.json
    user_id = int(payload["id"])
    user_id_to_follow = int(payload["follow"])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자가 존재하지 않습니다.", 400
    
    user = app.users[user_id]
    user.setdefault("follow", set()).add(user_id_to_follow)

    return jsonify(user)


@app.route("/unfollow", methods=["POST"])
def unfollow():
    payload = request.json
    user_id = int(payload["id"])
    user_id_to_follow = int(payload["unfollow"])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자가 존재하지 않습니다.", 400
    
    user = app.users[user_id]

    # remove() : 없는 값을 삭제하려고 하면 오류를 발생시킴
    # discard() : 없는 값을 삭제하려고 하면 무시함
    user.setdefault("follow", set()).discard(user_id_to_follow)

    return jsonify(user)


# 6. 엔드포인트의 주소에서 <int:user_id>는 엔드포인트의 주소에 해당 사용자의 아이디를 지정할 수 있게 해준다.
@app.route("/timeline/<int:user_id>", methods=["GET"])
def timeline(user_id):
    if user_id not in app.users:
        return "사용자가 존재하지 않습니다.", 400

    follow_list = app.users[user_id].get("follow", set())
    follow_list.add(user_id)

    timeline = [tweet for tweet in app.tweets if tweet["user_id"] in follow_list]

    return jsonify({
        "user_id": user_id,
        "timeline" : timeline
    })


# FLASK_APP=minitor.py FLASK_DEBUG=1 flask run