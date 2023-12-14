import configparser

config = configparser.ConfigParser()

# 섹션과 키-값 설정 추가
config['dev'] = {
    'host': 'localhost',
    'port': '3306',
    'user': 'adviser',
    'password': '123123',
    'database': 'example'
}

# config.ini 파일에 쓰기
with open('config.ini', 'w') as configfile:
    config.write(configfile)
