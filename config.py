# 데이터베이스 설정
# 이 파일을 config.py로 복사하고 실제 값으로 수정하세요
# config.py는 git에 포함되지 않습니다

# DB_HOST = 'localhost'
# DB_USER = 'car_db'
# DB_PASSWORD = 'car1245!@#$%'
# DB_NAME = 'car_db'


import os

# 환경 변수에서 데이터베이스 설정 가져오기
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'car_db')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'car1245!@#$%')
DB_NAME = os.environ.get('DB_NAME', 'car_db')