import os

db = {
    "user" : os.environ.get("ROOT"),
    "password" : os.environ.get("PASSWORD"),
    "host" : os.environ.get("HOST"),
    "port" : os.environ.get("PORT"),
    "database" : os.environ.get("DATABASE")
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
JWT_SECRET_KEY = os.environ.get("JWT_SECREAT_KEY")
JWT_EXP_DELTA_SECONDS = 7 * 24 * 60 * 60