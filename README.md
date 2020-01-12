# 깔끔한 파이썬 탄탄한 백엔드

[깔끔한 파이썬 탄탄한 백엔드] 도서 내용을 통해 기본 백엔드 개념 및 Flask 기본 개념을 학습했습니다.



#### 환경설정 파일

```shell
# .env
ROOT = "root"
PASSWORD = 설정 패스워드
HOST = "localhost"
PORT = 3306
DATABASE = "miniter"
```

#### MySQL 셋팅 (6장)

```shell
# 터미널에서 MySQL 접속
> mysql -u root -p
```

```sql
-- 데이터베이스 생성
> CREATE DATABASE miniter;

-- 데이터베이스 접근
> USE miniter;

-- users 테이블 생성
CREATE TABLE users(
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
	hashed_password VARCHAR(255) NOT NULL,
	profile VARCHAR(2000) NOT NULL,
	create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	update_at TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	UNIQUE KEY email (email)
);

-- users_follow_list 생성
CREATE TABLE users_follow_list(
	user_id INT NOT NULL,
	follow_user_id INT NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (user_id, follow_user_id),
	CONSTRAINT users_follow_list_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id),
	CONSTRAINT users_follow_list_follow_user_id_fkey FOREIGN KEY (follow_user_id) REFERENCES users(id)
);

-- tweets 테이블 생성
CREATE TABLE tweets(
	id INT NOT NULL AUTO_INCREMENT,
	user_id INT NOT NULL,
	tweet VARCHAR(300) NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	CONSTRAINT tweets_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id)
);
```
